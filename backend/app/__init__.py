from flask import Flask
from .config import Config
from flask_security import Security, SQLAlchemyUserDatastore
from db.models import db, User, Role

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  Security(app, user_datastore, register_blueprint=False)

  with app.app_context():
    db.create_all()

  return app
