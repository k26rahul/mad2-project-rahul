from flask import Blueprint, jsonify, request
from flask_security import roles_required, roles_accepted
from db.models import db, Subject

subject_bp = Blueprint('subject', __name__)


def _construct_subject_dict(subject):
  subject_dict = subject.as_dict()
  subject_dict['chapters'] = [chapter.id for chapter in subject.chapters]
  return subject_dict


@subject_bp.route('/get/<int:id>', methods=['GET'])
@roles_accepted('admin', 'user')
def get(id):
  subject = Subject.query.get_or_404(id)
  return jsonify(success=True, subject=_construct_subject_dict(subject))


@subject_bp.route('/get-all', methods=['GET'])
@roles_accepted('admin', 'user')
def get_all():
  subjects = Subject.query.all()
  result = [_construct_subject_dict(subject) for subject in subjects]
  return jsonify(success=True, subjects=result)


@subject_bp.route('/create', methods=['POST'])
@roles_required('admin')
def create():
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
      subject=_construct_subject_dict(subject),
      message="Subject created successfully"
  )


@subject_bp.route('/update/<int:id>', methods=['PUT'])
@roles_required('admin')
def update(id):
  subject = Subject.query.get_or_404(id)
  data = request.get_json()

  subject.name = data.get('name', subject.name)
  subject.description = data.get('description', subject.description)

  db.session.commit()
  return jsonify(
      success=True,
      subject=_construct_subject_dict(subject),
      message="Subject updated successfully"
  )


@subject_bp.route('/delete/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete(id):
  subject = Subject.query.get_or_404(id)
  db.session.delete(subject)
  db.session.commit()
  return jsonify(success=True, message="Subject deleted successfully")
