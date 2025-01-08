from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)

# MongoDB URI configuration
app.config["MONGO_URI"] = "mongodb://localhost:27017/book_management"
mongo = PyMongo(app)
books_collection = mongo.db.books

# Home route
@app.route('/')
def index():
    return "Welcome to the Book Management System!"

# 1. Create a new book (POST request)
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()

    if not data.get('title') or not data.get('author'):
        return jsonify({"error": "Missing required fields: 'title' and 'author'"}), 400

    book = {
        "title": data["title"],
        "author": data["author"],
        "published_year": data.get("published_year"),
        "genre": data.get("genre"),
    }

    # Insert the new book into the database
    result = books_collection.insert_one(book)
    return jsonify({"message": "Book added successfully", "book_id": str(result.inserted_id)}), 201

# 2. Retrieve all books (GET request)
@app.route('/books', methods=['GET'])
def get_books():
    books = books_collection.find()

    books_list = []
    for book in books:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string for JSON response
        books_list.append(book)

    return jsonify(books_list), 200

# 3. Retrieve a specific book by ID (GET request)
@app.route('/books/<book_id>', methods=['GET'])
def get_book(book_id):
    book = books_collection.find_one({"_id": ObjectId(book_id)})

    if book:
        book["_id"] = str(book["_id"])  # Convert ObjectId to string for JSON response
        return jsonify(book), 200
    else:
        return jsonify({"error": "Book not found"}), 404

# 4. Update book details (PUT request)
@app.route('/books/<book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()

    updated_data = {}
    if data.get("title"):
        updated_data["title"] = data["title"]
    if data.get("author"):
        updated_data["author"] = data["author"]
    if data.get("published_year"):
        updated_data["published_year"] = data["published_year"]
    if data.get("genre"):
        updated_data["genre"] = data["genre"]

    if not updated_data:
        return jsonify({"error": "No fields to update"}), 400

    result = books_collection.update_one(
        {"_id": ObjectId(book_id)}, 
        {"$set": updated_data}
    )

    if result.matched_count > 0:
        return jsonify({"message": "Book updated successfully"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404

# 5. Delete a book (DELETE request)
@app.route('/books/<book_id>', methods=['DELETE'])
def delete_book(book_id):
    result = books_collection.delete_one({"_id": ObjectId(book_id)})

    if result.deleted_count > 0:
        return jsonify({"message": "Book deleted successfully"}), 200
    else:
        return jsonify({"error": "Book not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)