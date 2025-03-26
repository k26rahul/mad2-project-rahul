from celery import Celery
from flask import Flask
from flask_mail import Mail, Message


def create_celery_app(app):
  celery = Celery(
      app.import_name,
      broker='redis://localhost:6379/0',
      backend='redis://localhost:6379/0'
  )
  celery.conf.update(app.config)

  class ContextTask(celery.Task):
    def __call__(self, *args, **kwargs):
      with app.app_context():
        return self.run(*args, **kwargs)

  celery.Task = ContextTask
  return celery


# Initialize Flask
app = Flask(__name__)
app.config.update(
    MAIL_SERVER="localhost",
    MAIL_PORT=1025,
    MAIL_USE_TLS=False,
    MAIL_USE_SSL=False,
    MAIL_DEFAULT_SENDER="noreply@example.com",
    # Celery configuration
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_TASK_SERIALIZER='json',
    CELERY_ACCEPT_CONTENT=['json'],
    CELERY_RESULT_SERIALIZER='json',
    TIMEZONE='UTC',
    CELERY_ENABLE_UTC=True,
)

# Initialize Flask-Mail
mail = Mail(app)

# Initialize Celery with Flask app
celery = create_celery_app(app)


@celery.task
def send_email(recipient, subject, body):
  msg = Message(subject, recipients=[recipient], body=body)
  mail.send(msg)
  return f"Email sent to {recipient}"
