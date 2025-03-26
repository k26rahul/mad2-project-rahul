from flask_mail import Message
from app.celery_app import celery, mail, app
from db.models import User, Quiz
from datetime import datetime


@celery.task
def send_email_task(to, subject, body):
  with app.app_context():
    msg = Message(subject, recipients=[to], body=body)
    mail.send(msg)


@celery.task
def send_daily_reminders():
  with app.app_context():
    users = User.query.all()
    for user in users:
      if not user.last_login:
        continue  # Skip users who have never logged in

      # Fetch quizzes created since the user's last login
      new_quizzes = Quiz.query.filter(Quiz.created_at > user.last_login).all()
      if not new_quizzes:
        continue  # Skip if no new quizzes

      # Prepare email content
      quiz_list = "\n".join([f"- {quiz.title}" for quiz in new_quizzes])
      email_body = f"Hi {user.name},\n\nHere are the new quizzes since your last login:\n\n{quiz_list}\n\nHappy learning!"

      # Send email
      send_email_task.delay(user.email, "New Quizzes Available!", email_body)
