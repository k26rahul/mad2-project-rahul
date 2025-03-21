from flask import Blueprint, request, jsonify
from flask_security.utils import verify_password, login_user, hash_password
from flask_security import current_user
from db.models import db, Role, User
from flask_security import logout_user
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/whoami', methods=['GET'])
def whoami():
  if not current_user.is_authenticated:
    return jsonify(
        success=False,
        message="You are not authenticated"
    ), 401

  return jsonify(
      success=True,
      email=current_user.email,
      role=current_user.roles[0].name,
      message="You are authenticated"
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
  dob = data.get('dob')
  qualification = data.get('qualification')

  if not all([name, email, password, dob]):
    return jsonify(
        success=False,
        message="Some fields are missing"
    ), 400

  if User.query.filter_by(email=email).first():
    return jsonify(
        success=False,
        message="Email is already registered"
    ), 400

  user = User(
      name=name,
      email=email,
      password=hash_password(password),
      dob=datetime.strptime(dob, '%Y-%m-%d'),
      qualification=qualification,
      roles=[Role.query.filter_by(name="user").first()]
  )
  db.session.add(user)
  db.session.commit()

  login_user(user)

  return jsonify(
      success=True,
      message="Registration successful",
      role="user"
  )


@auth_bp.route('/logout', methods=['POST'])
def logout():
  if not current_user.is_authenticated:
    return jsonify(
        success=False,
        message="You are not logged in"
    ), 401

  logout_user()

  return jsonify(
      success=True,
      message="Logged out successfully"
  )
