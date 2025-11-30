import os
from dotenv import load_dotenv

# Solo carga .env si existe (desarrollo local)
load_dotenv()

class ProConfig:
    DEBUG = os.getenv('DEBUG_MODE', 'True') == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

    # --- LECTURA Y CORRECCIÓN DE LA URI DE RAILWAY ---
    # 1. Lee la URI inyectada por Railway (ej: 'mysql://user:pass@host/db')
    raw_mysql_url = os.getenv('MYSQL_URL') or os.environ.get('MYSQL_URL')
    
    if not raw_mysql_url:
        raise RuntimeError(
            "La variable MYSQL_URL no está definida. "
            "Agrega MYSQL_URL en tu .env o en las variables de entorno del contenedor"
        )
    
    # 2. Reemplaza el prefijo por el dialecto PyMySQL explícito: mysql+pymysql://
    # Esto garantiza que SQLAlchemy use el driver correcto.
    SQLALCHEMY_DATABASE_URI = raw_mysql_url.replace('mysql://', 'mysql+pymysql://', 1)
    
    # -----------------------------------------------------

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.environ.get('JWT_SECRET_KEY')

config = {
    'pro': ProConfig
}

def get_database_config():
    """Retorna los datos por separado si alguna función los necesita."""
    return {
        'MYSQLHOST': os.getenv('MYSQLHOST') or os.environ.get('MYSQLHOST'),
        'MYSQLUSER': os.getenv('MYSQLUSER') or os.environ.get('MYSQLUSER'),
        'MYSQLPASSWORD': os.getenv('MYSQLPASSWORD') or os.environ.get('MYSQLPASSWORD'),
        'MYSQLDATABASE': os.getenv('MYSQLDATABASE') or os.environ.get('MYSQLDATABASE'),
    }