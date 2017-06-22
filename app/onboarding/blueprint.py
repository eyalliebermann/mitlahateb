from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.core.blueprint import volunteer_s
from app.onboarding.forms import ProfileForm

onboarding_bp = Blueprint(
    name='onboarding',
    import_name=__name__,
    template_folder='templates')


@onboarding_bp.route("/")
def index():
    return render_template('index.html')


@onboarding_bp.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    user_model = current_user._get_current_object()

    form = ProfileForm(
        request.form,
        obj=user_model)

    if request.method == 'POST' and form.validate():
        form.populate_obj(user_model)
        volunteer_s.save(user_model)

    return render_template(
        'profile.html',
        user=current_user,
        form=form)
