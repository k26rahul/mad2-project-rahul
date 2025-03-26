from flask import render_template
from flask_mail import Message
from app.celery_app import celery, mail, app
from db.models import User, Quiz, Role, QuizAttempt
from datetime import datetime, timedelta


@celery.task
def send_email_task(to, subject, body, is_html=False):
  msg = Message(subject, recipients=[to])
  if is_html:
    msg.html = body
  else:
    msg.body = body
  mail.send(msg)


@celery.task
def send_daily_reminders():
  print("Starting daily reminder emails task...")

  users = User.query.join(User.roles).filter(Role.name == 'user').all()
  for user in users:
    # Fetch quizzes created since the user's last login
    new_quizzes = Quiz.query.filter(Quiz.created_at > user.last_login).all()
    if not new_quizzes:
      print(f"Skipping email for user {user.name} ({user.email}) - No new quizzes")
      continue

    # Render email template
    with app.app_context():
      email_body = render_template('email/daily_reminder.html',
                                   name=user.name,
                                   last_login=user.last_login.strftime("%I:%M %p on %B %d, %Y"),
                                   quizzes=new_quizzes
                                   )

    print(f"Sending email to user {user.name} ({user.email}) about {len(new_quizzes)} new quizzes")
    send_email_task.delay(user.email, "New Quizzes Available!", email_body, is_html=True)

  print("Daily reminder emails task completed!")


@celery.task
def send_monthly_reports():
  print("Starting monthly activity report task...")

  one_month_ago = datetime.now() - timedelta(days=30)

  users = User.query.join(User.roles).filter(Role.name == 'user').all()

  for user in users:
    # Get all attempts in last month
    user_attempts = QuizAttempt.query.filter(
        QuizAttempt.user_id == user.id,
        QuizAttempt.attempted_at >= one_month_ago
    ).all()

    if not user_attempts:
      print(f"No activity for user {user.name} in the last month")
      continue

    # Get new quizzes created in last month
    new_quizzes = Quiz.query.filter(Quiz.created_at >= one_month_ago).count()

    # Group attempts by subject and chapter
    subject_stats = {}
    total_score = 0
    total_questions = 0

    for attempt in user_attempts:
      quiz = attempt.quiz
      chapter = quiz.chapter
      subject = chapter.subject.name

      if subject not in subject_stats:
        subject_stats[subject] = {
            'chapters': {},
            'total_score': 0,
            'total_questions': 0
        }

      chapter_name = chapter.name
      if chapter_name not in subject_stats[subject]['chapters']:
        subject_stats[subject]['chapters'][chapter_name] = {
            'attempts': [],
            'score': 0,
            'total': 0
        }

      # Get total questions in quiz
      quiz_total = len(quiz.questions)

      # Get ranking for this attempt
      all_attempts = QuizAttempt.query.filter_by(quiz_id=quiz.id).order_by(QuizAttempt.score.desc()).all()
      user_rank = next(i for i, a in enumerate(all_attempts, 1) if a.id == attempt.id)

      attempt_data = {
          'quiz_title': quiz.title,
          'score': attempt.score,
          'total': quiz_total,
          'percentage': (attempt.score / quiz_total * 100) if quiz_total > 0 else 0,
          'rank': user_rank,
          'total_attempts': len(all_attempts)
      }

      subject_stats[subject]['chapters'][chapter_name]['attempts'].append(attempt_data)
      subject_stats[subject]['chapters'][chapter_name]['score'] += attempt.score
      subject_stats[subject]['chapters'][chapter_name]['total'] += quiz_total

      subject_stats[subject]['total_score'] += attempt.score
      subject_stats[subject]['total_questions'] += quiz_total

      total_score += attempt.score
      total_questions += quiz_total

    # Calculate overall average
    average_score = (total_score / total_questions * 100) if total_questions > 0 else 0

    with app.app_context():
      email_body = render_template(
          'email/monthly_report.html',
          name=user.name,
          month=datetime.now().strftime('%B %Y'),
          new_quizzes=new_quizzes,
          total_attempts=len(user_attempts),
          average_score=average_score,
          subject_stats=subject_stats
      )

    print(f"Sending monthly report to {user.name} ({user.email})")
    send_email_task.delay(
        user.email,
        f"Monthly Activity Report - {datetime.now().strftime('%B %Y')}",
        email_body,
        is_html=True
    )

  print("Monthly activity reports task completed!")
