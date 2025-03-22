from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, Subject

subject_bp = Blueprint('subject', __name__)


@subject_bp.route('/get/<int:id>', methods=['GET'])
@roles_required('admin')
def get_subject(id):
  subject = Subject.query.get_or_404(id)
  subject_dict = subject.as_dict()
  subject_dict['chapters'] = [chapter.as_dict() for chapter in subject.chapters]
  return jsonify(success=True, subject=subject_dict)


@subject_bp.route('/get-all', methods=['GET'])
@roles_required('admin')
def get_subjects():
  subjects = Subject.query.all()
  result = []
  for subject in subjects:
    subject_dict = subject.as_dict()
    subject_dict['chapters'] = [chapter.as_dict() for chapter in subject.chapters]
    result.append(subject_dict)
  return jsonify(success=True, subjects=result)


@subject_bp.route('/create', methods=['POST'])
@roles_required('admin')
def create_subject():
  data = request.get_json()
  name = data.get('name')
  description = data.get('description')  # optional

  if not name:
    return jsonify(success=False, message="name is required; optional fields: description"), 400

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


@subject_bp.route('/update/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_subject(id):
  subject = Subject.query.get_or_404(id)
  data = request.get_json()

  subject.name = data.get('name', subject.name)
  subject.description = data.get('description', subject.description)

  db.session.commit()
  return jsonify(success=True, subject=subject.as_dict())


@subject_bp.route('/delete/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_subject(id):
  subject = Subject.query.get_or_404(id)
  db.session.delete(subject)
  db.session.commit()
  return jsonify(success=True, message="Subject deleted successfully")
