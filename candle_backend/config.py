import os

class Config:
    DEBUG = True
    TESTING = False
    CSRF_ENABLED = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    SECRET_KEY = os.environ.get("SECRET_KEY")

    SERVER_PATH = ''
    MYSQL_DATABASE_CHARSET = 'utf8mb4'  # Kvoli collation - zatial nevyuzivame.
    # app.config['SQLALCHEMY_ECHO'] = True    # zobrazuje nam queries, kt. bezia na pozadi
