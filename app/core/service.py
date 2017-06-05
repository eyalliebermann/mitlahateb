from app.core.models import Volunteer
from app.extensions import db
from app.utils import SQLAlchemyService


class VolunteerService(SQLAlchemyService):
    __model__ = Volunteer
    __db__ = db
