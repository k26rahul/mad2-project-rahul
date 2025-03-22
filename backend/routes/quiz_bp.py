from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, Quiz, Chapter

quiz_bp = Blueprint('quiz', __name__)


@quiz_bp.route('/get-quiz/<int:id>', methods=['GET'])
@roles_required('admin')
def get_quiz(id):
  quiz = Quiz.query.get_or_404(id)
  quiz_dict = quiz.as_dict()
  quiz_dict['chapter_name'] = quiz.chapter.name
  quiz_dict['subject_name'] = quiz.chapter.subject.name
  quiz_dict['questions'] = [q.as_dict() for q in quiz.questions]
  return jsonify(success=True, quiz=quiz_dict)


@quiz_bp.route('/get-quizzes', methods=['GET'])
@roles_required('admin')
def get_quizzes():
  quizzes = Quiz.query.all()
  result = []
  for quiz in quizzes:
    quiz_dict = quiz.as_dict()
    quiz_dict['chapter_name'] = quiz.chapter.name
    quiz_dict['subject_name'] = quiz.chapter.subject.name
    result.append(quiz_dict)
  return jsonify(success=True, quizzes=result)


@quiz_bp.route('/create-quiz', methods=['POST'])
@roles_required('admin')
def create_quiz():
  data = request.get_json()
  title = data.get('title')
  description = data.get('description')
  chapter_id = data.get('chapter_id')
  start_time = data.get('start_time')
  duration = data.get('duration')

  if not all([title, chapter_id]):
    return jsonify(success=False, message="Quiz title and chapter_id are required"), 400

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


@quiz_bp.route('/update-quiz/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_quiz(id):
  quiz = Quiz.query.get_or_404(id)
  data = request.get_json()

  quiz.title = data.get('title', quiz.title)
  quiz.description = data.get('description', quiz.description)
  quiz.start_time = data.get('start_time', quiz.start_time)
  quiz.duration = data.get('duration', quiz.duration)

  db.session.commit()
  return jsonify(success=True, quiz=quiz.as_dict())


@quiz_bp.route('/delete-quiz/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_quiz(id):
  quiz = Quiz.query.get_or_404(id)
  db.session.delete(quiz)
  db.session.commit()
  return jsonify(success=True, message="Quiz deleted successfully")
