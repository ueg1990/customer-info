"""
Main app module
"""
import logging
import sys

from flask import Flask, render_template

from app.config import ProdConfig
from app.customer import blueprint as customer_blueprint
from app.public import blueprint as public_blueprint
from app.extensions import db


def create_app(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_error_handlers(app)
    setup_logging(app)
    if config_object.DEBUG:
        with app.app_context():
            db.create_all()
    return app


def register_extensions(app):
    db.init_app(app)


def register_blueprints(app):
    app.register_blueprint(customer_blueprint)
    app.register_blueprint(public_blueprint)


def register_error_handlers(app):
    """Register error handlers."""
    def render_error(error):
        """Render error template."""
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template('errors/{0}.html'.format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)


def setup_logging(app):
    app.logger.addHandler(logging.StreamHandler(sys.stdout))
    app.logger.setLevel(logging.INFO)