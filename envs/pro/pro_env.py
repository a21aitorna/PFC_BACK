import os
from dotenv import load_dotenv

load_dotenv()

class ProConfig:
    DEBUG = os.getenv('DEBUG_MODE', 'True') == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    
    # Usamos directamente la URL completa de Railway
    SQLALCHEMY_DATABASE_URI = os.getenv('MYSQL_URL')

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

config = {
    'pro': ProConfig
}

def get_database_config():
    """Retorna solo los datos por separado si alguna función los necesita."""
    return {
        'MYSQLHOST': os.getenv('MYSQLHOST'),
        'MYSQLUSER': os.getenv('MYSQLUSER'),
        'MYSQLPASSWORD': os.getenv('MYSQLPASSWORD'),
        'MYSQLDATABASE': os.getenv('MYSQLDATABASE'),
    }
