from flask import Flask
from .routes import tasks_bp

def create_app(config=None):
    app = Flask(__name__, static_folder="../static")

    app.config["TESTING"] = False
    app.config["SECRET_KEY"] = "dev-secret-key"

    if config:
        app.config.update(config)

    app.register_blueprint(tasks_bp)

    return app
