import pandas as pd
from pymongo import MongoClient
import glob
import os

MONGODB_URI="mongodb+srv://boubakerelkilani_db_user:0xuDKcxBZxyobpHW@cluster0.mwp48qy.mongodb.net"
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
