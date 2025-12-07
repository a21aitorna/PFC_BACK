import os
import io
import zipfile
import xml.etree.ElementTree as ET
from ebooklib import epub
from PIL import Image
import fitz

COVERS_PATH = os.path.join('uploads', 'covers')
DEFAULT_COVER = '/uploads/covers/default_cover.jpg'  # ruta pública
ITEM_IMAGE = 9


def normalize_category(cat_name: str) -> str:
    return cat_name.strip().capitalize()


def save_cover_image(image_data, output_path, convert_to_png=True):
    """Guardar imagen y devolver ruta pública"""
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    try:
        if convert_to_png:
            image = Image.open(io.BytesIO(image_data))
            output_path = os.path.splitext(output_path)[0] + '.png'
            image.save(output_path, 'PNG')
        else:
            with open(output_path, "wb") as f:
                f.write(image_data)

        # Convertir ruta de disco a URL pública
        public_path = '/' + output_path.replace('\\', '/')
        return public_path

    except Exception as e:
        print(f"No se pudo guardar la portada: {e}")
        return DEFAULT_COVER


# Obtiene la portada leyendo el EPUB directamente como ZIP
def extract_cover_from_epub_zip(book_path, book_filename):
    try:
        with zipfile.ZipFile(book_path, 'r') as z:

            # 1. Localizar el OPF
            try:
                container = z.read('META-INF/container.xml')
            except KeyError:
                return DEFAULT_COVER

            root = ET.fromstring(container)
            ns = {'c': 'urn:oasis:names:tc:opendocument:xmlns:container'}
            rootfile = root.find('.//c:rootfile', ns)

            if rootfile is None:
                return DEFAULT_COVER

            opf_path = rootfile.get('full-path')
            if not opf_path:
                return DEFAULT_COVER

            # 2. Leer OPF
            opf_data = z.read(opf_path)
            opf_root = ET.fromstring(opf_data)

            # Namespaces
            ns_opf = {'opf': 'http://www.idpf.org/2007/opf'}

            metadata = opf_root.find('opf:metadata', ns_opf)
            manifest = opf_root.find('opf:manifest', ns_opf)

            cover_id_or_href = None

            # 3. EPUB2: <meta name="cover">
            if metadata is not None:
                for meta in metadata.findall('opf:meta', ns_opf):
                    if meta.get('name') == 'cover':
                        cover_id_or_href = meta.get('content')
                        break

            cover_href = None

            # 4. Buscar el item real en el manifest
            if cover_id_or_href and manifest is not None:
                for item in manifest.findall('opf:item', ns_opf):
                    if item.get('id') == cover_id_or_href:
                        cover_href = item.get('href')
                        break

                # por si es href directo
                if not cover_href:
                    for item in manifest.findall('opf:item', ns_opf):
                        if item.get('href') == cover_id_or_href:
                            cover_href = item.get('href')
                            break

            # 5. EPUB3 fallback: properties="cover-image"
            if not cover_href and manifest is not None:
                for item in manifest.findall('opf:item', ns_opf):
                    props = item.get('properties', '')
                    if 'cover-image' in props:
                        cover_href = item.get('href')
                        break

            # 6. Resolver ruta real
            image_bytes = None
            if cover_href:
                opf_dir = os.path.dirname(opf_path)
                image_path = os.path.normpath(os.path.join(opf_dir, cover_href)).replace('\\', '/')

                try:
                    image_bytes = z.read(image_path)
                except KeyError:
                    try:
                        image_bytes = z.read(cover_href)
                    except KeyError:
                        image_bytes = None

            # 7. Fallback por nombre típico
            if image_bytes is None:
                common_paths = [
                    'Images/cover.jpg', 'Images/cover.png',
                    'cover.jpg', 'cover.png'
                ]
                for p in common_paths:
                    try:
                        image_bytes = z.read(p)
                        break
                    except KeyError:
                        continue

            # 8. Guardar
            if image_bytes:
                filename = f"{os.path.splitext(book_filename)[0]}_cover"
                return save_cover_image(image_bytes, os.path.join(COVERS_PATH, filename), True)

            return DEFAULT_COVER

    except Exception as e:
        print("Error extrayendo portada:", e)
        return DEFAULT_COVER


def extract_epub_metadata(book_path, book_filename):
    if not os.path.exists(book_path):
        print(f"Archivo no encontrado: {book_path}")
        return None

    try:
        book = epub.read_epub(book_path)

        # Título y autor
        title = book.get_metadata('DC', 'title')[0][0] if book.get_metadata('DC', 'title') else 'Sin título'
        author = book.get_metadata('DC', 'creator')[0][0] if book.get_metadata('DC', 'creator') else 'Desconocido'

        # Categorías
        subjects = book.get_metadata('DC', 'subject')
        categories = [normalize_category(s[0]) for s in subjects if s and s[0].strip()] if subjects else []

        # Extracción de portada
        cover_path = extract_cover_from_epub_zip(book_path, book_filename)

        return {
            'title': title,
            'author': author,
            'categories': categories,
            'cover_path': cover_path
        }

    except Exception as e:
        print(f"Error procesando EPUB: {e}")
        import traceback
        traceback.print_exc()
        return None


def extract_pdf_metadata(book_path, book_filename):
    if not os.path.exists(book_path):
        print(f"Archivo no encontrado: {book_path}")
        return None

    try:
        doc = fitz.open(book_path)

        metadata = doc.metadata
        title = metadata.get('title', '') or 'Sin título'
        author = metadata.get('author', '') or 'Desconocido'
        categories = []

        cover_path = DEFAULT_COVER
        if doc.page_count > 0:
            page = doc.load_page(0)
            pix = page.get_pixmap()
            image_data = pix.tobytes("png")
            cover_path = save_cover_image(
                image_data,
                os.path.join(COVERS_PATH, f"{os.path.splitext(book_filename)[0]}_cover")
            )

        doc.close()

        return {
            'title': title,
            'author': author,
            'categories': categories,
            'cover_path': cover_path
        }

    except Exception as e:
        print(f"Error procesando PDF: {e}")
        return None


def extract_metadata(book_path, book_filename):
    ext = os.path.splitext(book_filename)[1].lower()
    if ext == '.epub':
        return extract_epub_metadata(book_path, book_filename)
    elif ext == '.pdf':
        return extract_pdf_metadata(book_path, book_filename)
    else:
        raise ValueError("Formato no permitido")
