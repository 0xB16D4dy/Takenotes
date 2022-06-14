from flask import Blueprint, flash, redirect, render_template, request, jsonify, url_for, send_from_directory,current_app
from flask_login import current_user, login_required
from .models import Note
from . import db
import json
from .forms import *
# from sqlalchemy.sql.functions import user

views = Blueprint("views", __name__)


@views.route('/home', methods=["GET","POST"])
@views.route('/', methods=["GET","POST"])
@login_required
def home():
    form = SearchForm()
    if request.method == 'POST':
        note = request.form.get('note')
        if len(note) < 1:
            flash('Note is too short!', category="danger")
        else:
            new_note = Note(data = note, user_id = current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category="success")
    return render_template('index.html', form = form, user=current_user)


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
 

@views.route('/update-note/<int:id>', methods=["GET","POST"])
def update_note(id):
    form = SearchForm()
    note_to_update = Note.query.get(id)
    if request.method == 'POST':
        note = request.form.get('note')
        # id_to_update = Note.query.get(note_id)
        if note_to_update:
            if note_to_update.user_id == current_user.id:
                if note != "":
                    note_to_update.data = note
                    db.session.commit()
                    flash('Note update!', category="success")
                    return redirect(url_for("views.home")) 
                flash("error", category="danger")
    return render_template("update.html",user = current_user, note_to_update = note_to_update) 




@views.route('/download/<int:id>', methods=['GET', 'POST'])
def download(id):
    note_to_download = Note.query.get(id)
    note_name_ext = str(id)+".txt"
    note_path = current_app.root_path+"\\static\\assets\\file\\"
    full_path = note_path+note_name_ext
    with open(full_path, 'w') as f: 
        f.writelines(str(note_to_download.data))
        f.close()
    return send_from_directory(note_path, note_name_ext, as_attachment=True)
