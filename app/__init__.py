import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    load_dotenv()  
    app = Flask(__name__)
    CORS(app)


    app.config.from_object('app.config.Config')

  
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")

    
    db.init_app(app)
    migrate.init_app(app, db)

    
    with app.app_context():
        from . import routes
        db.create_all()

    return app
