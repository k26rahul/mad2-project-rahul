from flask_mail import Message
from app.celery_app import celery, mail, app


@celery.task
def send_email_task(to, subject, body):
  with app.app_context():
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)
