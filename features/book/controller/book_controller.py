import os
from flask import request, jsonify, make_response, abort,send_from_directory
from werkzeug.utils import secure_filename
from utils.update_book_rating import update_uploaded_book_rating
from repo.books_repo import (save_book_file, 
                             save_book, 
                             get_user_books, 
                             delete_book, 
                             get_book_by_id,
                             get_detail_updated_books,
                             post_review_book,
                             get_reviews_by_id,
                             get_review_by_id,
                             delete_review_by_id,
                             get_upload_date_book
                             )
from repo.users_repo import get_user_by_user_id
from exceptions.http_status import (
    USER_NOT_FOUND_MSG,
    BAD_REQUEST_BOOK_NOT_FOUND_UPLOAD_BOOK,
    BAD_REQUEST_USER_NOT_FOUND_UPLOAD_BOOK,
    BAD_REQUEST_INVALID_FILE_UPLOAD_BOOK,
    BAD_REQUEST_BOOK_NOT_FOUND_DELETE_MSG,
    BAD_REQUEST_USER_NOT_FOUND_DELETE_MSG,
    BAD_REQUEST_BOOK_COULD_NOT_BE_DELETED_MSG,
    BOOK_CORRECT_DELETE_MSG,
    ERROR_DELETING_BOOK_MSG,
    BOOK_NOT_FOUND_DOWNLOAD_MSG,
    BAD_REQUEST_BOOK_HAS_NOT_FILE_MSG,
    BOOK_FILE_NOT_FOUND_MSG,
    DOWNLOAD_BOOK_ERROR_MSG,
    COVER_NOT_FOUND_MSG,
    BOOK_NOT_FOUND_MSG,
    GET_DETAIL_BOOK_ERROR_MSG,
    NOT_FULL_DATA_CREATE_REVIEW_MSG,
    NO_BOOK_REVIEWS_MSG,
    REVIEW_NOT_FOUND_MSG,
    REVIEW_DELETED_MSG,
    REVIEW_DELETED_ERROR_MSG,
    BAD_REQUEST_INVALID_RATING_MSG
    
)

ENV_KEY = os.environ.get("ENV_KEY")

if ENV_KEY=="pro":
    BASE_URL = "http://pfcback-production.up.railway.app/api/books"
elif ENV_KEY=="pre":
    BASE_URL="https://pfcfront-pre.up.railway.app/api/books"
    
ALLOWED_EXTENSIONS = {'pdf', 'epub'}

BOOKS_FOLDER = os.path.join(os.getcwd(), "uploads", "books")


def allowed_file(filename):
    """Revisa los formatos permitidos."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def upload_book_controller():
    """Subir libro y devolver rutas de libro y portada para el front."""
    
    if 'file' not in request.files:
        return BAD_REQUEST_BOOK_NOT_FOUND_UPLOAD_BOOK

    file = request.files['file']
    user_id = request.form.get('user_id')
    
    if not user_id:
        return BAD_REQUEST_USER_NOT_FOUND_UPLOAD_BOOK

    if file.filename == '' or not allowed_file(file.filename):
        return BAD_REQUEST_INVALID_FILE_UPLOAD_BOOK

    # Guardar libro físico
    file_path, filename = save_book_file(file)

    # Guardar libro y portada en BD
    libro, error = save_book(file_path, filename, user_id)
    if error:
        return jsonify({'error': error}), 500

    # Obtener fecha
    upload_date = get_upload_date_book(libro.id_book, user_id)
    
    # Generar URLs
    book_file_url = f"/api/books/file/{libro.file}" if libro.file else None
    cover_file_url = f"/api/books/cover/{libro.cover}" if libro.cover else None

    return jsonify({
        'message': 'Libro subido exitosamente',
        'book': {
            'id_book': libro.id_book,
            'title': libro.title,
            'author': libro.author,
            'file': book_file_url,
            'cover': cover_file_url,
            'uploaded_date': upload_date 
        },
        'uploaded_by_user': user_id
    })

def get_user_books_controller(user_id):
    """Devuelve todos los libros de un usuario."""
    
    user = get_user_by_user_id(user_id)
    if not user:
        return USER_NOT_FOUND_MSG

    libros = get_user_books(user_id)
    result = []

    for libro, subida  in libros:
        result.append({
            "id_book": libro.id_book,
            "title": libro.title,
            "author": libro.author,

            "cover": f"{BASE_URL}/{libro.cover}"
                     if libro.cover else None,

            "file": f"{BASE_URL}/{libro.file}"
                    if libro.file else None,
            "upload_date": subida.upload_date.isoformat() if subida.upload_date else None,
            "rating": subida.rating or 0,
            "user_id": subida.user_id
        })

    return jsonify(result)

def get_book_cover_controller(filename):
    """Devuelve una portada desde uploads/covers."""

    if ".." in filename or filename.startswith("/"):
        response = make_response(*COVER_NOT_FOUND_MSG)
        abort(response)

    base_folder = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'uploads', 'covers')
    file_path = os.path.join(base_folder, filename)

    if not os.path.exists(file_path):
        response = make_response(*COVER_NOT_FOUND_MSG)
        abort(response)

    return send_from_directory(base_folder, filename)

def get_book_file_controller(filename):
    """Devuelve un libro desde uploads/books"""
    filename = secure_filename(filename)
    
    base_folder = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'uploads', 'books')
    file_path = os.path.join(base_folder, filename)
    
    if not os.path.exists(file_path):
        response = make_response(*BOOK_FILE_NOT_FOUND_MSG)
        abort(response)

    return send_from_directory(base_folder, filename)

def delete_book_controller(user_id, book_id):
    """Eliminar un libro de la librería de un usuario, incluyendo archivos físicos"""
    
    user = get_user_by_user_id(user_id)
    if not user:
        return USER_NOT_FOUND_MSG
    
    if not book_id:
        return BAD_REQUEST_BOOK_NOT_FOUND_DELETE_MSG
    
    if not user_id:
        return BAD_REQUEST_USER_NOT_FOUND_DELETE_MSG
    
    try:
        success = delete_book(user_id, book_id)
        
        if not success:
            return BAD_REQUEST_BOOK_COULD_NOT_BE_DELETED_MSG
        
        return BOOK_CORRECT_DELETE_MSG
        
    except Exception as e:
        print(f"Exception en delete_book_controller: {e}")
        return ERROR_DELETING_BOOK_MSG
    
def download_book_controller(id_book):
    """Descargar un libro"""
    try:
        libro = get_book_by_id(id_book)
        if not libro:
            return BOOK_NOT_FOUND_DOWNLOAD_MSG
             
        if not libro.file:
            return BAD_REQUEST_BOOK_HAS_NOT_FILE_MSG
        
        file_path = os.path.join(BOOKS_FOLDER, libro.file)
        if not os.path.exists(file_path):
            return BOOK_FILE_NOT_FOUND_MSG

        return send_from_directory(BOOKS_FOLDER, libro.file, as_attachment=True)
    
    except Exception as e:
        print(f"Error descargando el libro: {e}")
        return DOWNLOAD_BOOK_ERROR_MSG
    
def get_detail_uploaded_book_controller(id_book):
    """Obtener detalle de un libro"""
    try:
        result = get_detail_updated_books(id_book)
        
        #Comprueba si hay resultado
        if not result:
            return BOOK_NOT_FOUND_MSG
        
        book, uploaded_book = result
        
        #Pasar de 10 a 5 para puntuación con estrellas
        rating_by_five = round((uploaded_book.rating or 0) / 2, 1)
        
        response = {
            "id_book": book.id_book,
            "title": book.title,
            "author": book.author,
            "cover": f"http://pfcback-production.up.railway.app/api/books/cover/{book.cover}"
                     if book.cover else None,
            "file": f"http://pfcback-production.up.railway.app/api/books/file/{book.file}"
                    if book.file else None,
            "upload_date": uploaded_book.upload_date.isoformat() if uploaded_book.upload_date else None,
            "rating": rating_by_five
        }
        
        return jsonify(response)
    
    except Exception as e:
        print(f"Error obteniendo el detalle del libro: {e}")
        return GET_DETAIL_BOOK_ERROR_MSG
        
def post_review_book_controller(id_book):
    """Crear reseña"""
    data = request.json
    user_id = data.get("user_id")
    book_id = id_book
    review_text = data.get("review_text")
    stars_rating = data.get("rating")
    
    if not all([user_id, book_id, review_text, stars_rating is not None]):
        return  NOT_FULL_DATA_CREATE_REVIEW_MSG
    
    libro = get_book_by_id(book_id)
    if not libro:
        return BOOK_NOT_FOUND_MSG
    
    book_rating = int(stars_rating*2)
    if book_rating<0 or book_rating>10:
        return BAD_REQUEST_INVALID_RATING_MSG
    
    response, status_code = post_review_book(user_id,book_id, review_text, book_rating)
    
    update_uploaded_book_rating(id_book)
    
    return response, status_code
    
def get_reviews_by_id_controller(id_book):
    """Obtiene todas las reseñas de un libro"""
    reviews = get_reviews_by_id(id_book)
    
    if reviews is None:
        return BOOK_NOT_FOUND_MSG
    
    if len(reviews) == 0:
        return NO_BOOK_REVIEWS_MSG
    
    reviews_list = [review.as_dict() for review in reviews]
    
    return {"reviews": reviews_list},200

def delete_review_by_id_controller(id_review):
    """Elimina reseña"""
    review = get_review_by_id(id_review)
    if not review:
        return REVIEW_NOT_FOUND_MSG
    
    book_id = review.book_id
    
    success = delete_review_by_id(id_review)

    if not success:
        return REVIEW_DELETED_ERROR_MSG
    
    update_uploaded_book_rating(book_id)
    
    return REVIEW_DELETED_MSG