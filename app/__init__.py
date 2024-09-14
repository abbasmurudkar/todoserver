import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Load configuration from object
    app.config.from_object('app.config.Config')

    # Set database URL from environment variable
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register routes
    with app.app_context():
        from . import routes
        db.create_all()

    return app
