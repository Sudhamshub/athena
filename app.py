from flask import Flask, request, jsonify
import os
from pymongo import MongoClient

MONGO_URI = os.getenv("MONGO_URI")  
client = MongoClient(MONGO_URI)
db = client['todo_db']
collection = db['todo_items']

@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    data = request.get_json()
    item = {
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription")
    }
    result = collection.insert_one(item)
    return jsonify({"inserted_id": str(result.inserted_id), "status":"ok"})
