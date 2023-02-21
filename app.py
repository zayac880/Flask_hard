# основной файл приложения. здесь конфигурируется фласк, сервисы, SQLAlchemy и все остальное что требуется для приложения.
# этот файл часто является точкой входа в приложение

# Пример

from flask import Flask
from flask_restx import Api

from config import Config
from setup_db import db
from views.movies import movies_ns
from views.genres import genre_ns
from views.directors import director_ns
from create_data import data_to_db


# функция создания основного объекта app
def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    return app


# функция подключения расширений (Flask-SQLAlchemy, Flask-RESTx, ...)
def register_extensions(app):
    db.init_app(app)
    api = Api(app)
    api.add_namespace(movies_ns)
    api.add_namespace(genre_ns)
    api.add_namespace(director_ns)
    create_data(app, db)


def create_data(app, db):
    with app.app_context():
        db.drop_all()
        db.create_all()
        data_to_db()
        # with db.session.begin():
        #    db.session.add_all()


app = create_app(Config())
app.debug = True

if __name__ == '__main__':
    app.run(host="localhost", debug=True, port=5000)
