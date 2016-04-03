from celery import Celery
from celery.task import task, periodic_task
from flask import Flask
from extensions import mail
from settings import Config, ProdConfig


def make_celery(app):
    celery = Celery(app.import_name, broker=Config.BROKER_URL)
    celery.conf.update(app.config)
    TaskBase = celery.Task
    class ContextTask(TaskBase):
        abstract = True
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery


def create_app2(config_object=ProdConfig):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    # register_blueprints(app) !imp == otherwise tasks cant be imported in blueprint

    return app


def register_extensions(app):
    mail.init_app(app)


app = create_app2(Config())
celery = make_celery(app)


@task
def test2(msg):
    with app.app_context():
        mail.send(msg)