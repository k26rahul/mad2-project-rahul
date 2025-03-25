from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db, User

admin_bp = Blueprint('admin', __name__)


def _construct_user_dict(user):
  user_dict = user.as_dict()
  del user_dict['password']
  del user_dict['fs_uniquifier']
  user_dict['role'] = user.roles[0].name
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
