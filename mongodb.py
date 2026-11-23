import os
from unittest import result
from pymongo import MongoClient
from dotenv import load_dotenv

from pymongo import MongoClient
uri = "mongodb+srv://wakanyileonard_db_user:<db_password>@opra.hgnplrc.mongodb.net/"
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Connected successfully")
    client.close()

except Exception as e:
    raise Exception(
        "The following error occurred: ", e)

load_dotenv()
MONGODB_URI = os.getenv("MONGODB_URI")
MONGODB_USERNAME = os.getenv("MONGODB_USERNAME")

client = MongoClient(MONGODB_URI)
client.admin.command('ping')
print("Pinged your deployment. You successfully connected to MongoDB!")

db = client['OPRA-AI']
customers = db['customers']
orders = db['orders']
products= db['products']
print(products)
print(orders)
print(customers)

product_list=[
    {
        "name": "MERCEDESS BENZ",
        "description": "This is a MERCEDESS BENZ",
        "price": 1000000,
        "quantity": 12,
        "available": True
    },
    {
        "name": "BMW",
        "description": "This is a BMW",
        "price": 200000,
    "quantity": 30,
    "available": True
},{
    "name": "TOYOTA",
    "description": "This is a TOYOTA",
    "price": 30000,
    "quantity": 25,
    "available": True
}
]
result = products.insert_many(product_list)
print(f"Inserted products with ids: {result.inserted_ids}")

available_products = products.find({"available": True})
for product in available_products:
    print(f"Product Name: {product['name']}, Description: {product['description']}, Price: {product['price']}, Quantity: {product['quantity']}")

