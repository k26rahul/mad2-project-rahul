from flask_security.utils import hash_password
from db.models import db, Role, User


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
        roles=[admin_role]
    )
    db.session.add(admin_user)
    db.session.commit()

  if not User.query.filter_by(email="user@example.com").first():
    print("Seeding user...")
    user = User(
        email="user@example.com",
        password=hash_password("12345"),
        roles=[user_role]
    )
    db.session.add(user)
    db.session.commit()
