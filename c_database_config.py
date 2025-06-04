import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# مسیر پروژه (همون جایی که a_main.py هست)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

ENVIRONMENT = os.getenv("ENV", "local").lower()

if ENVIRONMENT == "production":
    DB_USER = os.getenv("POSTGRES_USER")
    DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
    DB_NAME = os.getenv("POSTGRES_DB")
    DB_HOST = os.getenv("POSTGRES_HOST")
    DB_PORT = os.getenv("POSTGRES_PORT", "5432")

    SQLALCHEMY_DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

else:
    SQLITE_DB_FILE = os.getenv("SQLITE_DB_FILE", "c_database/smart_expert.db")

    # ساخت مسیر کامل بر اساس مسیر پروژه
    absolute_db_path = os.path.join(BASE_DIR, "..", SQLITE_DB_FILE).replace("\\", "/")
    db_dir = os.path.dirname(absolute_db_path)

    if db_dir and not os.path.exists(db_dir):
        os.makedirs(db_dir)

    SQLALCHEMY_DATABASE_URL = f"sqlite:///{absolute_db_path}"

def get_database_url():
    return SQLALCHEMY_DATABASE_URL
