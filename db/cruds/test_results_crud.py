from db.models import TestResult

from db.cruds.base_crud import BaseService


class TestResultService(BaseService[TestResult]):
    def __init__(self):
        super().__init__(TestResult)


test_result_service = TestResultService()
