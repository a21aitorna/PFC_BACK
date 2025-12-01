from flask import jsonify
from flask_jwt_extended import get_jwt_identity
from exceptions.http_status import (USER_NOT_FOUND_MSG,
                                    SUCCESS_UNBLOCK_USER_MSG,
                                    SUCCESS_RECTIFY_DELETE_USER_MSG,
                                    CAN_NOT_BLOCK_AN_ADMIN,
                                    CAN_NOT_DELETE_AN_ADMIN)
from repo.admin_repo import (get_all_not_admin_users, 
                             block_user, unblock_user, 
                             delete_user,
                             rectify_delete_user)
from repo.users_repo import get_user_by_user_id

def get_not_admin_users_controller():
    """Controlador para recuperar todos los usuarios que no son admin"""
    users = get_all_not_admin_users()
    return jsonify([user.as_dict() for user in users])
        
def block_user_controller(id_user):
    """Controlador para bloquear un usuario"""
    user  = get_user_by_user_id(id_user)
    
    if not user:
        return USER_NOT_FOUND_MSG

    if user.id_role == 1:
            return CAN_NOT_BLOCK_AN_ADMIN
    
    block_user(user)
    
    return jsonify({
        "message": "User blocked for 3 days",
        "block_date": user.block_date
    })
    
def unblock_user_controller(id_user):
    """Controlador para desbloquear un usuario"""
    user = unblock_user(id_user)
    
    if not user:
        return USER_NOT_FOUND_MSG
    
    return SUCCESS_UNBLOCK_USER_MSG

def delete_user_controller(id_user):
    """Controlador para eliminar un usuario"""
    user = get_user_by_user_id(id_user)

    if not user:
        return USER_NOT_FOUND_MSG

    if user.id_role == 1:
        return CAN_NOT_DELETE_AN_ADMIN
        
    delete_user(user)
    
    return jsonify({
        "message":"User is going to be deleted in 15 days",
        "delete_date": user.delete_date
    })
    
def rectify_delete_user_controller(id_user):
    """Controlador para rectificar la eliminación de un usuario"""
    user = rectify_delete_user(id_user)
    
    if not user:
        return USER_NOT_FOUND_MSG
    
    return SUCCESS_RECTIFY_DELETE_USER_MSG