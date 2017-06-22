from notifications import MitlahatebPushMessageSet
from models import Skill, Organization, Job, Volunteer
from sqlalchemy.orm.query import Query

class NotificationService(object):
    def find_relevant_volunteers(self, skills, organizations):
        # db.session
        # Select token from tbl_volunteers join tbl_vol_skills on volunteers.volunteer_id = tbl_vol_skills.volunteer_id)
        #   and exists
        return
