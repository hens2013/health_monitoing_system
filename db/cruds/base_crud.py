from app.logger import logging

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Type, TypeVar, Generic, Optional, List
from sqlalchemy.orm import DeclarativeBase, joinedload
from sqlalchemy import inspect

# Define a generic model type
ModelType = TypeVar("ModelType", bound=DeclarativeBase)


class BaseService(Generic[ModelType]):
    """
    Optimized Base Service class providing common CRUD operations and optimized queries.
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model
        self.primary_key = self.get_primary_key()
        logging.info(f"{self.model.__name__} service initialized.")

    def get_primary_key(self) -> str:
        """
        Retrieves the primary key field name dynamically for the SQLAlchemy model.
        """
        return inspect(self.model).primary_key[0].name  # Gets the first primary key column name

    async def create(self, db: AsyncSession, obj_data: dict) -> ModelType:
        """
        Optimized creation method with exception handling.
        """
        try:
            new_obj = self.model(**obj_data)
            db.add(new_obj)
            await db.commit()
            await db.refresh(new_obj)
            logging.info(f"Created {self.model.__name__} with {self.primary_key}={getattr(new_obj, self.primary_key)}")
            return new_obj
        except Exception as e:
            await db.rollback()
            logging.error(f"Error creating {self.model.__name__}: {e}")
            return None

    async def bulk_create(self, db: AsyncSession, obj_data_list: List[dict]) -> List[ModelType]:
        """
        Optimized bulk insert operation.
        """
        try:
            new_objs = [self.model(**obj_data) for obj_data in obj_data_list]
            db.add_all(new_objs)
            await db.commit()
            for obj in new_objs:
                await db.refresh(obj)
            logging.info(f"Bulk insert completed for {len(new_objs)} records in {self.model.__name__}")
            return new_objs
        except Exception as e:
            await db.rollback()
            logging.error(f"Error in bulk creation for {self.model.__name__}: {e}")
            return []

    async def get_by_id(self, db: AsyncSession, obj_id: int, joins: Optional[List] = None) -> Optional[ModelType]:
        """
        Fetches a record by its primary key. Supports optional joins and optimized queries.
        """
        try:
            query = select(self.model).where(getattr(self.model, self.primary_key) == obj_id)
            if joins:
                for join_model in joins:
                    query = query.options(joinedload(join_model))  # Apply joins dynamically

            result = await db.execute(query)
            obj = result.scalars().first()
            if obj:
                logging.info(f"Retrieved {self.model.__name__} with {self.primary_key}={obj_id}")
            else:
                logging.warning(f"{self.model.__name__} with ID {obj_id} not found.")
            return obj
        except Exception as e:
            logging.error(f"Error retrieving {self.model.__name__} with ID {obj_id}: {e}")
            return None

    async def get_all(self, db: AsyncSession, joins: Optional[List] = None) -> List[ModelType]:
        """
        Retrieves all records, with optional joins for related tables.
        """
        query = select(self.model)
        if joins:
            for join_model in joins:
                query = query.options(joinedload(join_model))

        result = await db.execute(query)
        objs = result.scalars().all()
        logging.info(f"Retrieved {len(objs)} {self.model.__name__} records.")
        return objs

    async def get_by_user_id(self, db: AsyncSession, user_id: int, joins: Optional[List] = None) -> List[ModelType]:
        """
        Fetches all records related to a specific user, with optional joins.
        """
        query = select(self.model).where(getattr(self.model, "user_id") == user_id)
        if joins:
            for join_model in joins:
                query = query.options(joinedload(join_model))

        result = await db.execute(query)
        objs = result.scalars().all()
        logging.info(f"Retrieved {len(objs)} {self.model.__name__} records for user_id={user_id}.")
        return objs

    async def update(self, db: AsyncSession, obj_id: int, obj_data: dict) -> Optional[ModelType]:
        """
        Updates a record by primary key.
        """
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            logging.warning(f"Update failed: {self.model.__name__} with {self.primary_key}={obj_id} not found.")
            return None

        for key, value in obj_data.items():
            setattr(obj, key, value)

        await db.commit()
        await db.refresh(obj)
        logging.info(f"Updated {self.model.__name__} with {self.primary_key}={obj_id}")
        return obj

    async def delete(self, db: AsyncSession, obj_id: int) -> bool:
        """
        Deletes a record by primary key.
        """
        obj = await self.get_by_id(db, obj_id)
        if not obj:
            logging.warning(f"Delete failed: {self.model.__name__} with {self.primary_key}={obj_id} not found.")
            return False

        await db.delete(obj)
        await db.commit()
        logging.info(f"Deleted {self.model.__name__} with {self.primary_key}={obj_id}")
        return True
