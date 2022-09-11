class Config(object):
    DEBUG = False
    TESTING = False
    SECRET_KEY = 'sd45j3j0398gsdj02240409234ts0d20'

class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:password@localhost/WebbApp"

class DevelopmentConfig(Config):
    ENV="development"
    DEVELOPMENT=True
    DEBUG=True
    SQLALCHEMY_DATABASE_URI="mysql+mysqlconnector://root:password@localhost/WebbApp"