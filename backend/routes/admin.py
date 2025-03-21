from flask import Blueprint, jsonify
from flask_security import roles_required
from db.models import Subject

admin_bp = Blueprint('admin', __name__)


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
