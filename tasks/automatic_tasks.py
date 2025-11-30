from datetime import date, timedelta
from database.db import db
from dao.persona_dao import Persona
from repo.books_repo import delete_book

def automatic_unblock_users():
    """Método para desbloquear usuarios automáticamente tras 3 días"""
    today = date.today()
    three_days_ago = today - timedelta(days=3)
    
    expired_users = Persona.query.filter(Persona.is_blocked==True, Persona.block_date<= three_days_ago).all()
    for user in expired_users:
        user.is_blocked = False
        user.block_date = None

    if expired_users:
        db.session.commit()
    else:
        print("No había usuarios para desbloquear.")

def automatic_delete_users():
    """Método para borrar los usuarios una vez pasados 15 días"""
    today = date.today()
    fifteen_days_ago = today - timedelta(days=15)
    
    deleted_users = Persona.query.filter(
        Persona.is_erased == True,
        Persona.delete_date <= fifteen_days_ago
    ).all()
    
    for user in deleted_users:
        for uploaded in user.libros_subidos:
            delete_book(user.id_user, uploaded.book_id)
        
        db.session.delete(user)
    
    if deleted_users:
        db.session.commit()
    else:
        print("No había usuarios para borrar.")