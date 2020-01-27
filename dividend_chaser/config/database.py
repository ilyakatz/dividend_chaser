import os
from dotenv import load_dotenv
load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_DATABASE = os.getenv("DB_DATABASE")
DB_USER = os.getenv("DB_USER") or ""
DB_PASSWORD = os.getenv("DB_PASSWORD") or ""

DATABASES = {
    'default': 'postgres',
    'postgres': {
        'driver': 'postgres',
        'host': DB_HOST,
        'database': DB_DATABASE,
        'user': DB_USER,
        'password': DB_PASSWORD,
        'prefix': ''
    }
}
