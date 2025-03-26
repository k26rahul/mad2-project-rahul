from celery import Celery


def make_celery(app):
  celery = Celery(
      app.import_name,
      backend="redis://localhost:6380/0",
      broker="redis://localhost:6380/0",
  )
  celery.conf.update(app.config)
  return celery
