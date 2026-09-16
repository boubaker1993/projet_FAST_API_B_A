import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pymongo import MongoClient

load_dotenv()

app = FastAPI()

MONGODB_URI = os.getenv("MONGODB_URI")

client = MongoClient(MONGODB_URI)
db = client["OLIST"]


@app.get("/produits-review-olist")
def produits_review_olist():
    pipeline = [
        {"$match": {"order_status": "delivered"}},

        {"$lookup": {
            "from": "customers",
            "localField": "customer_id",
            "foreignField": "customer_id",
            "as": "customer"
        }},

        {"$unwind": "$customer"},

        {"$lookup": {
            "from": "order_items",
            "localField": "order_id",
            "foreignField": "order_id",
            "as": "items"
        }},

        {"$unwind": "$items"},

        {"$lookup": {
            "from": "products",
            "localField": "items.product_id",
            "foreignField": "product_id",
            "as": "product"
        }},

        {"$unwind": "$product"},

        {"$lookup": {
            "from": "order_reviews",
            "localField": "order_id",
            "foreignField": "order_id",
            "as": "review"
        }},

        {"$unwind": "$review"},

        {"$project": {
            "_id": 0,
            "order_id": 1,
            "customer_id": 1,
            "zipcode": "$customer.customer_zip_code_prefix",
            "product_id": "$items.product_id",
            "product_category": "$product.product_category_name",
            "price": "$items.price",
            "review_score": "$review.review_score"
        }},

        {"$limit": 10}
    ]

    return list(db["orders"].aggregate(pipeline))