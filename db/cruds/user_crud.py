from db.models import User

from db.cruds.base_crud import BaseService


class UserService(BaseService[User]):
    def __init__(self):
        super().__init__(User)


user_service = UserService()  # Singleton instance
