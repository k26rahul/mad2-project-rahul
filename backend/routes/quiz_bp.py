from flask import Blueprint, jsonify, request
from flask_security import roles_required, roles_accepted
from db.models import db, Quiz, Chapter
from datetime import datetime

quiz_bp = Blueprint('quiz', __name__)


def _construct_quiz_dict(quiz):
  quiz_dict = quiz.as_dict()
  quiz_dict['chapter_name'] = quiz.chapter.name
  quiz_dict['subject_name'] = quiz.chapter.subject.name
  quiz_dict['questions'] = [q.id for q in quiz.questions]
  return quiz_dict


@quiz_bp.route('/get/<int:id>', methods=['GET'])
@roles_accepted('admin', 'user')
def get(id):
  quiz = Quiz.query.get_or_404(id)
  return jsonify(success=True, quiz=_construct_quiz_dict(quiz))


@quiz_bp.route('/get-all', methods=['GET'])
@roles_accepted('admin', 'user')
def get_all():
  quizzes = Quiz.query.all()
  result = [_construct_quiz_dict(quiz) for quiz in quizzes]
  return jsonify(success=True, quizzes=result)


@quiz_bp.route('/create', methods=['POST'])
@roles_required('admin')
def create():
  data = request.get_json()
  title = data.get('title')
  chapter_id = data.get('chapter_id')
  description = data.get('description')  # optional
  start_time = datetime.fromisoformat(data.get('start_time')) if data.get('start_time') else None  # optional
  duration = data.get('duration')  # optional

  if not all([title, chapter_id]):
    return jsonify(success=False, message="title and chapter_id are required; optional fields: description, start_time, duration"), 400

  chapter = Chapter.query.get(chapter_id)
  if not chapter:
    return jsonify(success=False, message=f"Chapter with id {chapter_id} not found"), 404

  quiz = Quiz(
      title=title,
      description=description,
      chapter_id=chapter_id,
      start_time=start_time,
      duration=duration
  )
  db.session.add(quiz)
  db.session.commit()

  return jsonify(success=True, quiz=quiz.as_dict(), message="Quiz created successfully")


@quiz_bp.route('/update/<int:id>', methods=['PUT'])
@roles_required('admin')
def update(id):
  quiz = Quiz.query.get_or_404(id)
  data = request.get_json()

  quiz.title = data.get('title', quiz.title)
  quiz.description = data.get('description', quiz.description)
  quiz.start_time = data.get('start_time', quiz.start_time)
  quiz.duration = data.get('duration', quiz.duration)

  db.session.commit()
  return jsonify(success=True, quiz=quiz.as_dict(), message="Quiz updated successfully")


@quiz_bp.route('/delete/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete(id):
  quiz = Quiz.query.get_or_404(id)
  db.session.delete(quiz)
  db.session.commit()
  return jsonify(success=True, message="Quiz deleted successfully")
