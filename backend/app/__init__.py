from flask import Flask
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore
from .config import Config
from db.models import db, User, Role
from db.seed import seed_data


user_datastore = SQLAlchemyUserDatastore(db, User, Role)


def create_app():
  app = Flask(__name__)
  app.config.from_object(Config)

  db.init_app(app)
  Security(app, user_datastore, register_blueprint=False)

  CORS(app, supports_credentials=True)

  register_blueprints(app)

  with app.app_context():
    db.create_all()
    seed_data()

  return app


def register_blueprints(app):
  from routes.auth_bp import auth_bp
  from routes.admin_bp import admin_bp
  from routes.user_bp import user_bp
  from routes.subject_bp import subject_bp
  from routes.chapter_bp import chapter_bp
  from routes.quiz_bp import quiz_bp
  from routes.question_bp import question_bp

  app.register_blueprint(auth_bp, url_prefix='/api/auth')
  app.register_blueprint(admin_bp, url_prefix='/api/admin')
  app.register_blueprint(user_bp, url_prefix='/api/user')
  app.register_blueprint(subject_bp, url_prefix='/api/subject')
  app.register_blueprint(chapter_bp, url_prefix='/api/chapter')
  app.register_blueprint(quiz_bp, url_prefix='/api/quiz')
  app.register_blueprint(question_bp, url_prefix='/api/question')
