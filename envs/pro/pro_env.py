import os
from dotenv import load_dotenv

# Solo carga .env si existe, útil para desarrollo local
load_dotenv()

class ProConfig:
    DEBUG = os.getenv('DEBUG_MODE', 'True') == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

    # Primero intenta leer MYSQL_URL de .env, si no existe toma la del entorno del contenedor
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_URL') or os.environ.get('MYSQL_URL')
    
    if not SQLALCHEMY_DATABASE_URI:
        raise RuntimeError(
            "La variable MYSQL_URL no está definida. "
            "Agrega MYSQL_URL en tu .env o en las variables de entorno del contenedor"
        )

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY') or os.environ.get('JWT_SECRET_KEY')

config = {
    'pro': ProConfig
}

def get_database_config():
    """Retorna datos por separado si alguna función los necesita."""
    return {
        'MYSQLHOST': os.getenv('MYSQLHOST') or os.environ.get('MYSQLHOST'),
        'MYSQLUSER': os.getenv('MYSQLUSER') or os.environ.get('MYSQLUSER'),
        'MYSQLPASSWORD': os.getenv('MYSQLPASSWORD') or os.environ.get('MYSQLPASSWORD'),
        'MYSQLDATABASE': os.getenv('MYSQLDATABASE') or os.environ.get('MYSQLDATABASE'),
    }
