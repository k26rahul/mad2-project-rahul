import enum
import uuid
from datetime import datetime
from typing import Optional

from flask_security import RoleMixin, UserMixin
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Table, Integer, Enum, String
from sqlalchemy.orm import Mapped, relationship, mapped_column

db = SQLAlchemy()


class Base(db.Model):
  __abstract__ = True

  def as_dict(self):
    result = {}
    for c in self.__table__.columns:
      result[c.name] = getattr(self, c.name)
    return result


# association table for many-to-many relationship between users and roles
user_roles = Table(
    'user_roles',
    db.metadata,
    Column('user_id', Integer, ForeignKey('users.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('roles.id'), primary_key=True)
)


class Role(Base, RoleMixin):
  __tablename__ = 'roles'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

  users: Mapped[list["User"]] = relationship(
      "User",
      secondary=user_roles,
      back_populates="roles"
  )


class User(Base, UserMixin):
  __tablename__ = 'users'

  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  active: Mapped[bool] = mapped_column(default=True)
  fs_uniquifier: Mapped[str] = mapped_column(
      String(255), unique=True, nullable=False, default=lambda: str(uuid.uuid4())
  )

  roles: Mapped[list['Role']] = relationship(
      "Role",
      secondary=user_roles,
      back_populates="users"
  )
