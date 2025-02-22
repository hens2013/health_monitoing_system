from db.models import DailySteps

from db.cruds.base_crud import BaseService


class StepService(BaseService[DailySteps]):
    def __init__(self):
        super().__init__(DailySteps)


step_service = StepService()
