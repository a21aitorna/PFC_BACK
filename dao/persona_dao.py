from database.db import db

class Persona(db.Model):
    __tablename__ = 'user'

    id_user = db.Column(db.Integer, primary_key=True)
    id_role = db.Column(db.Integer, db.ForeignKey('role.id_role'), nullable=False)
    name = db.Column(db.String(50), nullable=False)
    surname = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    born_date = db.Column(db.Date, nullable=False)
    library_name = db.Column(db.String(100), nullable=False)
    is_blocked = db.Column(db.Boolean, default=False)
    is_erased = db.Column(db.Boolean, default=False)
    block_date = db.Column(db.Date)
    delete_date = db.Column(db.Date)
    security_question = db.Column(db.String(200), nullable=False)
    answer = db.Column(db.String(500), nullable=False)

    role = db.relationship('Rol', backref='usuarios', lazy=True)

    def __init__(self, id_role, name, surname, username, password, born_date, 
                 library_name, security_question, answer, 
                 is_blocked=False, is_erased=False, 
                 block_date=None, delete_date=None):
        self.id_role = id_role
        self.name = name
        self.surname = surname
        self.username = username
        self.password = password
        self.born_date = born_date
        self.library_name = library_name
        self.is_blocked = is_blocked
        self.is_erased = is_erased
        self.block_date = block_date
        self.delete_date = delete_date
        self.security_question = security_question
        self.answer = answer
        
    def as_dict(self):
        return {
            'id_user': self.id_user,
            'user_role_id': self.id_role,
            'user_role_name': self.role.role_name if self.role else None,
            'name': self.name,
            'surname': self.surname,
            'username': self.username,
            'born_date': self.born_date,
            'library_name': self.library_name,
            'is_blocked': self.is_blocked,
            'is_erased': self.is_erased,
            'block_date': self.block_date,
            'delete_date': self.delete_date,
            'security_question': self.security_question
        }
        
    def __repr__(self):
        return f"<Persona {self.username}>"
