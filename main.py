from flask import Flask, request, jsonify
from flask_mysqldb import MySQL


app = Flask(__name__)

# Configuration de la base de données
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'books_service'


mysql = MySQL(app)
print(mysql)
cur = mysql.connection.cursor()
print(cur)

# Route pour ajouter un livre
@app.route('/books', methods=['POST'])
def add_book():
    data = request.get_json()
    title = data['title']
    author = data['author']
    published_date = data.get('published_date')
    isbn = data['isbn']

    cursor = mysql.connection.cursor()
    cursor.execute('INSERT INTO books (title, author, published_date, isbn) VALUES (%s, %s, %s, %s)',
                   (title, author, published_date, isbn))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Book added successfully!'}), 201

# Route pour récupérer tous les livres
@app.route('/books', methods=['GET'])
def get_books():
    cursor = mysql.connection.cursor()
    print(cursor)
    return "1"

# Route pour modifier un livre
@app.route('/books/<int:id>', methods=['PUT'])
def update_book(id):
    data = request.get_json()
    cursor = mysql.connection.cursor()
    cursor.execute('UPDATE books SET title = %s, author = %s, published_date = %s, isbn = %s WHERE id = %s',
                   (data['title'], data['author'], data.get('published_date'), data['isbn'], id))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Book updated successfully!'}), 200

# Route pour supprimer un livre
@app.route('/books/<int:id>', methods=['DELETE'])
def delete_book(id):
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM books WHERE id = %s', (id,))
    mysql.connection.commit()
    cursor.close()
    return jsonify({'message': 'Book deleted successfully!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
