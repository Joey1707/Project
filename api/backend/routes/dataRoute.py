from flask import Blueprint, Flask, jsonify, Response, request
from backend.app import MYSQLdb
from backend.config import ConfigMongo
from backend.models.userModels import User
import os
from dotenv import load_dotenv
from backend.services import fetch_and_process_data, token_required, input_data, checking_correct_filetype
import pandas as pd

app = Flask(__name__)
client = ConfigMongo.get_client()
db = client["Project"]  

load_dotenv()
data = Blueprint('dataRoute', __name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

#reading collection
@data.route("/userData", methods=["POST"])
@token_required
def get_data(id):
    MYSQLUser = User.query.filter_by(id=id).first()
    collection = db["User", MYSQLUser.id]  
    df = fetch_and_process_data()

    print("Database name:", db.name)  
    print("Collection name:", collection.name)  
     
    if df is None:
        return jsonify({"error": "No data found in MongoDB collection."}), 404  # Use 404 for "Not Found"
    return jsonify(df.to_dict(orient="records")), 200

#inputing data to a collection
@data.route("/inputingData", methods=["POST"])
@token_required
def inputing_data(email):
    try:
        MYSQLUser = User.query.filter_by(email=email).first()
        if not MYSQLUser:
            return jsonify({"error": "user not found"}), 404

        # Ensure a file is provided
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]

        if file.filename == "":
            return jsonify({"error": "No selected file"}), 400
        
        # Check file extension
        ALLOWED_EXTENSIONS = {"csv", "xlsx"}
        file_extension = file.filename.rsplit(".", 1)[1].lower()

        if file_extension not in ALLOWED_EXTENSIONS:
            return jsonify({"error": "Invalid file format. Only CSV and Excel are allowed"}), 400

        # Read the file
        if file_extension == "csv":
            df = pd.read_csv(file)
        elif file_extension == "xlsx":
            df = pd.read_excel(file)

        # Convert DataFrame to list of dictionaries
        user_data_list = df.to_dict(orient="records")

        # Attach MYSQL user ID to each record
        for user_data in user_data_list:
            user_data["MYSQL_ID"] = MYSQLUser.id

        collection = db["user_data"]

        # Insert data into MongoDB
        db_response = collection.insert_many(user_data_list)

        return jsonify({
            "message": "Data imported successfully",
            "inserted_ids": [str(id) for id in db_response.inserted_ids]
        }), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500


@data.route('/testingDataBase_Updating', methods=['POST'])
@token_required
def create_or_update_user(id):
    MYSQLUser = User.query.filter_by(id=id).first()
    
    try:
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
    
@data.route("/testingDataBase_InsertingUser", methods=["POST"])
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



