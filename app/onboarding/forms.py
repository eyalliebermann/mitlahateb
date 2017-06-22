from wtforms import Form, StringField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import input_required, length, required
from wtforms.widgets import Select

from app.admin.blueprint import my_domain
from app.core import Skill, db


class Select2Widget(Select):
    def __call__(self, field, **kwargs):
        kwargs.setdefault('data-role', 'select2')
        kwargs.setdefault('multiple', 'multiple')

        allow_blank = getattr(field, 'allow_blank', False)
        if allow_blank and not self.multiple:
            kwargs['data-allow-blank'] = '1'

        return super(Select2Widget, self).__call__(field, **kwargs)


class ProfileForm(Form):
    name = StringField(
        my_domain.lazy_gettext('Name'),
        validators=[required(), input_required(), length(min=5)])

    skills = QuerySelectMultipleField(
        my_domain.lazy_gettext('Skills'),
        query_factory=lambda: db.session.query(Skill),
        get_label=lambda x: x.name,
        widget=Select2Widget(multiple=True)
    )
