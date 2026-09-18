import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
client = MongoClient(MONGODB_URI)
db = client["OLIST"]

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

print("\n========== EXPLAIN SANS INDEX ==========\n")

sans_index = db.command(
    "explain",
    {
        "aggregate": "orders",
        "pipeline": pipeline,
        "cursor": {}
    },
    verbosity="executionStats"
)

stats_sans = sans_index["stages"][0]["$cursor"]["executionStats"]

print("Documents examinés :", stats_sans["totalDocsExamined"])
print("Clés examinées :", stats_sans["totalKeysExamined"])
print("Documents retournés :", stats_sans["nReturned"])
print("Temps :", stats_sans["executionTimeMillis"], "ms")

print("\n========== CREATION DES INDEX ==========\n")

if "order_status_1" not in db.orders.index_information():
    db.orders.create_index("order_status")

if "customer_id_1" not in db.customers.index_information():
    db.customers.create_index("customer_id")

if "order_id_1" not in db.order_items.index_information():
    db.order_items.create_index("order_id")

if "product_id_1" not in db.products.index_information():
    db.products.create_index("product_id")

if "order_id_1" not in db.order_reviews.index_information():
    db.order_reviews.create_index("order_id")

print("Index vérifiés.")

print("\n========== EXPLAIN AVEC INDEX ==========\n")

avec_index = db.command(
    "explain",
    {
        "aggregate": "orders",
        "pipeline": pipeline,
        "cursor": {}
    },
    verbosity="executionStats"
)

stats_avec = avec_index["stages"][0]["$cursor"]["executionStats"]

print("Documents examinés :", stats_avec["totalDocsExamined"])
print("Clés examinées :", stats_avec["totalKeysExamined"])
print("Documents retournés :", stats_avec["nReturned"])
print("Temps :", stats_avec["executionTimeMillis"], "ms")

print("\n========== INDEX UTILISES ==========\n")

for stage in avec_index["stages"]:
    if "$lookup" in stage:
        print(
            stage["$lookup"]["from"],
            ":",
            stage["$lookup"].get("indexesUsed", [])
        )