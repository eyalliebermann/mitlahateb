from flask import Flask
from flask.globals import current_app
from flask.helpers import send_from_directory
from flask_env import MetaFlaskEnv

from app.admin import admin_bp
from app.core.blueprint import core_bp
from app.extensions import db, migrate
from app.onboarding import onboarding_bp

app = Flask(__name__, static_url_path='')


class FlaskConfig(object):
    __metaclass__ = MetaFlaskEnv


with app.app_context():
    current_app.config.from_object(FlaskConfig)

    if not ('SQLALCHEMY_DATABASE_URI' in current_app.config):
        current_app.config['SQLALCHEMY_DATABASE_URI'] = current_app.config['DATABASE_URL']

    db.init_app(app)
    migrate.init_app(app, db)
    app.register_blueprint(core_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(admin_bp)


@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('./static', filename)
