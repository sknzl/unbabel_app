import eventlet
import os
import sys
sys.path.append('.')
import unittest
from app import db, app
from flask_socketio import SocketIO
from api import post_translation
from models import Translation

basedir = os.path.abspath(os.path.dirname(__file__))
socketio = SocketIO(app)

class TestBase(unittest.TestCase):
	def setUp(self):
		self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
		app.config["TESTING"] = True
		app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
		self.client = app.test_client()
		db.drop_all()
		db.create_all()
	

	def test_index(self):
		response = self.client.get("/", follow_redirects=True)
		self.assertEqual(response.status_code, 200)
		

class TestSocketIO(unittest.TestCase):
	def setUp(self):
		self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
		app.config["TESTING"] = True
		app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
		self.client = socketio.test_client(app)
		db.drop_all()
		db.create_all()
	

	def tearDown(self):
		self.client.disconnect()
	

	def test_connection(self):
            connected = self.client.is_connected()
            self.assertEqual(connected, True)


class TestAPI(unittest.TestCase):
        def setUp(self):
            self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
            app.config["TESTING"] = True
            app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
            self.client = app.test_client()
            db.drop_all()
            db.create_all()
        

        def test_api_get(self):
            response = post_translation("en", "es", "hello")
            self.assertEqual(response["source_language"], "en")
            self.assertEqual(response["target_language"], "es")
            self.assertEqual(response["text"], "hello")
            self.assertEqual(response["status"], "new")
            self.assertEqual("uid" in response, True)


class TestTranslation(unittest.TestCase):
        def setUp(self):
            self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
            app.config["TESTING"] = True
            app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
            self.client = app.test_client()
            db.drop_all()
            db.create_all()
        
        def test_post_translation(self):
            data = {'translation_text': 'Hello'}
            response = self.client.post('/translation',data=data)
            self.assertEqual(response.json["source_text"], data["translation_text"])
            self.assertEqual(Translation.query.count(), 1)

        def test_all_translations(self):
            texts = [{'translation_text': 'Hello'}, {'translation_text': 'Hello 2'}]
            for text in texts:
                self.client.post('/translation',data=text)
            
            self.assertEqual(Translation.query.count(), 2)

        def test_delete_translations(self):
            texts = [{'translation_text': 'Hello'}, {'translation_text': 'Hello 2'}]
            for text in texts:
                self.client.post('/translation',data=text)
            response = self.client.get("/translations/delete", follow_redirects=True)
            
            self.assertEqual(response.status_code, 200)
            self.assertEqual(Translation.query.count(), 0)

class TestCallback(unittest.TestCase):
        def setUp(self):
            self.db_uri = 'sqlite:///' + os.path.join(basedir, 'test.db')
            app.config["TESTING"] = True
            app.config["SQLALCHEMY_DATABASE_URI"] = self.db_uri
            self.client_http = app.test_client()
            self.client_ws = socketio.test_client(app)
            db.drop_all()
            db.create_all()
            translation = Translation(
                source_text="Hello",
                target_text=None,
                source_language="en",
                target_language="es",
                uid=111222,
                status="new",
            )

            db.session.add(translation)
            db.session.commit()

        def test_callback(self):
            self.client_ws.connect()
            data = {'status': 'completed', 'translated_text': "Hola", 'uid': 111222}
            response = self.client_http.post('/unbabel_callback',data=data)
            self.assertEqual(response.json["success"], True)

if __name__ == "__main__":
	unittest.main()