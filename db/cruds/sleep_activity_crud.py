from db.models import SleepingActivity

from db.cruds.base_crud import BaseService

class SleepService(BaseService[SleepingActivity]):
    def __init__(self):
        super().__init__(SleepingActivity)

sleep_service = SleepService()
