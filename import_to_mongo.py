import pandas as pd
from pymongo import MongoClient
import glob
import os
from dotenv import load_dotenv
MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
client.drop_database("OLIST")
db = client["OLIST"]


files = glob.glob(
    "data/*.csv"
)

for file in files:

    df = pd.read_csv(file)
    filename = os.path.basename(file)
    collection_name = filename.replace("olist_", "").replace("_dataset", "").replace(".csv", "")
    collection = db[collection_name]
    data = df.to_dict("records")
    result = collection.insert_many(data)
    print(f"{len(result.inserted_ids)} documents insérés dans la collection '{collection_name}'.")
