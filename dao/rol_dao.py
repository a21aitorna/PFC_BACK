from database.db import db


class Rol(db.Model):
    __tablename__ = 'role'

    id_role = db.Column(db.Integer, primary_key = True)
    role_name = db.Column(db.String(50), unique = True)

    def __init__(self, role_name):
        self.role_name = role_name

    def __repr__(self):
        return f'<Rol {self.role_name}>'
        