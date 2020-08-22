from celery import Celery
from flask import Flask

from api.v1 import bp as bp_v1
from config import Config


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    app.register_blueprint(bp_v1)
    return app


def create_celery_app(app=None):
    app = app or create_app()

    celery = Celery()
    celery.config_from_object('celeryconfig')

    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask
    celery.app = app

    return celery

