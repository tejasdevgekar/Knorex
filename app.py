from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory data store (replace this with a database in a real-world scenario)
data_store = {
    1: {"id": 1, "name": "Item 1"},
    2: {"id": 2, "name": "Item 2"}
}

# Endpoint to retrieve all items
@app.route('/get', methods=['GET'])
def get_all_items():
    return jsonify(list(data_store.values()))

# Endpoint to retrieve a specific item by ID
@app.route('/get/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = data_store.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# Endpoint to create a new item
@app.route('/set', methods=['POST'])
def create_item():
    new_item = request.json
    item_id = max(data_store.keys()) + 1
    new_item['id'] = item_id
    data_store[item_id] = new_item
    return jsonify(new_item), 201

# Endpoint to update an existing item
@app.route('/set/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    item = data_store.get(item_id)
    if item:
        updated_item = request.json
        item.update(updated_item)
        return jsonify(item)
    else:
        return jsonify({"error": "Item not found"}), 404

# Endpoint to delete an existing item
@app.route('/delete/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = data_store.pop(item_id, None)
    if item:
        return jsonify({"message": "Item deleted successfully"})
    else:
        return jsonify({"error": "Item not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
