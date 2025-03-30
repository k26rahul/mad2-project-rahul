from flask import Flask
from flask_cors import CORS
from flask_security import Security, SQLAlchemyUserDatastore

from db.models import db, User, Role
from db.seed import seed_data

from .config import Config
from .blueprints import register_blueprints
from .error_handlers import register_error_handlers
from .cache import cache

from datetime import datetime, date
from flask.json.provider import DefaultJSONProvider


class UpdatedJSONProvider(DefaultJSONProvider):
  # https://stackoverflow.com/questions/43663552/keep-a-datetime-date-in-yyyy-mm-dd-format-when-using-flasks-jsonify
  def default(o):
    if isinstance(o, (date, datetime)):
      return o.isoformat()
    return super().default(o)


def create_app():
  app = Flask(__name__,
              template_folder='../templates',
              static_folder='../static',  # Add static folder configuration
              static_url_path='/static')  # URLs will be prefixed with /static
  app.config.from_object(Config)
  app.json_provider_class = UpdatedJSONProvider

  db.init_app(app)

  cache.init_app(app)

  user_datastore = SQLAlchemyUserDatastore(db, User, Role)
  Security(app, user_datastore, register_blueprint=False)

  CORS(app, supports_credentials=True)

  register_error_handlers(app)

  with app.app_context():
    db.create_all()
    seed_data()

  return app


app = create_app()
register_blueprints(app)


@app.route('/test-cache')
@cache.cached(timeout=5)
def test_cache():
  from datetime import datetime
  from flask import jsonify
  return jsonify(
      time=str(datetime.now()),
  )
