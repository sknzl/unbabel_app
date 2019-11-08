from flask import request, jsonify, render_template, redirect, url_for
from app import app, db, socketio
from forms import TextForm
from models import Translation
from api import post_translation
from tasks import get_translation_task

@app.route("/")
def index():
    form = TextForm()
    return render_template("index.html", form=form)

@app.route("/translations/delete")
def delete_translations():
    db.session.query(Translation).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.route("/translations")
def all_translations():
    translations = Translation.query.all()
    return jsonify([translation.serialize() for translation in translations])


@app.route('/translation', methods=['POST'])
def post_request():
    data = {}
    data['source_language'] = 'en'
    data['target_language'] = 'es'
    data['source_text'] = request.form['translation_text']

    translation = Translation(
        source_text=data['source_text'],
        target_text=None,
        source_language=data['source_language'],
        target_language=data['target_language'],
        uid=None,
        status=None,
    )

    db.session.add(translation)
    db.session.commit()
    get_translation_task.delay(translation.id, data)

    return jsonify(translation.serialize())


@app.route('/unbabel_callback', methods=['POST'])
def unbabel_callback():
    status = request.form["status"]
    target_text = request.form["translated_text"]
    uid = request.form["uid"]
    # error catching missing if Translation instance was deleted in the meantime.
    translation = Translation.query.filter_by(uid=uid).first()
    translation.status = status
    translation.target_text = target_text
    db.session.commit()
    socketio.emit('response', translation.serialize())
    response = jsonify(success=True)
    return response

