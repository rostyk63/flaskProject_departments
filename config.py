class Config(object):
    DEBUG = True
    SECRET_KEY = 'u5wqar7opt9870p98tflukdysdt6u56e76t8ulgilgi'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:1963@localhost:5432/departments'


# class ProductionConfig(Config):
#     DEBUG = False
#     SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL'].replace("postgres://", "postgresql://", 1)
