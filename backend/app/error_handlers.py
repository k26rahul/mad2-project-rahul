from flask import jsonify


def register_error_handlers(app):
  @app.errorhandler(400)
  def bad_request(error):
    response = jsonify(success=False, message="Bad Request")
    response.status_code = 400
    return response

  @app.errorhandler(401)
  def unauthorized(error):
    response = jsonify(success=False, message="Unauthorized")
    response.status_code = 401
    return response

  @app.errorhandler(403)
  def forbidden(error):
    response = jsonify(success=False, message="Forbidden")
    response.status_code = 403
    return response

  @app.errorhandler(404)
  def not_found(error):
    response = jsonify(success=False, message="Not Found")
    response.status_code = 404
    return response

  @app.errorhandler(405)
  def method_not_allowed(error):
    response = jsonify(success=False, message="Method Not Allowed")
    response.status_code = 405
    return response

  @app.errorhandler(500)
  def internal_server_error(error):
    response = jsonify(success=False, message="Internal Server Error")
    response.status_code = 500
    return response
