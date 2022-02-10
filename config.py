import os

class Config:

    SECRET_KEY = 'SECRET_KEY'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://kirimi:alphine3900@localhost/alphinepitch'
    UPLOADED_PHOTOS_DEST ='app/static/photos'
    # SQLALCHEMY_TRACK_MODIFICATIONS = False


    #  email configurations
    MAIL_SERVER = 'siler254.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")



    @staticmethod
    def init_app(app):
        pass


class ProdConfig(Config):
        SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
class TestConfig(Config):
    pass


class DevConfig(Config):
    DEBUG = True

config_options = {
'development':DevConfig,
'production':ProdConfig,
'test':TestConfig
}