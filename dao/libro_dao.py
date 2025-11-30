from database.db import db

class Libro(db.Model):
    __tablename__ = 'book'
    
    id_book = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    cover = db.Column(db.String(1024), nullable=False)
    file = db.Column(db.String(1024), nullable=False)
    
    def __init__(self, title, author, cover, file):
        self.title = title
        self.author = author
        self.cover = cover
        self.file = file
        
    def as_dict(self):
        return {
            'id_book': self.id_book,
            'title': self.title,
            'author': self.author
        }