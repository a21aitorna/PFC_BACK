import os
from dotenv import load_dotenv

load_dotenv()

class ProConfig:
    DEBUG = os.getenv('DEBUG_MODE', 'True') == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MYSQLUSER')}:{os.getenv('MYSQLPASSWORD')}"
        f"@{os.getenv('MYSQLHOST')}/{os.getenv('MYSQLDATABASE')}"
    )
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

config = {
    'pro': ProConfig
}

def get_database_config():
    return {
        'MYSQLHOST': os.getenv('MYSQLHOST'),
        'MYSQLUSER': os.getenv('MYSQLUSER'),
        'MYSQLPASSWORD': os.getenv('MYSQLPASSWORD'),
        'MYSQLDATABASE': os.getenv('MYSQLDATABASE'),
    }
