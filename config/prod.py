from pathlib import Path


DEBUG = False
SECRET_KEY = 'secret'
SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/login_app.db"
SQLALCHEMY_TRACK_MODIFICATIONS = False

BASE_DIR = Path(__file__).resolve().parent.parent  # Obtiene la carpeta donde está el archivo actual
UPLOAD_FOLDER = BASE_DIR / "uploads"  # Sube un nivel y apunta a "uploads"