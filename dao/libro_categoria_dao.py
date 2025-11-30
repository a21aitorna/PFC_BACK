from database.db import db

class LibroCategoria(db.Model):
    __tablename__ = 'book_category'

    id_book_category = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id_book'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id_category'), nullable=False)

    book = db.relationship('Libro', backref='categorias_libro', lazy=True)
    category = db.relationship('Categoria', backref='categorias_libro', lazy=True)
