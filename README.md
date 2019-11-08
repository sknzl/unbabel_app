# Unbabel App
A Flask project showcasing a simple App translating from English to Spanish using the Unbabel API. The app can be easily extended to support any other language provided by Unbabel. Requests to the Unbabel API are done over an asynchronous job queue implemented with Celery, which makes the app highly scalable. Returned translations from the API are received from a callback route that delivers the finished translations with a WebSocket connection to the frontend. This avoids constant ajax polling and allows to display the finished translations the fastest way possible on the frontend.

## Stack
- Python 3
- Flask
- PostgreSQL
- Celery
- WebSocket (flask-socketio)
- Redis
- Frontend: Bootstrap, jQuery + Vanilla JS

## Run it locally
- PostgreSQL must be running with a created database called `unbabel`.
- Redis must be running.
- Clone the repository.
- Create a python3 venv, activate it, and install the required packages with `pip install -r requirements.txt`.
- Run `python manage.py db upgrade` to apply database migrations.
- To receive callbacks from the Unbabel API two options exists: Use ngrok or port forwarding. In the case
of port-forwarding set the environment variable `CALLBACK_HOST` to the host and port that forwards to your local machine at port 5000 or hard code the host in `config.py`.
The easier option is ngrok (https://ngrok.com). Run ngrok with `ngrok http 5000`. The development server will recognize automatically the public ngrok address on startup.
- Set the Unbabel API credentials in the environment variables `UNBABEL_USERNAME` and `UNBABEL_API_KEY` or hard code the credentials in `config.py`.
- Start the development server with `python app.py`.
- Start celery with `celery -A app.celery  worker --loglevel=info`.
- Go to http://localhost:5000

## Deploy to Heroku
- The Procfile for Heroku is already provided.
- Run `heroku create` and `git push heroku master`.
- Add the Heroku Redis add-on and scale the worker for Celery.
- Set the `CALLBACK_HOST` environment variable to the heroku app address with `heroku config:set CALLBACK_HOST=...`.
- Set the Unbabel API credentials in the environment variables with `heroku config:set UNBABEL_USERNAME=...` and `heroku config:set UNBABEL_API_KEY=...`.
- A demo is deployed at https://stormy-dawn-55587.herokuapp.com.

## Tests
- run `python tests/tests.py`.


