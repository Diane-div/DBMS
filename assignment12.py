from flask import Flask, request, jsonify
from flask_cors import CORS
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
CORS(app)  # To allow frontend requests

# MongoDB connection (local)
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["mycollection"]

@app.route('/add', methods=['POST'])
def add_document():
    data = request.json
    result = collection.insert_one(data)
    return jsonify({'message': 'Document added', 'id': str(result.inserted_id)})

@app.route('/get', methods=['GET'])
def get_documents():
    docs = []
    for doc in collection.find():
        doc['_id'] = str(doc['_id'])
        docs.append(doc)
    return jsonify(docs)

@app.route('/edit/<id>', methods=['PUT'])
def edit_document(id):
    data = request.json
    result = collection.update_one({'_id': ObjectId(id)}, {'$set': data})
    return jsonify({'message': 'Document updated', 'modified_count': result.modified_count})

@app.route('/delete/<id>', methods=['DELETE'])
def delete_document(id):
    result = collection.delete_one({'_id': ObjectId(id)})
    return jsonify({'message': 'Document deleted', 'deleted_count': result.deleted_count})

if __name__ == '__main__':
    app.run(debug=True)
