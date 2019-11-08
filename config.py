import os

class Config(object):
    DEBUG = True
    CALLBACK_HOST = os.environ.get('CALLBACK_HOST', "https://localhost:8000") #change here localhost:8000 if you are not running ngrok or CALLBACK_HOST is not defined in the env
    SECRET_KEY = os.urandom(32)
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', "postgresql://localhost/unbabel")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_BROKER_URL=os.environ.get('REDIS_URL', 'redis://localhost:6379')
    CELERY_RESULT_BACKEND=os.environ.get('REDIS_URL', 'redis://localhost:6379')
    UNBABEL_USERNAME = os.environ.get('UNBABEL_USERNAME', 'username') #define unbabel api username in env or here
    UNBABEL_API_KEY = os.environ.get('UNBABEL_API_KEY', 'api_key') #define unbabel api key in env or here

