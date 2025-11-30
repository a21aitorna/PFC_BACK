from flask import Blueprint
from flasgger import swag_from
from features.admin.controller.admin_controller import (get_not_admin_users_controller,
                                                        block_user_controller,
                                                        unblock_user_controller,
                                                        delete_user_controller,
                                                        rectify_delete_user_controller)
from utils.jwt_decorator import admin_required

admin_routes = Blueprint('admin_routes', __name__, url_prefix="/api/admin")

get_not_admin_users_swagger_path = '/app/backend/docs/admin/get_not_admin_users_swagger.yml'
block_user_swagger_path = '/app/backend/docs/admin/block_user_swagger.yml'
unblock_user_swagger_path = '/app/backend/docs/admin/unblock_user_swagger.yml'
delete_user_swagger_path = '/app/backend/docs/admin/delete_user_swagger.yml'
rectify_delete_user_swagger_path = '/app/backend/docs/admin/rectify_delete_user_swagger.yml'

def register_admin_routes(app):
    app.register_blueprint(admin_routes)
    
@admin_routes.get('/not-admin-users')
@swag_from(get_not_admin_users_swagger_path)
@admin_required
def get_not_admin_users_route():
    """"Devuelve los usuarios que no son admin"""
    return get_not_admin_users_controller()

@admin_routes.post('/block/<int:id_user>')
@swag_from(block_user_swagger_path)
@admin_required
def block_user_route(id_user):
    """Bloquea el usuario seleccionado"""
    return block_user_controller(id_user)

@admin_routes.post('/unblock/<int:id_user>')
@swag_from(unblock_user_swagger_path)
@admin_required
def unblock_user_route(id_user):
    """Rectifica el desbloqueo del usuario seleccionado"""
    return unblock_user_controller(id_user)

@admin_routes.post('/delete/<int:id_user>')
@swag_from(delete_user_swagger_path)
@admin_required
def delete_user_route(id_user):
    """Selecciona un usuario a eliminar"""
    return delete_user_controller(id_user)

@admin_routes.post('rectify-delete/<int:id_user>')
@swag_from(rectify_delete_user_swagger_path)
@admin_required
def rectify_delete_user_route(id_user):
    """Rectifica la eliminación de un usuario"""
    return rectify_delete_user_controller(id_user)