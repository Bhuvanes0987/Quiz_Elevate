
import os
from dotenv import load_dotenv
load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL') or (
        f"mysql+pymysql://{os.getenv('MYSQL_USER','root')}:{os.getenv('MYSQL_PASSWORD','Excel@123')}@{os.getenv('MYSQL_HOST','localhost')}:{os.getenv('MYSQL_PORT','3306')}/{os.getenv('MYSQL_DATABASE','quizelevate')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-string')
    OLLAMA_URL = os.getenv('OLLAMA_URL', 'http://localhost:11434')
