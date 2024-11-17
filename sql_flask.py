from flask import Flask, jsonify, request
from http import HTTPStatus
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Pupuwiwi001",
        database="lib_books"
    )

@app.route("/api/books", methods=["GET"])
def get_books():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    cursor.close()
    connection.close()
    return jsonify({"success": True, "data": books, "total": len(books)}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()
    cursor.close()
    connection.close()

    if book is None:
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND
    return jsonify({"success": True, "data": book}), HTTPStatus.OK

@app.route("/api/books", methods=["POST"])
def create_book():
    if not request.is_json:
        return (
            jsonify({"success": False, "error": "Content-type must be application/json"}),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()
    required_fields = ["title", "author", "year"]
    for field in required_fields:
        if field not in data:
            return (
                jsonify({"success": False, "error": f"Missing required field: {field}"}), 
                HTTPStatus.BAD_REQUEST,
            )
    
    connection = get_db_connection()
    cursor = connection.cursor()
    insert_query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (data["title"], data["author"], data["year"]))
    connection.commit()
    new_book_id = cursor.lastrowid
    cursor.close()
    connection.close()

    new_book = {
        "id": new_book_id,
        "title": data["title"],
        "author": data["author"],
        "year": data["year"],
    }
    return jsonify({"success": True, "data": new_book}), HTTPStatus.CREATED

@app.route("/api/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if book is None:
        cursor.close()
        connection.close()
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND

    if not request.is_json:
        return (
            jsonify({"success": False, "error": "Content-type must be application/json"}),
            HTTPStatus.BAD_REQUEST,
        )

    data = request.get_json()
    update_query = """
        UPDATE books
        SET title = %s, author = %s, year = %s
        WHERE id = %s
    """
    cursor.execute(
        update_query,
        (
            data.get("title", book["title"]),
            data.get("author", book["author"]),
            data.get("year", book["year"]),
            book_id,
        )
    )
    connection.commit()
    cursor.close()
    connection.close()

    updated_book = {
        "id": book_id,
        "title": data.get("title", book["title"]),
        "author": data.get("author", book["author"]),
        "year": data.get("year", book["year"]),
    }
    return jsonify({"success": True, "data": updated_book}), HTTPStatus.OK

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
    book = cursor.fetchone()

    if book is None:
        cursor.close()
        connection.close()
        return jsonify({"success": False, "error": "Book not found"}), HTTPStatus.NOT_FOUND

    delete_query = "DELETE FROM books WHERE id = %s"
    cursor.execute(delete_query, (book_id,))
    connection.commit()
    cursor.close()
    connection.close()
    return jsonify({"success": True, "message": f"Book with id {book_id} has been deleted"}), HTTPStatus.OK

@app.errorhandler(404)
def not_found(error):
    return jsonify({"success": False, "error": "Resource not found"}), HTTPStatus.NOT_FOUND

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"success": False, "error": "Internal Server Error"}), HTTPStatus.INTERNAL_SERVER_ERROR

if __name__ == '__main__':
    app.run(debug=True)
