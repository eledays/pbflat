from config import Config

from flask import Flask


def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    from app.routes import bp as routes_bp
    from app.auth import bp as auth_bp
    app.register_blueprint(routes_bp)
    app.register_blueprint(auth_bp)

    from app.db import init_db, get_any_user, create_user
    init_db()

    if not get_any_user():
        create_user('user')

    return app
