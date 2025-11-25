from flask import Flask, request, jsonify
import os
import uuid
import hashlib
from pymongo import MongoClient

app = Flask(__name__)

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["todo_db"]
collection = db["todo_items"]

@app.route('/submittodoitem', methods=['POST'])
def submittodoitem():
    data = request.get_json()

    item_uuid = data.get("itemUuid") or str(uuid.uuid4())
    item_hash = data.get("itemHash") or hashlib.sha256(
        (data.get("itemName") + data.get("itemDescription")).encode()
    ).hexdigest()

    item = {
        "itemId": data.get("itemId"),
        "itemUuid": item_uuid,
        "itemHash": item_hash,
        "itemName": data.get("itemName"),
        "itemDescription": data.get("itemDescription")
    }

    result = collection.insert_one(item)

    return jsonify({
        "inserted_id": str(result.inserted_id),
        "status": "ok"
    })

if __name__ == "__main__":
    app.run(debug=True)
