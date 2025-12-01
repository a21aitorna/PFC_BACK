from flask import jsonify
from dao.persona_dao import Persona
from dao.rol_dao import Rol
from datetime import datetime, timedelta
from database.db import db

def get_all_not_admin_users():
    """Conseguir todos los usuarios de la aplicación que no sean admin"""
    users = Persona.query.join(Rol).filter(Rol.role_name != 'Admin').all()
    return users

def block_user(user):
    """Bloquea un usuario"""
    
    if not user:
        return None
    
    user.is_blocked = True
    user.block_date = datetime.now().date()
    
    db.session.commit()
    return user

def unblock_user(id_user):
    """Rectifica el bloqueo"""
    user = Persona.query.get(id_user)
    
    if not user:
        return None
    user.is_blocked = False
    user.block_date = None
    
    db.session.commit()
    return user

def auto_unblock_user(user):
    """Desbloquea el usuario automáticamente tras 3 días"""
    if user.is_blocked and user.block_date:
        unblock_date = user.block_date + timedelta(days=3)
        today = datetime.now().date()
        if today > unblock_date:
            user.is_blocked = False
            user.block_date = None
            db.session.commit()
    return user        
    
def delete_user(user):
    """Elimina el usuario"""    
    if not user:
        return None
    user.is_erased =  True
    user.delete_date = datetime.now().date()
    
    db.session.commit()
    return user

def rectify_delete_user(id_user):
    """Rectifica la eliminación del usuario dentro de los 15 días"""
    user = Persona.query.get(id_user)
    
    if not user:
        return None
    user.is_erased = False
    user.delete_date = None
    
    db.session.commit()
    return user