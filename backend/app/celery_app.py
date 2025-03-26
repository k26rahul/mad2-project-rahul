from celery import Celery
from flask_mail import Mail
from flask import Flask
from celery.schedules import crontab
from app import app


def make_celery(app):
  celery = Celery(
      app.import_name,
      backend=app.config['result_backend'],
      broker=app.config['broker_url']
  )
  celery.conf.update(app.config)

  # Wrap tasks to run within the Flask app context
  class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return self.run(*args, **kwargs)

  celery.Task = ContextTask
  return celery


def create_app():
  # app = Flask(__name__)
  app.config.update(
      broker_url='redis://localhost:6380/0',  # New key for CELERY_BROKER_URL
      result_backend='redis://localhost:6380/0',  # New key for CELERY_RESULT_BACKEND
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

# Add Celery Beat schedule
celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'app.celery_tasks.send_daily_reminders',
        'schedule': 5.0,  # For testing. Change to crontab(hour=8, minute=0) for 8 AM daily.
    },
}
