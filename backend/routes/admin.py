from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, Subject, Chapter

admin_bp = Blueprint('admin', __name__)

# Subject Routes


@admin_bp.route('/subjects', methods=['GET'])
@roles_required('admin')
def get_subjects():
  subjects = Subject.query.all()
  result = []
  for subject in subjects:
    subject_dict = subject.as_dict()
    subject_dict['chapters'] = [chapter.as_dict() for chapter in subject.chapters]
    result.append(subject_dict)
  return jsonify(success=True, subjects=result)


@admin_bp.route('/subjects', methods=['POST'])
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


@admin_bp.route('/subjects/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_subject(id):
  subject = Subject.query.get_or_404(id)
  data = request.get_json()

  subject.name = data.get('name', subject.name)
  subject.description = data.get('description', subject.description)

  db.session.commit()
  return jsonify(success=True, subject=subject.as_dict())


@admin_bp.route('/subjects/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_subject(id):
  subject = Subject.query.get_or_404(id)
  db.session.delete(subject)
  db.session.commit()
  return jsonify(success=True, message="Subject deleted successfully")


@admin_bp.route('/subjects/<int:id>', methods=['GET'])
@roles_required('admin')
def get_subject(id):
  subject = Subject.query.get_or_404(id)
  subject_dict = subject.as_dict()
  subject_dict['chapters'] = [chapter.as_dict() for chapter in subject.chapters]
  return jsonify(success=True, subject=subject_dict)


# Chapter Routes
@admin_bp.route('/chapters', methods=['POST'])
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


@admin_bp.route('/chapters/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  data = request.get_json()

  chapter.name = data.get('name', chapter.name)
  chapter.description = data.get('description', chapter.description)

  db.session.commit()
  return jsonify(success=True, chapter=chapter.as_dict())


@admin_bp.route('/chapters/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  db.session.delete(chapter)
  db.session.commit()
  return jsonify(success=True, message="Chapter deleted successfully")
