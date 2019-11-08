import eventlet
eventlet.monkey_patch()

import os
from flask import Flask
from flask_socketio import SocketIO, send, emit
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from config import Config
from celery import Celery
from helpers import get_ngrok_url, make_celery


app = Flask(__name__)
Bootstrap(app)
app.config.from_object(Config)
db = SQLAlchemy(app)
celery = make_celery(app)

socketio = SocketIO(app, message_queue=app.config['CELERY_BROKER_URL'])


from views import *

NGROK_HOST = get_ngrok_url()
if NGROK_HOST:
    app.config['CALLBACK_HOST'] = NGROK_HOST

if __name__ == '__main__':
    socketio.run(app, debug=True)


