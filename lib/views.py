from flask import Blueprint, flash, render_template, request, jsonify
from flask_login import current_user, login_required
from .models import Note
from . import db
import json
# from sqlalchemy.sql.functions import user

views = Blueprint("views", __name__)

@views.route('/home', methods=["GET","POST"])
@views.route('/', methods=["GET","POST"])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category="danger")
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category="success")
    return render_template('index.html', user=current_user)


@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    note_id = note['note_id']
    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
        flash('Note deleted!', category="success")
    return jsonify({"code" : 200})

