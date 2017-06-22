from flask import Blueprint, render_template, request, jsonify
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


@onboarding_bp.route("/api/jobs")
def api_jobs():
    return jsonify({
        'jobs': [{
            'id': 1,
            'title': 'Hosting a guy in need!',
            'description': 'Host an f2m guy in need tonight! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent volutpat aliquet ante, ac suscipit odio consectetur in. Donec elementum nibh id congue venenatis. Etiam mattis et ex non blandit. Donec sed vestibulum neque. Ut egestas odio et sapien volutpat, ac laoreet odio placerat. Maecenas id metus volutpat, scelerisque magna eget, fermentum justo. Fusce quis mauris et elit luctus accumsan. Nunc sed nibh et nisi euismod pharetra. Morbi pretium hendrerit posuere. Aenean congue elit at convallis faucibus.',
            'date': '2017-06-21'
        }, {
            'id': 3,
            'title': 'Last Minute Call for securing Pride!',
            'description': 'Host an f2m guy in need tonight! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent volutpat aliquet ante, ac suscipit odio consectetur in. Donec elementum nibh id congue venenatis. Etiam mattis et ex non blandit. Donec sed vestibulum neque. Ut egestas odio et sapien volutpat, ac laoreet odio placerat. Maecenas id metus volutpat, scelerisque magna eget, fermentum justo. Fusce quis mauris et elit luctus accumsan. Nunc sed nibh et nisi euismod pharetra. Morbi pretium hendrerit posuere. Aenean congue elit at convallis faucibus.',
            'date': '2017-06-22'
        }, {
            'id': 4,
            'title': 'Missing story teller on Hoshen tommorow',
            'description': 'Host an f2m guy in need tonight! Lorem ipsum dolor sit amet, consectetur adipiscing elit. Praesent volutpat aliquet ante, ac suscipit odio consectetur in. Donec elementum nibh id congue venenatis. Etiam mattis et ex non blandit. Donec sed vestibulum neque. Ut egestas odio et sapien volutpat, ac laoreet odio placerat. Maecenas id metus volutpat, scelerisque magna eget, fermentum justo. Fusce quis mauris et elit luctus accumsan. Nunc sed nibh et nisi euismod pharetra. Morbi pretium hendrerit posuere. Aenean congue elit at convallis faucibus.',
            'when': '2017-06-23'
        }]
    })


@onboarding_bp.route("/API/profile_data", methods=('GET', 'POST'))
def profile_data():
    UPD = User_Profile_Data()
    json_in = request.get_json()
    if request.method == 'POST':
        return UPD.create_update_user_profile(json_in)
    if request.method == 'GET':
        return UPD.get_user_profile(json_in)
