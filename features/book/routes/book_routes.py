from flask import Blueprint
from flasgger import swag_from
from werkzeug.utils import secure_filename

from features.book.controller.book_controller import (
    upload_book_controller,
    get_user_books_controller,
    get_book_cover_controller,
    get_book_file_controller,
    delete_book_controller,
    download_book_controller,
    get_detail_uploaded_book_controller,
    post_review_book_controller,
    get_reviews_by_id_controller,
    delete_review_by_id_controller
)

book_routes = Blueprint('book_routes', __name__, url_prefix="/api/books")

upload_book_swagger_path = '/app/backend/docs/books/upload_book_swagger.yml'
get_user_books_swagger_path = '/app/backend/docs/books/get_user_books_swagger.yml'
get_cover_book_swagger_path = '/app/backend/docs/books/get_cover_book_swagger.yml'
get_book_file_swagger_path = '/app/backend/docs/books/get_book_file_swagger.yml'
delete_book_swagger_path = '/app/backend/docs/books/delete_book_swagger.yml'
download_book_swagger_path = '/app/backend/docs/books/download_book_swagger.yml'
get_detail_uploaded_book_swagger_path = '/app/backend/docs/books/get_detail_uploaded_book_swagger.yml'
post_review_bookswagger_path = '/app/backend/docs/books/post_review_book_swagger.yml'
get_reviews_book_swagger_path = '/app/backend/docs/books/get_reviews_book_swagger.yml'
delete_review_by_id_swagger_path = '/app/backend/docs/books/delete_review_swagger.yml'

def register_book_routes(app):
    app.register_blueprint(book_routes)

@book_routes.post('/upload')
@swag_from(upload_book_swagger_path)
def upload_book_route():
    """Sube los libros"""
    return upload_book_controller()

@book_routes.get('/user/<int:user_id>')
@swag_from(get_user_books_swagger_path)
def get_user_books_route(user_id):
    """Devuelve los libros del usuario"""
    return get_user_books_controller(user_id)

@book_routes.get("/cover/<filename>")
@swag_from(get_cover_book_swagger_path)
def get_book_cover_route(filename):
    """Devuelve la portada del libro"""
    safe_name = secure_filename(filename)
    return get_book_cover_controller(safe_name)

@book_routes.get("/file/<filename>")
@swag_from(get_book_file_swagger_path)
def get_book_file_route(filename):
    """Devuelve el archivo del libro"""
    safe_name = secure_filename(filename)
    return get_book_file_controller(safe_name)

@book_routes.delete("/delete/user/<int:user_id>/book/<int:book_id>")
@swag_from(delete_book_swagger_path)
def delete_book_route(user_id, book_id):
    """Elimina un libro"""
    return delete_book_controller(user_id, book_id)

@book_routes.get("/download/<int:id_book>")
@swag_from(download_book_swagger_path)
def download_book_route(id_book):
    """Descarga un libro"""
    return download_book_controller(id_book)

@book_routes.get("/detail-book/<int:id_book>")
@swag_from(get_detail_uploaded_book_swagger_path)
def get_detail_uploaded_book_route(id_book):
    """Consigue el detalle de un libro"""
    return get_detail_uploaded_book_controller(id_book)

@book_routes.post("/book/<int:id_book>/review")
@swag_from(post_review_bookswagger_path)
def post_review_book_route(id_book):
    """Postea una reseña"""
    return post_review_book_controller(id_book)

@book_routes.get("/book/<int:id_book>/reviews")
@swag_from(get_reviews_book_swagger_path)
def get_reviews_book_route(id_book):
    """Obtiene reseñas de un libro"""
    return get_reviews_by_id_controller(id_book)

@book_routes.delete("/review/<int:id_review>")
@swag_from(delete_review_by_id_swagger_path)
def delete_review_by_id_route(id_review):
    """Elimina reseña"""
    return delete_review_by_id_controller(id_review)