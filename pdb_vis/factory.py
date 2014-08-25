import logging

from flask import Flask


_log = logging.getLogger(__name__)


def create_app(settings=None):
    _log.info("Creating app")

    app = Flask(__name__, static_folder='frontend/static',
                template_folder='frontend/templates')
    app.config.from_object('pdb_vis.default_settings')
    if settings:
        app.config.update(settings)
    else:  # pragma: no cover
        app.config.from_envvar('PDB_VIS_SETTINGS')  # pragma: no cover

    # Set the maximum content length to 150MB. This is to allow large PDB files
    # to be sent in post requests. The largest PDB file found to date is 109MB
    # in size.
    app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024 * 150

    # Ignore Flask's built-in logging
    # app.logger is accessed here so Flask tries to create it
    app.logger_name = "nowhere"
    app.logger

    # Use ProxyFix to correct URL's when redirecting.
    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

    # Initialise extensions
    from pdb_vis import toolbar
    toolbar.init_app(app)

    # Register blueprints
    from pdb_vis.frontend.dashboard.views import bp as dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app
