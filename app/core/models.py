from sqlalchemy import Column, Integer, Unicode, ForeignKey, Table, String
from sqlalchemy.orm import relationship

from app.core.security import SqlalchemyUserMixin
from app.extensions import db


class Skill(db.Model):
    __tablename__ = 'skill'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64), nullable=False)

    def __unicode__(self):
        return self.name


class Organization(db.Model):
    __tablename__ = 'organization'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64), nullable=False)
    description = Column(Unicode(64))

    def __unicode__(self):
        return self.name


skill_to_job_table = Table(
    'skill_to_job',
    db.Model.metadata,
    Column('skill_id', Integer, ForeignKey('skill.id')),
    Column('job_id', Integer, ForeignKey('job.id')))


class Job(db.Model):
    __tablename__ = 'job'
    id = Column(Integer, primary_key=True)
    name = Column(Unicode(64))
    organization_id = Column(Integer, ForeignKey('organization.id'), nullable=False)
    organization = relationship(Organization)
    required_skills = relationship(Skill, secondary=skill_to_job_table)

    def __unicode__(self):
        return self.name


vol_to_job_table = Table(
    'vol_to_job',
    db.Model.metadata,
    Column('volunteer_id', String(64), ForeignKey('volunteer.id')),
    Column('job_id', Integer, ForeignKey('job.id')))

vol_to_skill_table = Table(
    'vol_to_skill',
    db.Model.metadata,
    Column('volunteer_id', String(64), ForeignKey('volunteer.id')),
    Column('skill_id', Integer, ForeignKey('skill.id')))


class Volunteer(db.Model, SqlalchemyUserMixin):
    __tablename__ = 'volunteer'
    name = Column(Unicode(64), nullable=False)
    jobs = relationship(Job, secondary=vol_to_job_table)
    skills = relationship(Skill, secondary=vol_to_skill_table)

    def __unicode__(self):
        return self.first_name + ' ' + self.last_name
