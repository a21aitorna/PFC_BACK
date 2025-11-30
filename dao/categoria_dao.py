from database.db import db

class Categoria(db.Model):
    __tablename__ = 'category'

    id_category = db.Column(db.Integer, primary_key = True)
    category_name = db.Column(db.String(100))

    def __init__(self, category_name):
        self.category_name = category_name
