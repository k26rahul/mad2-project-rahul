from flask_security.utils import hash_password
from db.models import db, Role, User, Subject, Chapter, Quiz, Question
from .data_subjects import data_subjects
from .data_quizzes import data_quizzes


def seed_data():
  if not Role.query.first():
    print("Seeding roles...")
    db.session.add(Role(name="admin"))
    db.session.add(Role(name="user"))
    db.session.commit()

  admin_role = Role.query.filter_by(name="admin").first()
  user_role = Role.query.filter_by(name="user").first()

  if not User.query.filter_by(email="admin@example.com").first():
    print("Seeding admin user...")
    admin_user = User(
        email="admin@example.com",
        password=hash_password("12345"),
        name="Admin User",
        roles=[admin_role]
    )
    db.session.add(admin_user)
    db.session.commit()

  if not User.query.filter_by(email="user@example.com").first():
    print("Seeding user...")
    user = User(
        email="user@example.com",
        password=hash_password("12345"),
        name="Regular User",
        roles=[user_role]
    )
    db.session.add(user)
    db.session.commit()

  if not Subject.query.first():
    print("Seeding subjects and chapters...")
    for subject_data in data_subjects:
      subject = Subject(
          name=subject_data["name"],
          description=subject_data["description"]
      )
      db.session.add(subject)
      db.session.flush()  # Flush to get subject.id

      for chapter_data in subject_data["chapters"]:
        chapter = Chapter(
            name=chapter_data["name"],
            description=chapter_data["description"],
            subject_id=subject.id
        )
        db.session.add(chapter)

    db.session.commit()

  if not Quiz.query.first():
    print("Seeding quizzes and questions...")
    for subject_name, chapters in data_quizzes.items():
      subject = Subject.query.filter_by(name=subject_name).first()
      if not subject:
        continue

      for chapter_name, quizzes in chapters.items():
        chapter = Chapter.query.filter_by(name=chapter_name, subject_id=subject.id).first()
        if not chapter:
          continue

        for quiz_data in quizzes:
          quiz = Quiz(
              title=quiz_data["title"],
              description=quiz_data["description"],
              chapter_id=chapter.id
          )
          db.session.add(quiz)
          db.session.flush()

          for q_data in quiz_data["questions"]:
            question = Question(
                statement=q_data["statement"],
                option_a=q_data["option_a"],
                option_b=q_data["option_b"],
                option_c=q_data["option_c"],
                option_d=q_data["option_d"],
                correct_option=q_data["correct_option"],
                quiz_id=quiz.id
            )
            db.session.add(question)

    db.session.commit()
