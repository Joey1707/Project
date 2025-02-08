from flask import Blueprint, Flask, jsonify
from backend.app import db
from backend.config import ConfigMongo
import datetime

# Replace with your actual credentials

data = Blueprint('dataRoute', __name__)
app = Flask(__name__)

@data.route('/mongoUser', methods=['POST'])
def create_user():
    try:
        # Get database reference
        db = ConfigMongo.get_client()
        
        # Insert user data into 'people' collection
        user = {'name': 'adam', 'lastname': 'smith'}
        db_response = db.people.insert_one(user)
    
        return jsonify({"message": "User created", 
                        "mimetype": "application/json",
                        "id": str(db_response.inserted_id)})

    except Exception as ex:
        return jsonify({"error": str(ex)})