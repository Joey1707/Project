from flask import Blueprint, Flask, jsonify, request, Response
from backend.app import MYSQLdb
from backend.config import ConfigMongo
import datetime
from functools import wraps
import jwt as pyjwt
from backend.models.userModels import User
import os
from dotenv import load_dotenv
from backend.services import fetch_and_process_data

# from bson.objectid import ObjectId

# client = ConfigMongo.get_client()
# db = client["Project"]  # Select database
# collection = db["UserData"]  # Select collection  # Ensure this points to the correct DB

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

# @data.route('/mongoUser', methods=['POST'])
# @token_required
# def create_or_update_user(email):
#     MYSQLUser = User.query.filter_by(email=email).first()
    
#     try:
#         # User data to insert or update
#         user_data = {
#             'name': 'adam', 
#             'lastname': 'smith', 
#             'MYSQL_ID': MYSQLUser.id
#         }

#         # Update if exists, otherwise insert
#         db_response = collection.update_one(
#             {"MYSQL_ID": MYSQLUser.id},  # Search filter
#             {"$set": user_data},         # Data to set/update
#             upsert=True                  # Insert if no match found
#         )
        
#         return jsonify({
#             "message": "User created or updated",
#             "mimetype": "application/json",
#             "mySQL_ID": MYSQLUser.id,
#             "matched_count": db_response.matched_count,
#             "modified_count": db_response.modified_count
#         }), 200

#     except Exception as ex:
#         return jsonify({"error": str(ex)})
    
@data.route("/insertingUser", methods=["POST"])
def insert_user():
 
    try:
        user_data = {
            'name': 'adam',
            'lastname': 'smith'
        }

        db_response = collection.insert_one(user_data)
        
        print(db_response.inserted_id)
        print(f"Using database: {db.name}")
        print(f"Using collection: {collection.name}")
        
        return jsonify({
                "message": "User created successfully",
                "id": str(db_response.inserted_id)  # Convert ObjectId to string for JSON serialization
            }), 200

    except Exception as ex:
        print(ex)
        return Response(
            response=({"error": str(ex)}),
            status=500,
            mimetype="application/json"
        )

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

@data.route("/userData", methods=["GET"])
def get_data():

    df = fetch_and_process_data()
    if df is None:
        return jsonify({"error": "No data found in MongoDB collection."}), 404  # Use 404 for "Not Found"
    return jsonify(df.to_dict(orient="records")), 200

# @data.route("/userData", methods=["GET"])
# def get_data():
#     client = ConfigMongo.get_client()
#     db = client["Project"]  # Select database
#     collection = db["newUser"]  # Select collection  # Ensure this points to the correct DB
#     try:
#     # Print the number of documents in the collection
#     # count = collection.count_documents({})
#     # print(f"Number of documents in collection: {count}")

#     # Fetch the first few documents
#         data = list(collection.find({}, {"_id": 0}).limit(1))
#         return jsonify({"data": data}), 200
 
#     except Exception as ex:
#         print(f"Error: {ex}")
#         return jsonify({"error": str(ex)}), 500