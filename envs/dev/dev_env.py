import os
from dotenv import load_dotenv

load_dotenv()

class DevConfig:
    DEBUG = os.getenv('DEBUG_MODE', 'True') == 'True'
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}"
        f"@{os.getenv('MYSQL_HOST')}/{os.getenv('DATABASE_NAME')}"
    )
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')

config = {
    'dev': DevConfig
}

def get_database_config():
    return {
        'MYSQL_HOST': os.getenv('MYSQL_HOST'),
        'MYSQL_USER': os.getenv('MYSQL_USER'),
        'MYSQL_PASSWORD': os.getenv('MYSQL_PASSWORD'),
        'DATABASE_NAME': os.getenv('DATABASE_NAME'),
    }
