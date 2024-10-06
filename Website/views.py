from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json

# This file will define a blueprintof the website, i.e. will contain the routes of the website
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')

        if len(note) < 1:
            flash('Note too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added successfully', category='success')

    return render_template('home.html', user=current_user)      # home.html is available only when the current_user is logged in

@views.route('/login/loginpage1')
def loginpage1():
    return render_template('loginpage1.html')

@views.route('/sign_up')
def sign_up():
    return render_template('sign-up.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
def delete_note():
    # take note data from post request and load it as json
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({})