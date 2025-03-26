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
    Column('user_id', Integer, ForeignKey('user.id'), primary_key=True),
    Column('role_id', Integer, ForeignKey('role.id'), primary_key=True)
)


class Role(Base, RoleMixin):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)

  users: Mapped[list["User"]] = relationship(
      "User",
      secondary=user_roles,
      back_populates="roles"
  )


class User(Base, UserMixin):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
  password: Mapped[str] = mapped_column(String(255), nullable=False)
  active: Mapped[bool] = mapped_column(default=True)
  fs_uniquifier: Mapped[str] = mapped_column(
      String(255), unique=True, nullable=True, default=lambda: str(uuid.uuid4())
  )
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  dob: Mapped[Optional[datetime]] = mapped_column(nullable=True)
  qualification: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
  last_login: Mapped[Optional[datetime]] = mapped_column(
      nullable=True, default=lambda: datetime.now()
  )

  roles: Mapped[list['Role']] = relationship(
      "Role",
      secondary=user_roles,
      back_populates="users"
  )
  quiz_attempts: Mapped[list["QuizAttempt"]] = relationship("QuizAttempt", back_populates="user")


class Subject(Base):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  description: Mapped[Optional[str]] = mapped_column(String(500))
  created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

  chapters: Mapped[list["Chapter"]] = relationship("Chapter", back_populates="subject", cascade="all, delete-orphan")


class Chapter(Base):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  name: Mapped[str] = mapped_column(String(100), nullable=False)
  description: Mapped[Optional[str]] = mapped_column(String(500))
  subject_id: Mapped[int] = mapped_column(ForeignKey('subject.id'))
  created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

  subject: Mapped["Subject"] = relationship("Subject", back_populates="chapters")
  quizzes: Mapped[list["Quiz"]] = relationship("Quiz", back_populates="chapter", cascade="all, delete-orphan")


class Quiz(Base):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  title: Mapped[str] = mapped_column(String(100), nullable=False)
  description: Mapped[Optional[str]] = mapped_column(String(500))
  chapter_id: Mapped[int] = mapped_column(ForeignKey('chapter.id'))
  created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())
  start_time: Mapped[Optional[datetime]] = mapped_column(nullable=True)
  duration: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Duration in minutes

  chapter: Mapped["Chapter"] = relationship("Chapter", back_populates="quizzes")
  questions: Mapped[list["Question"]] = relationship("Question", back_populates="quiz", cascade="all, delete-orphan")
  attempts: Mapped[list["QuizAttempt"]] = relationship("QuizAttempt", back_populates="quiz")


class Question(Base):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  statement: Mapped[str] = mapped_column(String(500), nullable=False)
  option_a: Mapped[str] = mapped_column(String(255), nullable=False)
  option_b: Mapped[str] = mapped_column(String(255), nullable=False)
  option_c: Mapped[str] = mapped_column(String(255), nullable=False)
  option_d: Mapped[str] = mapped_column(String(255), nullable=False)
  correct_option: Mapped[int] = mapped_column(Integer, nullable=False)
  quiz_id: Mapped[int] = mapped_column(ForeignKey('quiz.id'))
  created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

  quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="questions")


class QuizAttempt(Base):
  id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
  user_id: Mapped[int] = mapped_column(ForeignKey('user.id'))
  quiz_id: Mapped[int] = mapped_column(ForeignKey('quiz.id'))
  score: Mapped[int] = mapped_column(Integer, nullable=False)
  attempted_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now())

  user: Mapped["User"] = relationship("User", back_populates="quiz_attempts")
  quiz: Mapped["Quiz"] = relationship("Quiz", back_populates="attempts")
