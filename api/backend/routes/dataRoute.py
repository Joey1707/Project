from flask import Blueprint, Flask, jsonify, request
from backend.app import MYSQLdb
from backend.config import ConfigMongo
import datetime
from functools import wraps
import jwt as pyjwt
from backend.models.userModels import User
import os
from dotenv import load_dotenv
# from bson.objectid import ObjectId

load_dotenv()
data = Blueprint('dataRoute', __name__)
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

def token_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')  # Get the token from the Authorization header
        if not token:
            return jsonify({'alert': 'Token is missing'}), 401

        try:
            token = token.split(" ")[1]
            payload = pyjwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            email = payload.get('email')  # Accessing email from the payload

        except pyjwt.ExpiredSignatureError:
            return jsonify({'alert': 'Token expired'}), 401
        except pyjwt.InvalidTokenError:
            return jsonify({'alert': 'Invalid token'}), 401

        # You can now use the email to authenticate or authorize the user
        print(f"Authenticated user Email: {email}")

        return func(email=email,*args, **kwargs)

    return decorated

@data.route('/mongoUser', methods=['POST'])
@token_required
def create_or_update_user(email):
    MYSQLUser = User.query.filter_by(email=email).first()
    
    try:
        # Get database reference
        db = ConfigMongo.get_client()
        collection = db.people

        # User data to insert or update
        user_data = {
            'name': 'adam', 
            'lastname': 'smith', 
            'MYSQL_ID': MYSQLUser.id
        }

        # Update if exists, otherwise insert
        db_response = collection.update_one(
            {"MYSQL_ID": MYSQLUser.id},  # Search filter
            {"$set": user_data},         # Data to set/update
            upsert=True                  # Insert if no match found
        )
        
        return jsonify({
            "message": "User created or updated",
            "mimetype": "application/json",
            "mySQL_ID": MYSQLUser.id,
            "matched_count": db_response.matched_count,
            "modified_count": db_response.modified_count
        }), 200

    except Exception as ex:
        return jsonify({"error": str(ex)})


@data.route("/mongodbUser", methods=["GET"])
def get_some_users():
    MONGOdb = ConfigMongo.get_client()
    try:
        users = list(MONGOdb.people.find())
        for user in users:
            user["_id"] = str(user["_id"])
        return jsonify(users)
    except Exception as ex:
        print("Error fetching users:", ex)
        return jsonify({"error": str(ex)}), 500


