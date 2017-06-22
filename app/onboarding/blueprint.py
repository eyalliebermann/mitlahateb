from flask import Blueprint, render_template, request
from flask_login import current_user, login_required

from app.core.blueprint import volunteer_s
from app.onboarding.forms import ProfileForm
from REST_API_logic import User_Profile_Data

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


@onboarding_bp.route("/API/profile_data", methods=('GET', 'POST'))
def profile_data():
    UPD = User_Profile_Data()
    json_in = request.get_json()
    if request.method == 'POST':
        return UPD.create_update_user_profile(json_in)
    if request.method == 'GET':
        return UPD.get_user_profile(json_in)
