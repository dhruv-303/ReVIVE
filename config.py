import os
import urllib.parse
from datetime import timedelta
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'revive-college-startup-secret-key-2026-auth')
    JWT_EXPIRATION_DELTA = timedelta(days=7)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MySQL Credentials from Environment Variables
    MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
    MYSQL_PORT = os.environ.get('MYSQL_PORT', '3306')
    MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
    MYSQL_DB = os.environ.get('MYSQL_DB', 'revive_db')

    # Allow custom direct DATABASE_URL override
    custom_db_url = os.environ.get('DATABASE_URL')
    if custom_db_url:
        SQLALCHEMY_DATABASE_URI = custom_db_url
    else:
        # URL encode password in case it contains special characters (@, :, /, etc.)
        encoded_password = urllib.parse.quote_plus(MYSQL_PASSWORD)
        mysql_uri = f"mysql+pymysql://{MYSQL_USER}:{encoded_password}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}?charset=utf8mb4"

        # Check if MySQL is actively reachable on the given host/port
        # If not reachable, fallback gracefully to SQLite so the project can be run and tested
        # immediately even before the student boots up MySQL in Workbench.
        import socket
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            res = sock.connect_ex((MYSQL_HOST, int(MYSQL_PORT)))
            sock.close()
            if res == 0:
                SQLALCHEMY_DATABASE_URI = mysql_uri
                ACTIVE_DB_TYPE = "MySQL"
            else:
                sqlite_path = os.path.join(BASE_DIR, 'revive_dev.db')
                SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"
                ACTIVE_DB_TYPE = "SQLite (Fallback: MySQL server not responding on port 3306)"
        except Exception:
            sqlite_path = os.path.join(BASE_DIR, 'revive_dev.db')
            SQLALCHEMY_DATABASE_URI = f"sqlite:///{sqlite_path}"
            ACTIVE_DB_TYPE = "SQLite (Fallback)"

