from flask import request, jsonify
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
from repo.users_repo import get_user_by_username

from exceptions.http_status import (BAD_REQUEST_EMPTY_LOGIN_MSG, 
                                    BAD_REQUEST_USERNAME_LOGIN_MSG, 
                                    BAD_REQUEST_PASSWORD_LOGIN_MSG, 
                                    USER_NOT_FOUND_MSG, 
                                    UNAUTHORIZED_LOGIN_MSG,
                                    BLOCKED_USER_CAN_NOT_LOGIN_MSG,
                                    DELETED_USER_CAN_NOT_LOGIN_MSG)

def login_controller():
    data = request.json
    username = data.get("username")
    password = data.get("password")
    
    if not username and not password:
        return BAD_REQUEST_EMPTY_LOGIN_MSG
    
    if not username:
        return BAD_REQUEST_USERNAME_LOGIN_MSG
    
    if not password:
        return BAD_REQUEST_PASSWORD_LOGIN_MSG
    
    user = get_user_by_username(username)
    
    if not user:
        return USER_NOT_FOUND_MSG
    
    if not check_password_hash(user.password, password):
        return UNAUTHORIZED_LOGIN_MSG
    
    if user.is_blocked and user.block_date:
        return BLOCKED_USER_CAN_NOT_LOGIN_MSG
    
    if user.is_erased and user.delete_date:
        return DELETED_USER_CAN_NOT_LOGIN_MSG
    
    acces_token = create_access_token(identity=str(user.id_user))
    return jsonify ({
        "msg": "The user has logged correctly",
        "token": acces_token,
        "user":{
            "id_user": user.id_user,
            "id_role": user.id_role,
            "name": user.name,
            "username": user.username
        }
    }),200
    
    