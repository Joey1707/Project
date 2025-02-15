import pandas as pd
from backend.config import ConfigMongo
from functools import wraps
from flask import jsonify, request
import jwt as pyjwt
from flask import Flask
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# Secret Key for JWT
app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

def fetch_and_process_data(collection):
    try:
        data = list(collection.find({}, {"_id": 0}).limit(1))

        if not data:  
            print("No data found in MongoDB collection.")  
            return None

    except Exception as e:
        print("Error:", e)  
        return None

    # Convert data to DataFrame
    df = pd.DataFrame(data)
    print (df.head)

    if "Date" in df.columns:
        df["Date"] = pd.to_datetime(df["Date"])

    return df

def input_data(collection, user_data, MYSQLUser):
    try:
        if not user_data:
            return jsonify({"there's no data that can be inputed"}),400

        user_data["MYSQL_ID"] = MYSQLUser.id
        db_response = collection.insert_one(user_data)

        print(db_response.inserted_id)

        return jsonify({
            "message": "data imported succesfully", 
            "id" : str(db_response.inserted_id)
        }), 200
    
    except Exception as e:
        print ("error:", e)
        return jsonify({"error when inputing data, please try again"}), 500

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
        print(f"Authenticated user ID: {email}")

        return func(email=email,*args, **kwargs)

    return decorated