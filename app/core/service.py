from app.core.models import Volunteer, Skill, Organization
from app.extensions import db
from app.utils import SQLAlchemyService


class VolunteerService(SQLAlchemyService):
    __model__ = Volunteer
    __db__ = db

    def find_tokens(self, skills, organizations):
        s = self.__db__.session
        result = s.query(Volunteer.token_id).filter(
            Volunteer.organizations.any(
                Organization.id.in_(organizations)
            )
        ).filter(
            Volunteer.skills.any(
                Skill.id.in_(skills)
            )
        ).all()
        return [r[0] for r in result]
