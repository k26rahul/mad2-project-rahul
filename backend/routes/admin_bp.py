from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, User
from sqlalchemy import func
from db.models import Subject, Chapter, Quiz, Question, QuizAttempt
from db.seed import seed_data
from app.cache import cache

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/test-cache')
@cache.cached(timeout=5)
def test_cache():
  from datetime import datetime
  from flask import jsonify
  return jsonify(
      time=str(datetime.now()),
  )


def _construct_user_dict(user):
  user_dict = user.as_dict()
  del user_dict['password']
  del user_dict['fs_uniquifier']
  user_dict['role'] = user.roles[0].name
  user_dict['total_attempts'] = QuizAttempt.query.filter_by(user_id=user.id).count()
  return user_dict


@admin_bp.route('/users/<int:id>', methods=['GET'])
@roles_required('admin')
def get_user(id):
  user = User.query.get_or_404(id)
  return jsonify(success=True, user=_construct_user_dict(user))


@admin_bp.route('/users', methods=['GET'])
@roles_required('admin')
def get_all_users():
  users = User.query.all()
  result = [_construct_user_dict(user) for user in users]
  return jsonify(success=True, users=result)


@admin_bp.route('/users/<int:id>/block', methods=['PUT'])
@roles_required('admin')
def block_user(id):
  user = User.query.get_or_404(id)

  if user.roles[0].name == 'admin':
    return jsonify(
        success=False,
        message="Cannot block admin users"
    ), 403

  user.active = False
  user.fs_uniquifier = None  # Invalidate user's session
  db.session.commit()

  return jsonify(
      success=True,
      user=_construct_user_dict(user),
      message="User blocked successfully"
  )


@admin_bp.route('/users/<int:id>/unblock', methods=['PUT'])
@roles_required('admin')
def unblock_user(id):
  user = User.query.get_or_404(id)
  user.active = True
  db.session.commit()

  return jsonify(
      success=True,
      user=_construct_user_dict(user),
      message="User unblocked successfully"
  )


@admin_bp.route('/statistics', methods=['GET'])
@roles_required('admin')
def get_statistics():
  # Subject wise statistics
  # First get attempts with their scores and question counts
  attempts_with_scores = db.session.query(
      Subject.name,
      QuizAttempt.score,
      func.count(Question.id).label('question_count')
  ).join(Chapter, Subject.id == Chapter.subject_id) \
   .join(Quiz, Chapter.id == Quiz.chapter_id) \
   .join(QuizAttempt, Quiz.id == QuizAttempt.quiz_id) \
   .join(Question, Question.quiz_id == Quiz.id) \
   .group_by(QuizAttempt.id).all()

  # print(attempts_with_scores)
  # [('Mathematics', 5, 5), ('Mathematics', 4, 5), ('Mathematics', 3, 5), ('Mathematics', 2, 5), ('Mathematics', 1, 5), ('Mathematics', 5, 5)]

  # Equivalent SQL:
  # SELECT subject.name, quiz_attempt.score, COUNT(question.id) as question_count
  # FROM subject
  # JOIN chapter ON subject.id = chapter.subject_id
  # JOIN quiz ON chapter.id = quiz.chapter_id
  # JOIN quiz_attempt ON quiz.id = quiz_attempt.quiz_id
  # JOIN question ON question.quiz_id = quiz.id
  # GROUP BY quiz_attempt.id;

  # Process the results to get subject statistics
  subject_stats = {}
  for name, score, question_count in attempts_with_scores:
    if name not in subject_stats:
      subject_stats[name] = {
          'name': name,
          'attempts': 0,
          'top_percentage': 0
      }

    subject_stats[name]['attempts'] += 1
    percentage = (score * 100.0) / question_count if question_count > 0 else 0
    subject_stats[name]['top_percentage'] = max(
        subject_stats[name]['top_percentage'],
        percentage
    )

  subject_data = list(subject_stats.values())

  return jsonify({
      'success': True,
      'counts': {
          'subjects': Subject.query.count(),
          'chapters': Chapter.query.count(),
          'quizzes': Quiz.query.count(),
          'attempts': QuizAttempt.query.count(),
          'questions': Question.query.count(),
      },
      'subject_statistics': subject_data
  })


@admin_bp.route('/repopulate', methods=['POST'])
@roles_required('admin')
def repopulate_database():
  try:
    # Drop all tables
    db.drop_all()
    # Recreate all tables
    db.create_all()
    # Reseed the database
    seed_data()

    return jsonify(
        success=True,
        message="Database successfully repopulated"
    )
  except Exception as e:
    return jsonify(
        success=False,
        message=f"Failed to repopulate database: {str(e)}"
    ), 500
