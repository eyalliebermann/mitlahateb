from flask import Blueprint, render_template
from flask_login import current_user, login_required

onboarding_bp = Blueprint(
    name='onboarding',
    import_name=__name__,
    template_folder='templates')


@onboarding_bp.route("/")
def index():
    return render_template('index.html')


@onboarding_bp.route("/profile")
@login_required
def profile():
    return render_template('profile.html', user=current_user)
