from flask import Blueprint, jsonify, request
from flask_security import roles_required
from db.models import db

admin_bp = Blueprint('admin', __name__)
