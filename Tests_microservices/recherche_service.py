from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuration de la base de données MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/books_service'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Modèle Livre (repris du service de gestion des livres)
class Livre(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(100), nullable=False)
    auteur = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=True)
    genre = db.Column(db.String(50), nullable=False)


# Route de recherche de livres
@app.route('/search', methods=['GET'])
def search_books():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "Aucune requête de recherche fournie"}), 400

    # Filtrer par titre, auteur ou genre
    results = Livre.query.filter(
        (Livre.titre.like(f'%{query}%')) |
        (Livre.auteur.like(f'%{query}%')) |
        (Livre.genre.like(f'%{query}%'))
    ).all()

    if results:
        return jsonify([{
            "id": livre.id,
            "titre": livre.titre,
            "auteur": livre.auteur,
            "description": livre.description,
            "genre": livre.genre
        } for livre in results])
    else:
        return jsonify({"message": "Aucun livre trouvé"}), 404


# Route pour afficher tous les livres
@app.route('/catalog', methods=['GET'])
def list_books():
    books = Livre.query.all()
    return jsonify([{
        "id": livre.id,
        "titre": livre.titre,
        "auteur": livre.auteur,
        "description": livre.description,
        "genre": livre.genre
    } for livre in books])


if __name__ == '__main__':
    app.run(debug=True, port=5001)
