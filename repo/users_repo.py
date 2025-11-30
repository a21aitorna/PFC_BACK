from dao.persona_dao import Persona
from database.db import db
from sqlalchemy import or_

def get_user_by_user_id(id_user):
    """Obtener usuario por su id"""
    user = Persona.query.filter_by(id_user=id_user).first()
    return user

def get_user_by_username(username):
    """Obtener usuario por su nombre de usuario"""
    user = Persona.query.filter_by(username=username).first()
    return user

def save_user(person):
    """Guarda un usuario en la base de datos"""
    try:
        db.session.add(person)
        db.session.commit()
        return person
    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar usuario: {e}")
        raise e
    
def get_security_question_by_username(username):
    """Obtener la pregunta de seguridad del usuario"""
    user = get_user_by_username(username)
    return user.security_question

def get_answer_by_username(username):
    """Obtener la respuesta del usuario"""
    user = get_user_by_username(username)
    return user.answer

def get_password_by_username(username):
    """Obtener la contraseña del usuario"""
    user = get_user_by_username(username)
    return user.password

def update_user_password(username, hashed_password):
    """Actualizar la contraseña del usuario"""
    user = get_user_by_username(username)
    user.password = hashed_password
    # db.session.flush() -> se escribe en base de datos pero no confirma el cambio
    db.session.commit()
    return user

def get_user_library_name(id_user):
    """Obtener el nombre de la librería del usuario"""
    user = get_user_by_user_id(id_user)
    return user.library_name

def get_users_or_libraries(searched_text, limit=5):
    """Busca usuario o nombre de librería"""
    if not searched_text:
        return []
    userSearch = Persona.query.filter(or_(
        Persona.username.ilike(f"%{searched_text}%"),
        Persona.library_name.ilike(f"%{searched_text}%")
        ),
        Persona.is_erased == False
    ).limit(limit).all()
    return userSearch
    