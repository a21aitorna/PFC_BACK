from flask import Blueprint, request
from flasgger import swag_from
from features.user.controller.login_controller import login_controller

login_routes = Blueprint('login_routes', __name__, url_prefix="/api")

login_swagger_path = '/app/backend/docs/users/login_swagger.yml'

def register_login_routes(app):
    app.register_blueprint(login_routes)
    
@login_routes.post('/login')
@swag_from(login_swagger_path)
def login_route():
    return login_controller()
