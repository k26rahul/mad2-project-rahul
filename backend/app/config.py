import os
import secrets
from dotenv import load_dotenv

load_dotenv()


class Config:
  # Debugging
  DEBUG = os.getenv('DEBUG', 'True') == 'True'

  # Security
  SECRET_KEY = os.getenv('SECRET_KEY', secrets.token_hex(32))
  SECURITY_PASSWORD_SALT = os.getenv('SECURITY_PASSWORD_SALT', secrets.token_hex(16))
  SECURITY_REMEMBER_SALT = os.getenv('SECURITY_REMEMBER_SALT', secrets.token_hex(16))

  # Database
  SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///')

  # Session Management
  SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
  SESSION_PERMANENT = os.getenv('SESSION_PERMANENT', 'True') == 'True'
  PERMANENT_SESSION_LIFETIME = int(os.getenv('PERMANENT_SESSION_LIFETIME', 86400))

  # Cookies
  REMEMBER_COOKIE_SAMESITE = os.getenv('REMEMBER_COOKIE_SAMESITE', 'None')
  REMEMBER_COOKIE_SECURE = os.getenv('REMEMBER_COOKIE_SECURE', 'True') == 'True'
  SESSION_COOKIE_SAMESITE = os.getenv('SESSION_COOKIE_SAMESITE', 'None')
  SESSION_COOKIE_SECURE = os.getenv('SESSION_COOKIE_SECURE', 'True') == 'True'
