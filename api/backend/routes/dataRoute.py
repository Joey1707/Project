from flask import Blueprint, Flask, jsonify, request
from backend.config import ConfigMongo
from backend.models.userModels import User
import os
from dotenv import load_dotenv
from backend.services import token_required
import pandas as pd
from backend.models.userModels import User
from datetime import datetime, timezone
from bson import ObjectId

app = Flask(__name__)
client = ConfigMongo.get_client()
db = client["Project"]  

load_dotenv()
data = Blueprint('dataRoute', __name__)
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

#reading collection
from datetime import datetime
from flask import request, jsonify
from bson import ObjectId
import pandas as pd

@data.route("/userData", methods=["GET"])
@token_required
def get_data(email):
    # Fetch the user from MySQL
    MYSQLUser = User.query.filter_by(email=email).first()
    if not MYSQLUser:
        return jsonify({"error": "user not found"}), 404

    # Access the MongoDB collection
    collection = db["user_data"]

    # Initialize the base filter with MYSQL_ID
    filters = {"MYSQL_ID": MYSQLUser.id}

    # Get query parameters
    timestamp_str = request.args.get("timestamp")
    userID = request.args.get("upload_id")
    MYSQLID_str = request.args.get("MYSQL_ID")

    # Check if at least one parameter is provided
    if not timestamp_str and not userID and not MYSQLID_str:
        return jsonify ({"error": "At least one parameter is required"}), 400
    
    if timestamp_str and not userID and not MYSQLID_str:
        return jsonify({"error": "timestamp must be paired with upload_id or MYSQL_ID"}), 400
    # Add upload_id to the filter if provided
    if userID:
        try:
            filters["upload_id"] = str(ObjectId(userID))  # Validate and use the provided upload_id
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": "Invalid upload_id format"}), 400

    # Add timestamp to the filter if provided
    if timestamp_str:
        try:
            # Remove the time zone offset (e.g., "+00:00") if present
            if "+" in timestamp_str:
                timestamp_str = timestamp_str.split("+")[0]

            # Parse the timestamp string into a datetime object
            target_timestamp = datetime.fromisoformat(timestamp_str)
            filters["timestamp"] = target_timestamp
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": "Invalid timestamp format. Use ISO format (e.g., 2025-02-27T19:54:13.710)"}), 400

    # Add MYSQL_ID to the filter if provided (override the base filter)
    if MYSQLID_str:
        try:
            filters["MYSQL_ID"] = int(MYSQLID_str)  # Validate and use the provided MYSQL_ID
        except Exception as e:
            print("Error:", e)
            return jsonify({"error": "Invalid MYSQL_ID format"}), 400

    # Query the MongoDB collection with the combined filters
    results = list(collection.find(filters, {"_id": 0}))

    # Check if any results were found
    if not results:
        return jsonify({"error": "No data found for the given criteria"}), 404

    # Convert results to a DataFrame for additional processing (if needed)
    df = pd.DataFrame(results)

    # Convert the "Date" column to a string format if it exists
    if "Date" in df.columns and not df["Date"].isnull().all():
        df["Date"] = pd.to_datetime(df["Date"], errors="coerce").fillna("").astype(str)

    # Debugging: Print database and collection names
    print("Database name:", db.name)
    print("Collection name:", collection.name)

    # Return the results as JSON
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

        # Generate a unique upload_id
        upload_id = str(ObjectId())  # Generate upload_id before inserting metadata

        timestamp = datetime.now(timezone.utc).replace(tzinfo=None)
        for user_data in user_data_list:
            user_data["MYSQL_ID"] = MYSQLUser.id
            user_data["timestamp"] = timestamp
            user_data["upload_id"] = upload_id  # Use upload_id instead of upload_count

        collection = db["user_data"]
        collection.insert_many(user_data_list)

        user_uploads = db["user_uploads"]
        upload_info = user_uploads.find_one_and_update(
            {"MYSQL_ID": MYSQLUser.id},
            {"$inc": {"upload_count": 1}},
            upsert=True,
            return_document=True
        )

        upload_count = upload_info["upload_count"]

        user_uploads.insert_one({
            "MYSQL_ID": MYSQLUser.id,
            "upload_id": upload_id,
            "upload_count": upload_count,
            "data_count": len(user_data_list),
            "timestamp": timestamp,
            "status": True
        })

        return jsonify({
            "message": "Data imported successfully",
            "upload_id": upload_id
        }), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

@data.route("/deletingData", methods=["DELETE"])
@token_required
def delete_data(email):
    try:
        MYSQLUser = User.query.filter_by(email=email).first()
        if not MYSQLUser:
            return jsonify({"error": "user not found"}), 404

        collection = db["user_data"]
        user_uploads = db["user_uploads"]

        # Get query parameters for selective deletion
        timestamp_str = request.args.get("timestamp")
        userID = request.args.get("upload_id")

        # Build the filter based on the provided query parameters
        filters = {"MYSQL_ID": MYSQLUser.id}  # Always filter by user ID

        if userID:
            try:
                # Validate and use the provided userID
                filters["upload_id"] = str(ObjectId(userID))  # Use the provided upload_id
            except Exception as e:
                print("Error:", e)
                return jsonify({"error": "Invalid upload_id format"}), 400

        if timestamp_str:
            try:
                # Remove the time zone offset (e.g., "+00:00") if present
                if "+" in timestamp_str:
                    timestamp_str = timestamp_str.split("+")[0]

                # Parse the timestamp string into a datetime object
                target_timestamp = datetime.fromisoformat(timestamp_str)
                filters["timestamp"] = target_timestamp
            except Exception as e:
                print("Error:", e)
                return jsonify({"error": "Invalid timestamp format. Use ISO format (e.g., 2025-02-27T19:54:13.710)"}), 400

        # Delete documents matching the filter
        result = collection.delete_many(filters)

        # Update the upload_count in user_uploads if documents were deleted
        if result.deleted_count > 0:
            user_uploads.update_one(
                {"MYSQL_ID": MYSQLUser.id},
                {"$inc": {"upload_count": -1}}
            )
            if userID and timestamp_str:
                user_uploads.update_one(
                    {"MYSQL_ID": MYSQLUser.id, "upload_id": userID},
                    {"$set": {"status": False}},
                )

        # Check if any documents were deleted
        if result.deleted_count == 0:
            return jsonify({"error": "No data found for the given criteria"}), 404

        return jsonify({"message": f"Deleted {result.deleted_count} documents"}), 200

    except Exception as e:
        print("Error:", e)
        return jsonify({"error": "Internal server error"}), 500

@data.route("/uploadCount", methods=["GET"])
@token_required
def get_upload_count(email):
    MYSQLUser = User.query.filter_by(email=email).first()
    if not MYSQLUser:
        return jsonify({"error": "user not found"}), 404
    
    user_uploads = db["user_uploads"]
    upload_info = user_uploads.find_one({"MYSQL_ID": MYSQLUser.id})

    if not upload_info:
        return jsonify({"upload count": 0}), 200

    return jsonify({"upload_count": upload_info["upload_count"]}),200




###########################################################################

# @data.route('/testingDataBase_Updating', methods=['POST'])
# @token_required
# def create_or_update_user(id):
#     MYSQLUser = User.query.filter_by(id=id).first()
    
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
    
# @data.route("/testingDataBase_InsertingUser", methods=["POST"])
# def insert_user():
 
#     try:
#         user_data = {
#             'name': 'adam',
#             'lastname': 'smith'
#         }

#         db_response = collection.insert_one(user_data)
        
#         print(db_response.inserted_id)
#         print(f"Using database: {db.name}")
#         print(f"Using collection: {collection.name}")
        
#         return jsonify({
#                 "message": "User created successfully",
#                 "id": str(db_response.inserted_id)  # Convert ObjectId to string for JSON serialization
#             }), 200

#     except Exception as ex:
#         print(ex)
#         return Response(
#             response=({"error": str(ex)}),
#             status=500,
#             mimetype="application/json"
#         )

# @data.route("/mongodbUser", methods=["GET"])
# def get_some_users():
#     MONGOdb = ConfigMongo.get_client()
#     try:
#         users = list(MONGOdb.people.find())
#         for user in users:
#             user["_id"] = str(user["_id"])
#         return jsonify(users)
#     except Exception as ex:
#         print("Error fetching users:", ex)
#         return jsonify({"error": str(ex)}), 500



