from flask import Blueprint, request, jsonify
from flask_security import current_user, logout_user
from flask_security.utils import login_user, verify_password, hash_password
from db.models import db, Role, User
from datetime import datetime
import uuid

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/whoami', methods=['GET'])
def whoami():
  if not current_user.is_authenticated:
    return jsonify(
        success=False,
        message="You are not authenticated",
        is_authenticated=False,
    ), 401  # UNAUTHORIZED

  return jsonify(
      success=True,
      email=current_user.email,
      role=current_user.roles[0].name,
      message="You are authenticated",
      is_authenticated=True,
  )


@auth_bp.route('/login', methods=['POST'])
def login():
  data = request.get_json()
  email = data.get('email')
  password = data.get('password')
  remember_me = data.get('rememberMe', False)

  user = User.query.filter_by(email=email).first()

  if not user or not verify_password(password, user.password):
    return jsonify(
        success=False,
        message="Invalid email or password"
    ), 401

  if not user.active:
    return jsonify(
        success=False,
        message="Your account has been blocked. Please contact the administrator."
    ), 403

  user.fs_uniquifier = str(uuid.uuid4())
  user.last_login = datetime.now()  # Update last login timestamp
  db.session.commit()

  login_user(user, remember=remember_me)

  return jsonify(
      success=True,
      message="Login successful",
      role=user.roles[0].name
  )


@auth_bp.route('/register', methods=['POST'])
def register():
  data = request.get_json()
  name = data.get('name')
  email = data.get('email')
  password = data.get('password')
  dob = data.get('dob')  # optional
  qualification = data.get('qualification')  # optional

  if not all([name, email, password]):
    return jsonify(
        success=False,
        message="name, email, and password are required; optional fields: dob, qualification"
    ), 400  # BAD REQUEST

  if User.query.filter_by(email=email).first():
    return jsonify(
        success=False,
        message="Email is already registered"
    ), 400

  user = User(
      name=name,
      email=email,
      password=hash_password(password),
      dob=datetime.strptime(dob, '%Y-%m-%d') if dob else None,
      qualification=qualification,
      roles=[Role.query.filter_by(name="user").first()]
  )
  db.session.add(user)
  db.session.commit()

  login_user(user, remember=True)

  return jsonify(
      success=True,
      message="Registration successful",
      role="user",
      name=name,
      email=email
  )


@auth_bp.route('/logout', methods=['POST'])
def logout():
  if not current_user.is_authenticated:
    return jsonify(
        success=False,
        message="You are not logged in"
    ), 401

  current_user.fs_uniquifier = None
  db.session.commit()
  logout_user()

  return jsonify(
      success=True,
      message="Logged out successfully"
  )
