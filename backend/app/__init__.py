from flask import Flask
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from .config import Config
from db.models import db, User, Role
from db.seed import seed_data

from routes.auth import auth_bp
from routes.admin import admin_bp
from routes.user import user_bp
from routes.common import common_bp

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  Security(app, user_datastore, register_blueprint=False)

  # Enable CORS
  CORS(app, supports_credentials=True)

  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(admin_bp, url_prefix='/api/admin')
  app.register_blueprint(user_bp, url_prefix='/api/user')
  app.register_blueprint(common_bp, url_prefix='/api/common')

  with app.app_context():
    db.create_all()
    seed_data()  # after creating all tables

  return app
