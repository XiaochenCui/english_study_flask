import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'q654b146rg4h5212csac34g3'

    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@localhost/english'


config = {'default': DevelopmentConfig}
