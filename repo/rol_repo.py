from dao.rol_dao import Rol
from database.db import db

def get_role_by_name(role_name):
    """Devuelve un rol por su nombre"""
    return Rol.query.filter_by(role_name=role_name).first()

def create_role(role_name):
    """Crea un rol si no existe"""
    existing_role = get_role_by_name(role_name)
    if not existing_role:
        role = Rol(role_name)
        db.session.add(role)
        db.session.commit()
        return role
    return existing_role