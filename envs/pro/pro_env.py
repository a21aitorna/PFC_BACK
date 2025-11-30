# envs/pro/pro_env.py (Ajustado para Railway)

import os

def parse_api_url(env_key, default_value):
    api_url_from_env = os.getenv(env_key)
    if api_url_from_env:
        return api_url_from_env.rstrip('/api')
    return default_value

class ProConfig:
    DEBUG = os.getenv('DEBUG_MODE', 'False') == 'True'
    API_BASE_URL = parse_api_url('API_BASE_URL', 'http://localhost:5000')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False') == 'True'

    # Prioridad: DATABASE_URL > Variables separadas de MySQL
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')

    if not SQLALCHEMY_DATABASE_URI:
        _host = os.getenv('MYSQLHOST')
        _port = os.getenv('MYSQLPORT', '3306')
        _user = os.getenv('MYSQLUSER')
        _pass = os.getenv('MYSQLPASSWORD')
        _db = os.getenv('MYSQLDATABASE')

        if _host and _user and _pass and _db:
            # Forzar IPv4 si es necesario usando el host proporcionado por Railway
            SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{_user}:{_pass}@{_host}:{_port}/{_db}"
        else:
            raise ValueError(
                "SQLALCHEMY_DATABASE_URI no está configurada. "
                "Compruebe MYSQLHOST, MYSQLUSER, MYSQLPASSWORD y MYSQLDATABASE en el entorno."
            )

    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'cambia_esto_en_produccion')

config = {
    'pro': ProConfig
}
