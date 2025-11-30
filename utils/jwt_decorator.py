from functools import wraps
from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, JWTManager
from repo.users_repo import get_user_by_user_id
from exceptions.http_status import (
    USER_NOT_FOUND_MSG,
    FORBIDDEN_ACTION_NOT_ADMIN_MSG,
    UNAUTHORIZED_NOT_ADMIN_MSG
)

def register_jwt_callbacks(jwt: JWTManager):
    # Callback cuando no hay token
    @jwt.unauthorized_loader
    def custom_missing_token_callback(err_msg):
        return UNAUTHORIZED_NOT_ADMIN_MSG

    # Callback cuando el token es inválido
    @jwt.invalid_token_loader
    def custom_invalid_token_callback(err_msg):
        return UNAUTHORIZED_NOT_ADMIN_MSG

def admin_required(f):
    @wraps(f)
    @jwt_required()  # Valida que haya un token válido antes de entrar
    def decorated_function(*args, **kwargs):
        user_identity = get_jwt_identity()  # Obtenemos el identity del token

        try:
            user_id = int(user_identity)
        except (TypeError, ValueError):
            return UNAUTHORIZED_NOT_ADMIN_MSG

        user = get_user_by_user_id(user_id)

        if not user:
            return USER_NOT_FOUND_MSG  # 404
        if user.id_role != 1:
            return FORBIDDEN_ACTION_NOT_ADMIN_MSG  # 403

        return f(*args, **kwargs)

    return decorated_function
