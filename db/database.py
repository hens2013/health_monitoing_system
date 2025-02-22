import asyncio

import asyncpg
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.config import DB_URI, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
import os
from app.logger import logging
from db.base import Base

load_data_path = os.path.join(os.getcwd(), "data", "load_data.py")
# Create Async Database Engine
engine = create_async_engine(
    DB_URI,
    echo=True,
    future=True
)

# Create an Async Session Factory
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Dependency Injection for FastAPI Routes
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session



async def wait_for_db():
    """Wait for PostgreSQL to be ready before connecting."""
    retries = 10
    while retries:
        try:
            conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT,
                                         database="postgres")
            await conn.close()
            logging.info("✅ PostgreSQL is ready!")
            return
        except Exception as e:
            logging.warning(f"⏳ Waiting for PostgreSQL... {retries} attempts left")
            retries -= 1
            await asyncio.sleep(5)
    raise Exception("❌ PostgreSQL is not available. Exiting...")


async def create_database_if_not_exists():
    """Creates the database if it does not exist."""
    try:
        conn = await asyncpg.connect(user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT,
                                     database="postgres")
        result = await conn.fetchval(f"SELECT 1 FROM pg_database WHERE datname = '{DB_NAME}';")

        if not result:
            await conn.execute(f"CREATE DATABASE {DB_NAME} WITH OWNER {DB_USER};")
            logging.info(f"✅ Database '{DB_NAME}' created successfully.")
            return False
        else:
            logging.info(f"✅ Database '{DB_NAME}' already exists.")
            return True
        await conn.close()
    except Exception as e:
        logging.error(f"❌ Error creating database: {e}")


async def init_db():
    """Ensures PostgreSQL is ready, creates the database, and initializes tables."""
    await wait_for_db()
    is_exist=await create_database_if_not_exists()

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    if not is_exist:
        await run_load_data()
    logging.info("✅ Database initialized successfully.")


async def run_load_data():
    """
    Runs the `load_data.py` script after database initialization.
    """
    logging.info("Running load_data.py...")
    os.system(f"python {load_data_path}")
    logging.info("Data loading complete.")
