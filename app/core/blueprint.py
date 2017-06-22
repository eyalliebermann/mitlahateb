from logging import getLogger

from flask import redirect, render_template, Blueprint, request, abort, session
from flask_babelex import Babel, get_locale
from flask_login import LoginManager, logout_user, login_user

from app.core.core import SecurityService
from app.core.service import VolunteerService
from app.errors import JWTExpiredError, AppError

logger = getLogger(__name__)

core_bp = Blueprint(
    name='security',
    import_name=__name__,
    template_folder='templates')

volunteer_s = VolunteerService()
security_s = SecurityService(volunteer_s)

login_manager = LoginManager()
babel = Babel()


@core_bp.record_once
def core_init(state):
    babel.init_app(state.app)
    login_manager.init_app(state.app)

    security_s.domain = state.app.config['AUTH0_DOMAIN']
    security_s.client_id = state.app.config['AUTH0_CLIENT_ID']
    security_s.client_secret = state.app.config['AUTH0_CLIENT_SECRET']
    security_s.callback_url = state.app.config['AUTH0_CALLBACK_URL']

    try:
        security_s.get_jwks()  # prefetch jwks
    except AppError:
        logger.info('could not prefetch jwks')


@babel.localeselector
def locale_selector():
    if 'lang' in request.args:
        session['lang'] = request.args.get('lang')

    return (
        session.get('lang', None) or
        request.accept_languages.best_match(['he', 'en', 'ar'])
    )


@core_bp.app_context_processor
def locale_context_processor():
    return dict(locale=get_locale())


@login_manager.user_loader
def load_user(user_id):
    try:
        return security_s.authenticate(user_id)
    except JWTExpiredError:
        return None
    except AppError:
        logger.exception('could not authenticate, please take a look')
        return abort(500)


@core_bp.route('/callback')
def callback_handling():
    code = request.args.get('code')
    state = request.args.get('state')
    jwt = security_s.fetch_jwt(code)
    user = security_s.authenticate(jwt)
    login_user(user, remember=True)
    return redirect(state)


@core_bp.before_app_request
def logout_before_app_request():
    if request.path == '/' and 'logout' in request.args:
        logout_user()


@core_bp.app_errorhandler(401)
def errorhandler_401(error):
    return render_template('401.html', next=request.path)


@core_bp.app_errorhandler(403)
def errorhandler_403(error):
    return render_template('403.html')


@core_bp.app_errorhandler(404)
def errorhandler_404(error):
    return render_template('404.html')


@core_bp.app_errorhandler(500)
def errorhandler_500(error):
    return render_template('500.html')
