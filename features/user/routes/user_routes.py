from flask import Blueprint, request
from flasgger import swag_from
from features.user.controller.user_controller import register_user, verify_recover_user, get_security_question, update_new_password, get_user_library_name_controller, search_users_controller

user_routes = Blueprint('user_routes', __name__, url_prefix="/api")

register_swagger_path = '/app/backend/docs/users/register_swagger.yml'
recover_password_verify_user_path = '/app/backend/docs/users/recover_password_verify_user_swagger.yml'
recover_password_get_question_path = '/app/backend/docs/users/recover_password_get_question_swagger.yml'
recover_password_update_password_path = '/app/backend/docs/users/recover_password_update_password_swagger.yml'
get_library_name_path = '/app/backend/docs/users/get_library_name_swagger.yml'
search_users_swagger_path = '/app/backend/docs/users/search_users_swagger.yml'

def register_user_routes(app):
    app.register_blueprint(user_routes)
    
@user_routes.post('register')
@swag_from(register_swagger_path)
def register_user_route():
    return register_user()

@user_routes.post('/recover-password/verify-user')
@swag_from(recover_password_verify_user_path)
def verify_recover_user_route():
    return verify_recover_user()

@user_routes.get('/recover-password/security-question')
@swag_from(recover_password_get_question_path)
def get_security_question_route():
    return get_security_question()

@user_routes.post('/recover-password/update-password')
@swag_from(recover_password_update_password_path)
def update_new_password_route():
    return update_new_password()

@user_routes.get('/library-name')
@swag_from(get_library_name_path)
def get_library_name():
    return get_user_library_name_controller()

@user_routes.get("/users/search")
@swag_from(search_users_swagger_path)
def search_users_route():
    searched_text = request.args.get('q', '').strip()
    return search_users_controller(searched_text)