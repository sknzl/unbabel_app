import requests
import json
from app import app

username = app.config['UNBABEL_USERNAME']
api_key = app.config['UNBABEL_API_KEY']


def post_translation(source_language, target_language, text):
    callback_url = app.config["CALLBACK_HOST"] + "/unbabel_callback"
    headers = {
        'Authorization': "ApiKey {}:{}".format(username, api_key),
        'Content-Type': "application/json"
    }

    body = {
        'text': text,
        'source_language': source_language,
        'target_language': target_language,
        'callback_url': callback_url,
        'text_format': "text",
    }

    url = 'https://sandbox.unbabel.com/tapi/v2/translation/'

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.ok:
            return response.json()
        else:
            raise Exception('Something went wrong with the request: {}'.format(response.status_code))

    except Exception as e:
        raise Exception('Something went wrong with the API call: {}'.format(repr(e)))