from flask_security.utils import hash_password
from db.models import db, Role, User, Subject, Chapter
from .data import seed_subjects


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

  # Seed subjects and chapters if none exist
  if not Subject.query.first():
    print("Seeding subjects and chapters...")
    for subject_data in seed_subjects:
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
