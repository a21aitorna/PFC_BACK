from database.db import db
from datetime import datetime, timezone

class LibroSubido(db.Model):
    __tablename__ = 'uploaded_book'
    
    id_uploaded_book = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id_book'), nullable=False)
    upload_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    rating = db.Column(db.Float, default=0.0)

    user = db.relationship('Persona', backref='libros_subidos', lazy=True)
    book = db.relationship('Libro', backref='subidas', lazy=True)

    def __init__(self, user_id, book_id, upload_date=None, rating=0.0):
        self.user_id = user_id
        self.book_id = book_id
        self.upload_date = upload_date or datetime.now(timezone.utc)
        self.rating = rating
        
    def as_dict(self):
        return {
            'id_uploaded_book': self.id_uploaded_book,
            'uploaded_book_user_id': self.user_id,
            'uploaded_book_user_name': self.user.username if self.user else None,
            'uploaded_book': self.book.as_dict() if self.book else None,
            'rating': self.rating
        }
    