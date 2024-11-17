import mysql.connector

# Database configuration
db_config = {
    'user': 'root',  # Replace with your MySQL username
    'password': 'Pupuwiwi001',  # Replace with your MySQL password
    'host': 'localhost',
    'database': 'books'
}

def get_db_connection():
    """Creates a connection to the MySQL database."""
    try:
        cnx = mysql.connector.connect(**db_config)
        return cnx
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

def find_book(book_id):
    """Retrieves a single book from the database by its ID."""
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books WHERE id = %s", (book_id,))
        book = cursor.fetchone()
        cursor.close()
        cnx.close()
        return book
    return None

def get_all_books():
    """Fetches all books from the database."""
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor(dictionary=True)
        cursor.execute("SELECT * FROM books")
        books = cursor.fetchall()
        cursor.close()
        cnx.close()
        return books
    return []

def create_book(data):
    """Creates a new book in the database."""
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor()
        insert_query = "INSERT INTO books (title, author, year) VALUES (%s, %s, %s)"
        cursor.execute(insert_query, (data["title"], data["author"], data["year"]))
        cnx.commit()
        new_book_id = cursor.lastrowid
        cursor.close()
        cnx.close()
        return new_book_id
    return None

def update_book(book_id, data):
    """Updates a book record in the database."""
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor()
        update_query = """
        UPDATE books
        SET title = %s, author = %s, year = %s
        WHERE id = %s
        """
        cursor.execute(update_query, (data["title"], data["author"], data["year"], book_id))
        cnx.commit()
        cursor.close()
        cnx.close()
        return find_book(book_id)
    return None

def delete_book(book_id):
    """Deletes a book from the database."""
    cnx = get_db_connection()
    if cnx:
        cursor = cnx.cursor()
        delete_query = "DELETE FROM books WHERE id = %s"
        cursor.execute(delete_query, (book_id,))
        cnx.commit()
        cursor.close()
        cnx.close()
        return True
    return False
