from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from backend.config import ConfigMYSQL, ConfigMongo
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

MYSQLdb = SQLAlchemy()
migrate = Migrate()

# mongo_client = MongoClient(ConfigMongo)
# mongo_db = mongo_client["ProjectData"]
# user_collection = mongo_db["Data"]

def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigMYSQL)
    app.config.from_object(ConfigMongo)
    cors_origin = os.getenv("API_LINK_CORS", "").split(",")
    # Enable CORS
    CORS(app, 
         allow_headers=["Authorization", "Content-Type"],
         resources={r"/*": {"origins": cors_origin}}, 
         supports_credentials=True)
    # Initialize extensions
    MYSQLdb.init_app(app)
    migrate.init_app(app, MYSQLdb)

    # Import and register blueprints
    from backend.routes.authRoutes import auth
    from backend.routes.dataRoute import data
    app.register_blueprint(auth)
    app.register_blueprint(data)

    return app
