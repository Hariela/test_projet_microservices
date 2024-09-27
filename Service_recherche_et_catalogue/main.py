from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configurer la connexion à la même base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:@localhost/books_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modèle de livre (assurez-vous que cela correspond à ce que vous avez déjà)
class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)

# Route pour rechercher des livres
@app.route('/search', methods=['GET'])
def search_books():
    search_term = request.args.get('query')
    books = Book.query.filter(Book.title.like(f'%{search_term}%')).all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books])

# Route pour lister tous les livres
@app.route('/books', methods=['GET'])
def get_books():
    books = Book.query.all()
    return jsonify([{'id': book.id, 'title': book.title, 'author': book.author} for book in books])

if __name__ == '__main__':
    app.run(debug=True, port=5001)
