from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flasgger import Swagger
import pymysql

from envs.pro.pro_env import config

from dao.categoria_dao import Categoria
from dao.libro_categoria_dao import LibroCategoria
from dao.libro_dao import Libro
from dao.libro_subido_dao import LibroSubido
from dao.persona_dao import Persona
from dao.reseña_dao import Reseña
from dao.rol_dao import Rol

from database.db import init_app

from features.user.routes.login_routes import register_login_routes
from features.user.routes.user_routes import register_user_routes
from features.book.routes.book_routes import register_book_routes
from features.admin.routes.admin_routes import register_admin_routes
from seed import seed_roles, seed_test_user, seed_admin_user
from utils.jwt_decorator import register_jwt_callbacks
from tasks.automatic_tasks import automatic_unblock_users, automatic_delete_users

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config.from_object(config['pro'])

CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

init_app(app)

with app.app_context():
    seed_roles()
    seed_test_user()
    seed_admin_user()
    automatic_unblock_users()
    automatic_delete_users()
    
swagger = Swagger(app)
jwt = JWTManager(app)

register_jwt_callbacks(jwt)

register_login_routes(app)
register_user_routes(app)
register_book_routes(app)
register_admin_routes(app)

@app.route('/')
def index():
    return "Comprobación contenedor backend correcto"
