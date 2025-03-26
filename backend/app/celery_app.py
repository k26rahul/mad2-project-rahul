from celery import Celery
from flask_mail import Mail
from flask import Flask
from celery.schedules import crontab
from app import app

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


def register_tasks():
  import app.celery_tasks


mail = Mail(app)
celery = make_celery(app)
register_tasks()

# Add Celery Beat schedule
celery.conf.beat_schedule = {
    'send-daily-reminders': {
        'task': 'app.celery_tasks.send_daily_reminders',
        'schedule': crontab(hour=8, minute=0),  # Run at 8 AM daily
        # 'schedule': 5.0,  # For testing
    },
    'send-monthly-reports': {
        'task': 'app.celery_tasks.send_monthly_reports',
        'schedule': crontab(day_of_month=1, hour=9, minute=0),  # Run at 9 AM on 1st of every month
        # 'schedule': 5.0,  # For testing
    },
}
