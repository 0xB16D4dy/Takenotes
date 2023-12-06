from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for, send_from_directory,current_app, escape
from flask_login import current_user, login_required
from bs4 import BeautifulSoup
from .models import Note
from . import db
import json
from .forms import *
# from sqlalchemy.sql.functions import user

views = Blueprint("views", __name__)


@views.route('/home', methods=["GET"])
@views.route('/', methods=["GET"])
@login_required
def home():
    form = NoteForm()
    if form.validate_on_submit():
        note = format(escape(form.content.data))
        if note:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
        flash('Note added!', category="success")
    return render_template('index.html', form = form, user=current_user)


@views.route('/delete-note', methods=["POST"])
@login_required
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
 

@views.route('/update-note/<int:id>', methods=["GET","POST"])
@login_required
def update_note(id):
    note_to_update = Note.query.get(id)
    plaintext = BeautifulSoup(note_to_update.data)
    if request.method == 'POST':
        note = format(escape(request.form.get('note')))
        # note = request.form.get('note')
        if note_to_update:
            if note_to_update.user_id == current_user.id:
                if note != "":
                    note_to_update.data = note
                    db.session.commit()
                    flash('Note update!', category="success")
                else:
                    flash("error", category="danger")
            return redirect(url_for("views.home")) 
    return render_template("update.html",user = current_user, note_to_update = str(plaintext.get_text())) 




@views.route('/download/<int:id>', methods=['GET', 'POST'])
@login_required
def download(id):
    note_to_download = Note.query.get(id)
    note_name_ext = str(id)+".txt"
    note_path = current_app.root_path+"\\static\\assets\\file\\"
    full_path = note_path+note_name_ext
    plaintext = BeautifulSoup(note_to_download.data)
    with open(full_path, 'w') as f: 
        f.writelines(str(plaintext.get_text()))
        f.close()
    return send_from_directory(note_path, note_name_ext, as_attachment=True)
