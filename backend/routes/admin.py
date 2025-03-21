from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, Subject, Chapter, Quiz, Question

admin_bp = Blueprint('admin', __name__)

# Quiz Routes


@admin_bp.route('/get-quiz/<int:id>', methods=['GET'])
@roles_required('admin')
def get_quiz(id):
  quiz = Quiz.query.get_or_404(id)
  quiz_dict = quiz.as_dict()
  quiz_dict['chapter_name'] = quiz.chapter.name
  quiz_dict['subject_name'] = quiz.chapter.subject.name
  quiz_dict['questions'] = [q.as_dict() for q in quiz.questions]
  return jsonify(success=True, quiz=quiz_dict)


@admin_bp.route('/get-quizzes', methods=['GET'])
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


@admin_bp.route('/create-quiz', methods=['POST'])
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


@admin_bp.route('/update-quiz/<int:id>', methods=['PUT'])
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


@admin_bp.route('/delete-quiz/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_quiz(id):
  quiz = Quiz.query.get_or_404(id)
  db.session.delete(quiz)
  db.session.commit()
  return jsonify(success=True, message="Quiz deleted successfully")


# Question Routes
@admin_bp.route('/get-question/<int:id>', methods=['GET'])
@roles_required('admin')
def get_question(id):
  question = Question.query.get_or_404(id)
  question_dict = question.as_dict()
  question_dict['quiz_title'] = question.quiz.title
  question_dict['chapter_name'] = question.quiz.chapter.name
  question_dict['subject_name'] = question.quiz.chapter.subject.name
  return jsonify(success=True, question=question_dict)


@admin_bp.route('/create-question', methods=['POST'])
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
    return jsonify(success=False, message="All question fields are required"), 400

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


@admin_bp.route('/update-question/<int:id>', methods=['PUT'])
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


@admin_bp.route('/delete-question/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_question(id):
  question = Question.query.get_or_404(id)
  db.session.delete(question)
  db.session.commit()
  return jsonify(success=True, message="Question deleted successfully")

# Subject Routes


@admin_bp.route('/get-subject/<int:id>', methods=['GET'])
@roles_required('admin')
def get_subject(id):
  subject = Subject.query.get_or_404(id)
  subject_dict = subject.as_dict()
  subject_dict['chapters'] = [chapter.as_dict() for chapter in subject.chapters]
  return jsonify(success=True, subject=subject_dict)


@admin_bp.route('/get-subjects', methods=['GET'])
@roles_required('admin')
def get_subjects():
  subjects = Subject.query.all()
  result = []
  for subject in subjects:
    subject_dict = subject.as_dict()
    subject_dict['chapters'] = [chapter.as_dict() for chapter in subject.chapters]
    result.append(subject_dict)
  return jsonify(success=True, subjects=result)


@admin_bp.route('/create-subject', methods=['POST'])
@roles_required('admin')
def create_subject():
  data = request.get_json()
  name = data.get('name')
  description = data.get('description')

  if not name:
    return jsonify(success=False, message="Subject name is required"), 400

  subject = Subject(
      name=name,
      description=description
  )
  db.session.add(subject)
  db.session.commit()

  return jsonify(
      success=True,
      subject=subject.as_dict(),
      message="Subject created successfully"
  )


@admin_bp.route('/update-subject/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_subject(id):
  subject = Subject.query.get_or_404(id)
  data = request.get_json()

  subject.name = data.get('name', subject.name)
  subject.description = data.get('description', subject.description)

  db.session.commit()
  return jsonify(success=True, subject=subject.as_dict())


@admin_bp.route('/delete-subject/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_subject(id):
  subject = Subject.query.get_or_404(id)
  db.session.delete(subject)
  db.session.commit()
  return jsonify(success=True, message="Subject deleted successfully")


# Chapter Routes

@admin_bp.route('/get-chapter/<int:id>', methods=['GET'])
@roles_required('admin')
def get_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  chapter_dict = chapter.as_dict()
  return jsonify(success=True, chapter=chapter_dict)


@admin_bp.route('/create-chapter', methods=['POST'])
@roles_required('admin')
def create_chapter():
  data = request.get_json()
  name = data.get('name')
  description = data.get('description')
  subject_id = data.get('subject_id')

  if not all([name, subject_id]):
    return jsonify(
        success=False,
        message="Chapter name and subject_id are required"
    ), 400

  subject = Subject.query.get(subject_id)
  if not subject:
    return jsonify(
        success=False,
        message=f"Subject with id {subject_id} not found"
    ), 404

  chapter = Chapter(
      name=name,
      description=description,
      subject_id=subject_id
  )
  db.session.add(chapter)
  db.session.commit()

  return jsonify(
      success=True,
      chapter=chapter.as_dict(),
      message="Chapter created successfully"
  )


@admin_bp.route('/update-chapter/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  data = request.get_json()

  chapter.name = data.get('name', chapter.name)
  chapter.description = data.get('description', chapter.description)

  db.session.commit()
  return jsonify(success=True, chapter=chapter.as_dict())


@admin_bp.route('/delete-chapter/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  db.session.delete(chapter)
  db.session.commit()
  return jsonify(success=True, message="Chapter deleted successfully")
