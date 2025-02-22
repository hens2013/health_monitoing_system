from db.models import Test

from db.cruds.base_crud import BaseService


class TestService(BaseService[Test]):
    def __init__(self):
        super().__init__(Test)

test_service = TestService()
