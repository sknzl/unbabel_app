from app import celery
from api import post_translation
from app import app
from models import Translation
from app import db
from flask_socketio import SocketIO

@celery.task(ignore_result=True)
def get_translation_task(translation_id, data):
    response = post_translation(data['source_language'], data['target_language'], data['source_text'])
    # error catching if problem with response missing
    uid = response.get('uid')
    status = response.get('status')
    
    translation = Translation.query.filter_by(id=translation_id).first()
    translation.status = status
    translation.target_text = None
    translation.uid = uid
    db.session.commit()
    socketio = SocketIO(message_queue=app.config['CELERY_BROKER_URL'])
    socketio.emit('response', translation.serialize())
    return(translation.serialize())
