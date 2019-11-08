from app import db
import datetime


class Translation(db.Model):
    __tablename__ = 'translations'

    id = db.Column(db.Integer, primary_key=True)
    source_text = db.Column(db.Text)
    target_text = db.Column(db.Text)
    source_language = db.Column(db.String(255))
    target_language = db.Column(db.String(255))
    uid = db.Column(db.String(255))
    status = db.Column(db.String(255))
    created_time = db.Column(db.DateTime, default=datetime.datetime.utcnow)

    def __init__(self, source_text, target_text,
                 source_language, target_language, uid, status):
        self.source_text = source_text
        self.target_text = target_text
        self.source_language = source_language
        self.target_language = target_language
        self.uid = uid
        self.status = status

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'uid': self.uid, 
            'source_text': self.source_text,
            'target_text': self.target_text,
            'status': self.status,
            'created_time': self.created_time.strftime("%d/%m/%Y, %H:%M:%S")
        }