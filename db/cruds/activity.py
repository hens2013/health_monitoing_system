from db.models import PhysicalActivity

from db.cruds.base_crud import BaseService


class ActivityService(BaseService[PhysicalActivity]):
    def __init__(self):
        super().__init__(PhysicalActivity)


activity_service = ActivityService()
