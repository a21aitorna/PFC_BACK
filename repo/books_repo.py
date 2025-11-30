import os
import shutil
from flask import jsonify
from werkzeug.utils import secure_filename
import uuid
from typing import Tuple, Optional
from utils.extractor_metadatos import extract_metadata
from database.db import db
from dao.libro_dao import Libro
from dao.libro_subido_dao import LibroSubido
from dao.categoria_dao import Categoria
from dao.libro_categoria_dao import LibroCategoria
from dao.reseña_dao import Reseña

# Rutas de carpetas
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # backend/repo
UPLOADS_FOLDER = os.path.join(BASE_DIR, '../uploads')   # backend/uploads
BOOKS_FOLDER = os.path.join(UPLOADS_FOLDER, 'books')
COVERS_FOLDER = os.path.join(UPLOADS_FOLDER, 'covers')

def ensure_directories():
    """Asegura que existan los directorios necesarios"""
    os.makedirs(BOOKS_FOLDER, exist_ok=True)
    os.makedirs(COVERS_FOLDER, exist_ok=True)

def save_book_file(file_storage) -> Tuple[str, str]:
    """
    Guarda el archivo del libro en uploads/books (devuelve la ruta absoluta y el filename).
    """
    ensure_directories()

    filename = secure_filename(file_storage.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"

    file_path = os.path.join(BOOKS_FOLDER, unique_filename)
    file_storage.save(file_path)

    print(f"Archivo guardado en: {os.path.abspath(file_path)}")

    return file_path, unique_filename

def save_cover(cover_path) -> Optional[str]:
    """
    Guarda la portada en uploads/covers y devuelve solo el filename.
    """
    if not cover_path or not os.path.exists(cover_path):
        return None

    try:
        ensure_directories()

        original_filename = os.path.basename(cover_path)
        cover_filename = f"{uuid.uuid4().hex}_{original_filename}"

        new_cover_path = os.path.join(COVERS_FOLDER, cover_filename)

        shutil.copy2(cover_path, new_cover_path)

        try:
            os.remove(cover_path)
        except OSError as e:
            print(f"Advertencia: No se pudo eliminar archivo temporal {cover_path}: {e}")

        return cover_filename
    except Exception as e:
        print(f"Error guardando portada: {e}")
        return None

def get_or_create_category(cat_name):
    """Busca una categoría por nombre o la crea si no existe"""
    category = Categoria.query.filter_by(category_name=cat_name).first()
    if not category:
        category = Categoria(category_name=cat_name)
        db.session.add(category)
        db.session.flush()
    return category

def save_book_categories(libro, categories):
    """Asocia categorías a un libro"""
    for cat_name in categories:
        if cat_name and cat_name.strip():
            category = get_or_create_category(cat_name.strip())
            libro_categoria = LibroCategoria(book_id=libro.id_book, category_id=category.id_category)
            db.session.add(libro_categoria)

def save_book(file_path: str, filename: str, user_id: int) -> Tuple[Optional[Libro], Optional[str]]:
    """Guarda el libro, su portada y metadatos en BD."""
    metadata = extract_metadata(file_path, filename)
    if not metadata:
        return None, "No se pudieron extraer metadatos"

    try:
        #Guardar portada
        cover_filename = save_cover(metadata.get('cover_path'))
        book_filename = filename

        #Guardar libro en base de datos
        libro = Libro(
            title=metadata.get('title', 'Sin título'),
            author=metadata.get('author', 'Autor desconocido'),
            cover=cover_filename,
            file=book_filename
        )
        db.session.add(libro)
        db.session.flush()

        #Asocia categoría
        save_book_categories(libro, metadata.get('categories', []))

        # Guarda la relación usuario libro
        subida = LibroSubido(user_id=user_id, book_id=libro.id_book)
        db.session.add(subida)
        db.session.commit()
        return libro, None

    except Exception as e:
        db.session.rollback()
        print(f"Error al guardar libro: {e}")

        #Limpiar archivos en caso de fallo
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
            if metadata.get('cover_path') and os.path.exists(metadata['cover_path']):
                os.remove(metadata['cover_path'])
        except Exception as cleanup_error:
            print(f"Error en limpieza: {cleanup_error}")

        return None, f"Error en base de datos: {str(e)}"

def get_upload_date_book(book_id, user_id):
    """Conseguir la fecha de subida de un libro"""
    register = LibroSubido.query.filter_by(book_id=book_id, user_id=user_id).first()
    return register.upload_date
    
def get_user_books(user_id):
    """Obtiene todos los libros de un usuario"""
    return (
        db.session.query(Libro, LibroSubido)
        .join(LibroSubido, Libro.id_book == LibroSubido.book_id)
        .filter(LibroSubido.user_id == user_id)
        .all()
    )

def delete_book(id_user, id_book):
    """Elimina un libro y la relación con el usuario, así como los archivos físicos relacionados a ellos"""
    # Obtener reseñas del libro
    reseñas = Reseña.query.filter_by(book_id=id_book).all()
    
    # Obtener relación libro-usuario
    libro_subido = LibroSubido.query.filter_by(user_id=id_user, book_id=id_book).first()
    if not libro_subido:
        return False

    # Obtener relaciones libro-categorias
    libro_categorias = LibroCategoria.query.filter_by(book_id=id_book).all()

    # Obtener libro
    libro = Libro.query.get(id_book)
    if not libro:
        return False

    # Eliminar archivos físicos
    try:
        if libro.cover and os.path.exists(os.path.join(COVERS_FOLDER, libro.cover)):
            os.remove(os.path.join(COVERS_FOLDER, libro.cover))
        if libro.file and os.path.exists(os.path.join(BOOKS_FOLDER, libro.file)):
            os.remove(os.path.join(BOOKS_FOLDER, libro.file))
    except Exception as e:
        print(f"Error eliminando archivos físicos: {e}")
        return False

    # Eliminar de la base de datos
    try:
        for reseña in reseñas:
            db.session.delete(reseña)
        db.session.delete(libro_subido)
        for lc in libro_categorias:
            db.session.delete(lc)
        db.session.delete(libro)
        db.session.commit()
        return True

    except Exception as e:
        db.session.rollback()
        return False
    
def get_book_by_id(book_id):
    """Obtener libro por id"""
    return Libro.query.filter_by(id_book=book_id).first()

def get_detail_updated_books(id_book):
    """Obtener el detalle de un libro subido"""
    return (
        db.session.query(Libro, LibroSubido)
        .join(LibroSubido, Libro.id_book == LibroSubido.book_id)
        .filter(Libro.id_book == id_book)
        .first()
    )
    
def post_review_book(user_id, book_id, review_text, book_rating):
    """Publicar una reseña"""
    try:
        review = Reseña(
            user_id=user_id,
            book_id=book_id,
            review_text=review_text,
            book_rating=book_rating
        )
        
        db.session.add(review)
        db.session.commit()
        return jsonify({"message": "Reseña creada correctamente", "review": review.as_dict()}), 201

    except Exception as e:
        print(f"Error al crear la reseña: {e}")
        db.session.rollback()
        
def get_reviews_by_id(id_book):
    """"Obtiene todas las reseñas de un libro por fecha de creación"""
    return db.session.query(Reseña).filter(Reseña.book_id==id_book).order_by(Reseña.creation_date.desc()).all()

def get_review_by_id(id_review):
    """Obtiene una reseña en concreto"""
    return Reseña.query.get(id_review)

def delete_review_by_id(id_review):
    """Eimina una reseña por id"""
    review = get_review_by_id(id_review)
    if not review:
        return False
    try:
        db.session.delete(review)
        db.session.commit()
        return True
    except Exception as e:
        db.session.rollback()
        print(f"Error eliminando la reseñ: {e}")
        return False
    