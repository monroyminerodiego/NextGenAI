import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'fkq@X^W=`A}Zy+fz-e(q1Vj20(nB7U)')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'sqlite:///{}'.format(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'app.db'))
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    DEBUG = os.environ.get('FLASK_DEBUG', '0') == 1