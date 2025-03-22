from flask import Flask, jsonify
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from .config import Config
from db.models import db, User, Role
from db.seed import seed_data
from .blueprints import register_blueprints
from .error_handlers import register_error_handlers

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  Security(app, user_datastore, register_blueprint=False)

  CORS(app, supports_credentials=True)

  register_blueprints(app)
  register_error_handlers(app)

  with app.app_context():
    db.create_all()
    seed_data()

  return app
