import os

from flask import Blueprint, abort, request
from flask.helpers import flash
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla.fields import QuerySelectMultipleField
from flask_admin.contrib.sqla.view import ModelView
from flask_babelex import Domain
from flask_login import current_user
from wtforms import Form, StringField

from app import translations
from app.core import Organization, db, Job, Skill, Volunteer
from app.core.blueprint import security_s, volunteer_s, push_s

my_domain = Domain(
    dirname=os.path.dirname(translations.__file__))

admin = Admin(
    name=__name__,
    base_template='layout.html',
    template_mode='bootstrap3',
    translations_path=os.path.dirname(translations.__file__))

admin._menu = []

admin_bp = Blueprint(
    name='admin_mng',
    import_name=__name__,
    template_folder='templates')


@admin_bp.record_once
def init_admin(state):
    admin.init_app(state.app)


@admin_bp.before_app_request
def before_request_admin():
    # has false positives, please fix in the future
    if request.path.startswith(admin.url):
        if not current_user.is_authenticated:
            return abort(401)
        elif not security_s.is_level_sufficient(current_user, 'admin'):
            return abort(403)


class CustomView(ModelView):
    model = None
    view_level = 'admin'
    edit_level = 'admin'

    list_template = 'list.html'
    create_template = 'create.html'
    edit_template = 'edit.html'

    def is_accessible(self):
        if current_user.is_authenticated:
            return security_s.is_level_sufficient(current_user, self.view_level)
        return False

    @property
    def can_edit(self):
        if current_user.is_authenticated:
            return security_s.is_level_sufficient(current_user, self.edit_level)
        return False

    @property
    def can_create(self):
        return self.can_edit

    column_labels = dict(
        organization=my_domain.lazy_gettext('Organization'),
        job=my_domain.lazy_gettext('Job'),
        first_name=my_domain.lazy_gettext('First Name'),
        last_name=my_domain.lazy_gettext('Last Name'),
        name=my_domain.lazy_gettext('Name'),
        description=my_domain.lazy_gettext('Description'),
        jobs=my_domain.lazy_gettext('Jobs'),
        skills=my_domain.lazy_gettext('Skills'),
        level=my_domain.lazy_gettext('Level'),
        is_active=my_domain.lazy_gettext('Is Active'),
        events=my_domain.lazy_gettext('Events'),
        recurring=my_domain.lazy_gettext('Recurring'),
        start_time=my_domain.lazy_gettext('Start Time'),
        end_time=my_domain.lazy_gettext('End Time'),
        required_skills=my_domain.lazy_gettext('Required Skills'),
    )


class VolunteerView(CustomView):
    model = Volunteer
    view_level = 'user'
    edit_level = 'manager'
    can_create = False
    column_list = ['name', 'jobs']


class JobView(CustomView):
    model = Job
    view_level = 'user'
    edit_level = 'manager'
    column_list = ['organization', 'name', 'required_skills']


class OrganizationView(CustomView):
    model = Organization
    view_level = 'admin'
    edit_level = 'admin'


class SkillView(CustomView):
    model = Skill
    view_level = 'manager'
    edit_level = 'manager'


class NotificationsForm(Form):
    message = StringField(
        my_domain.lazy_gettext('Message'),
        validators=[])

    skills = QuerySelectMultipleField(
        my_domain.lazy_gettext('Skills'),
        query_factory=lambda: db.session.query(Skill),
        get_label=lambda x: x.name)

    organizations = QuerySelectMultipleField(
        my_domain.lazy_gettext('Organizations'),
        query_factory=lambda: db.session.query(Organization),
        get_label=lambda x: x.name)


class NotificationsView(BaseView):
    @expose('/', methods=('GET', 'POST'))
    def index(self):
        form = NotificationsForm(request.form)
        if request.method == 'POST' and form.validate():
            skills = [x.id for x in form.skills.data]
            organizations = [x.id for x in form.organizations.data]

            tokens = volunteer_s.find_tokens(
                skills=skills,
                organizations=organizations)

            push_s.push(
                tokens=tokens,
                body=form.message)

            flash(my_domain.gettext('Notifications sent successfully'))

        return self.render('notifications.html', form=form)


def add_view(name, view=CustomView):
    admin.add_view(view(
        model=view.model,
        session=db.session,
        name=name))


add_view(
    name=my_domain.lazy_gettext('Volunteers'),
    view=VolunteerView)

add_view(
    name=my_domain.lazy_gettext('Jobs'),
    view=JobView)

add_view(
    name=my_domain.lazy_gettext('Organizations'),
    view=OrganizationView)

add_view(
    name=my_domain.lazy_gettext('Skills'),
    view=SkillView)

admin.add_view(NotificationsView(
    name=my_domain.lazy_gettext('Send Notifications')))
