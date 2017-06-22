from app.core.models import Skill, Organization, Job, Volunteer, vol_to_org_table, vol_to_job_table, vol_to_skill_table
from app.core import db
from sqlalchemy.orm.query import Query
from sqlalchemy import update, insert, delete
from flask import jsonify, make_response
import json



class User_Profile_Data:
    """
    This User Profile Data block manages interactions with the user profile objects in the database.
    >>> UPD = User_Profile_Data()
    >>> UPD.create_update_user_profile('{"ID": "1","name": "Dylan","jobs": [1, 2, 3],"organizations": [1, 2, 3],"skills": [1, 2, 3],"token_id" : ["ExponentPushToken[MS85tsPivE9r94XIbS2ODD]"]}')

    """

    def __init__(self):
        self.name = ""
        self.jobs = []
        self.organizations = []
        self.skills = []
        self.token_id = ""

    def create_update_user_profile(self, json_dict):
        # if user ID is not null, load profile data and update.  Check user ID == login ID (possible security hole)
        s = db.session
        if json_dict['ID'] != None and json_dict['ID'] != '':
            # load profile data
            current_volunteer = s.query(Volunteer).filter(Volunteer.id == json_dict['ID']).first()
            # Update profile data
            if current_volunteer != None:
                upd_qry = update(Volunteer).where(Volunteer = current_volunteer)\
                    .values(token_id = json_dict["token_id"])
                # Update current volunteer skills.  Note: may require a full clear, I am not certain. DB
                current_volunteer.skills = json_dict["skills"]
                # Insert query combining all skills in json_dict["skills"] and json_dict["ID"].
                s.commit();
        else:
            current_volunteer = s.add();
            # Create profile row (else)
            ins = Volunteer.insert().values(id=json_dict['ID'], name=json_dict['Name'], token_id=json_dict['Token_ID'])
            # execute the insert.
            s.execute(ins)
            # Pull the inserted volunteer out of the database.  Pulling the inserted row would be more efficient.
            current_volunteer = s.query(Volunteer).filter(Volunteer.id == json_dict['ID']).first()
            current_volunteer.skills = json_dict["skills"]
            s.commit();

    def get_user_profile(self, api_data):

        return