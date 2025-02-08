from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from backend.config import ConfigMYSQL, ConfigMongo
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()

# mongo_client = MongoClient(ConfigMongo)
# mongo_db = mongo_client["ProjectData"]
# user_collection = mongo_db["Data"]

def create_app():
    app = Flask(__name__)
    app.config.from_object(ConfigMYSQL)
    app.config.from_object(ConfigMongo)

    # Enable CORS
    CORS(app, 
         allow_headers=["Authorization", "Content-Type"], 
         resources={r"/*": {"origins": ["https://project-4v2b.vercel.app", "http://localhost:5173", "http://127.0.0.1:5174"]}}, 
         supports_credentials=True)
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Import and register blueprints
    from backend.routes.authRoutes import auth
    from backend.routes.dataRoute import data
    app.register_blueprint(auth)
    app.register_blueprint(data)

    return app
