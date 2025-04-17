import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default-secret-key')
    COHERE_API_KEY = os.getenv('COHERE_API_KEY')
    HUGGINGFACEHUB_API_TOKEN = os.getenv('HUGGINGFACEHUB_API_TOKEN')
    GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
    
    # Vector store settings
    VECTORSTORE_DIR = 'vectorstore'
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'pptx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size 