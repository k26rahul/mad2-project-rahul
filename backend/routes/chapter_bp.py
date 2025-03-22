from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, Chapter, Subject

chapter_bp = Blueprint('chapter', __name__)


@chapter_bp.route('/get/<int:id>', methods=['GET'])
@roles_required('admin', 'user')
def get_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  chapter_dict = chapter.as_dict()
  return jsonify(success=True, chapter=chapter_dict)


@chapter_bp.route('/create', methods=['POST'])
@roles_required('admin')
def create_chapter():
  data = request.get_json()
  name = data.get('name')
  description = data.get('description')  # optional
  subject_id = data.get('subject_id')

  if not all([name, subject_id]):
    return jsonify(
        success=False,
        message="name and subject_id are required; optional fields: description"
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


@chapter_bp.route('/update/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  data = request.get_json()

  chapter.name = data.get('name', chapter.name)
  chapter.description = data.get('description', chapter.description)

  db.session.commit()
  return jsonify(success=True, chapter=chapter.as_dict())


@chapter_bp.route('/delete/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_chapter(id):
  chapter = Chapter.query.get_or_404(id)
  db.session.delete(chapter)
  db.session.commit()
  return jsonify(success=True, message="Chapter deleted successfully")
