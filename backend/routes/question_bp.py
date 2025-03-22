from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, Question, Quiz

question_bp = Blueprint('question', __name__)


@question_bp.route('/get/<int:id>', methods=['GET'])
@roles_required('admin', 'user')
def get_question(id):
  question = Question.query.get_or_404(id)
  question_dict = question.as_dict()
  question_dict['quiz_title'] = question.quiz.title
  question_dict['chapter_name'] = question.quiz.chapter.name
  question_dict['subject_name'] = question.quiz.chapter.subject.name
  return jsonify(success=True, question=question_dict)


@question_bp.route('/create', methods=['POST'])
@roles_required('admin')
def create_question():
  data = request.get_json()
  statement = data.get('statement')
  option_a = data.get('option_a')
  option_b = data.get('option_b')
  option_c = data.get('option_c')
  option_d = data.get('option_d')
  correct_option = data.get('correct_option')
  quiz_id = data.get('quiz_id')

  if not all([statement, option_a, option_b, option_c, option_d, correct_option, quiz_id]):
    return jsonify(success=False, message="statement, option_a, option_b, option_c, option_d, correct_option, and quiz_id are required"), 400

  quiz = Quiz.query.get(quiz_id)
  if not quiz:
    return jsonify(success=False, message=f"Quiz with id {quiz_id} not found"), 404

  question = Question(
      statement=statement,
      option_a=option_a,
      option_b=option_b,
      option_c=option_c,
      option_d=option_d,
      correct_option=correct_option,
      quiz_id=quiz_id
  )
  db.session.add(question)
  db.session.commit()

  return jsonify(success=True, question=question.as_dict(), message="Question created successfully")


@question_bp.route('/update/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_question(id):
  question = Question.query.get_or_404(id)
  data = request.get_json()

  question.statement = data.get('statement', question.statement)
  question.option_a = data.get('option_a', question.option_a)
  question.option_b = data.get('option_b', question.option_b)
  question.option_c = data.get('option_c', question.option_c)
  question.option_d = data.get('option_d', question.option_d)
  question.correct_option = data.get('correct_option', question.correct_option)

  db.session.commit()
  return jsonify(success=True, question=question.as_dict())


@question_bp.route('/delete/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_question(id):
  question = Question.query.get_or_404(id)
  db.session.delete(question)
  db.session.commit()
  return jsonify(success=True, message="Question deleted successfully")
