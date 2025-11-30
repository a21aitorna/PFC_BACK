from database.db import db
from datetime import datetime, timezone

class Reseña(db.Model):
    __tablename__ = 'review'

    id_review = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id_user'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('book.id_book'), nullable=False)
    review_text = db.Column(db.Text, nullable=False)
    book_rating = db.Column(db.Integer)
    creation_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    user = db.relationship('Persona', backref='reseñas', lazy=True)
    book = db.relationship('Libro', backref='reseñas', lazy=True)

    def __init__(self, user_id, book_id, review_text, book_rating, creation_date=None):
        self.user_id = user_id
        self.book_id = book_id
        self.review_text = review_text
        self.book_rating = book_rating
        self.creation_date = creation_date or datetime.now(timezone.utc)

    def as_dict(self):
        return{
            'id_review': self.id_review,
            'review_user_id': self.user_id,
            'review_user_username': self.user.username if self.user else None,
            'review_text': self.review_text,
            'book_rating': self.book_rating,
            'creation_date': self.creation_date
        }