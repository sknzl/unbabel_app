import requests
import json
import os
from celery import Celery
from requests.exceptions import ConnectionError

def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config['CELERY_RESULT_BACKEND'],
        broker=app.config['CELERY_BROKER_URL']
    )
    celery.conf.update(app.config)

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def get_ngrok_url():
    # https://stackoverflow.com/questions/34322988/view-random-ngrok-url-when-run-in-background
    url = "http://localhost:4040/api/tunnels"
    try:
        res = requests.get(url)
        res_unicode = res.content.decode("utf-8")
        res_json = json.loads(res_unicode)
        response = res_json["tunnels"][0]["public_url"]
        return response
    except ConnectionError:
        return False