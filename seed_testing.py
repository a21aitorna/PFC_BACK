from datetime import date
from werkzeug.security import generate_password_hash
from repo.users_repo import save_user, get_user_by_username
from dao.persona_dao import Persona

def seed_block_user():
    """Crea un usuario para tests de bloqueo"""
    existing_user = get_user_by_username("UserBlock")
    if not existing_user:
        user = Persona(
            id_role=2,
            name="UserBlock",
            surname="User",
            username = "UserBlock",
            password = generate_password_hash("TestUser123.."),
            born_date=date(1999,9,3),
            library_name="Block user",
            security_question="UserBlock",
            answer = generate_password_hash("UserBlock")
        )
        save_user(user)
        
def seed_delete_user():
    """Crea un usuario para tests de eliminación"""
    existing_user = get_user_by_username("UserDelete")
    if not existing_user:
        user = Persona(
            id_role=2,
            name="UserDelete",
            surname="User",
            username = "UserDelete",
            password = generate_password_hash("TestUser123.."),
            born_date=date(1999,9,3),
            library_name="Block user",
            security_question="UserDelete",
            answer = generate_password_hash("UserDelete")
        )
        save_user(user)