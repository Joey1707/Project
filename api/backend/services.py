import pandas as pd
from backend.config import ConfigMongo

client = ConfigMongo.get_client()
db = client["Project"]  
collection = db["newUser"]  

def fetch_and_process_data():
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