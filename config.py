import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    # Railway provides DATABASE_URL for PostgreSQL, fallback to SQLite for local dev
    database_url = os.getenv('DATABASE_URL', 'sqlite:///app.db')
    # Convert Railway's postgres:// to postgresql:// (SQLAlchemy requirement)
    if database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # OAuth Configuration
    GOOGLE_CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET')
    
    # Application URL - Railway will provide RAILWAY_PUBLIC_DOMAIN
    APP_URL = os.getenv('APP_URL') or os.getenv('RAILWAY_PUBLIC_DOMAIN', 'http://localhost:5000')
    # Ensure APP_URL has protocol
    if APP_URL and not APP_URL.startswith('http'):
        APP_URL = f'https://{APP_URL}'
    
    # OAuth Redirect URIs
    GOOGLE_REDIRECT_URI = f"{APP_URL}/auth/google/callback"
    
    # Cloudinary Configuration
    CLOUDINARY_CLOUD_NAME = os.getenv('CLOUDINARY_CLOUD_NAME')
    CLOUDINARY_API_KEY = os.getenv('CLOUDINARY_API_KEY')
    CLOUDINARY_API_SECRET = os.getenv('CLOUDINARY_API_SECRET')
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
