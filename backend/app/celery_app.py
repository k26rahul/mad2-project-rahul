from celery import Celery
from flask_mail import Mail
from flask import Flask


def make_celery(app):
  celery = Celery(
      app.import_name,
      backend=app.config['CELERY_RESULT_BACKEND'],
      broker=app.config['CELERY_BROKER_URL']
  )
  celery.conf.update(app.config)
  return celery


def create_app():
  app = Flask(__name__)
  app.config.update(
      CELERY_BROKER_URL='redis://localhost:6380/0',
      CELERY_RESULT_BACKEND='redis://localhost:6380/0',
      MAIL_SERVER='localhost',
      MAIL_PORT=1025,
      MAIL_USERNAME='',
      MAIL_PASSWORD='',
      MAIL_USE_TLS=False,
      MAIL_USE_SSL=False,
      MAIL_DEFAULT_SENDER='noreply@example.com'
  )
  return app


def register_tasks():
  import app.celery_tasks


app = create_app()
mail = Mail(app)
celery = make_celery(app)
register_tasks()
