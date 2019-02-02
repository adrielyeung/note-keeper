from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('note', __name__)


@bp.route('/')
def index():
    """Loads index page of notes."""
    db = get_db()
    notes = db.execute(
        'SELECT p.id, title, body, created, author_id, username, archived'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'  # Load note info as well as user info
    ).fetchall()
    return render_template('note/index.html', notes=notes)


# Create
@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    """Create a new note."""
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            title = ""

        if not body:
            error = 'Body is required.'
            flash(error)

        else:
            archived = 0

            db = get_db()
            db.execute(
                'INSERT INTO post (title, body, author_id, archived)'
                ' VALUES (?, ?, ?, ?)',
                (title, body, g.user['id'], archived)  # archived = 0 for False
            )
            db.commit()
            return redirect(url_for('note.index'))

    return render_template('note/create.html')


# Update and delete
def get_note(id, check_author=True):
    """Loads existing note. Change check_author  to False if everyone can modify, not only author."""
    note = get_db().execute(
        'SELECT p.id, title, body, created, author_id, username'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if note is None:
        abort(404, "Note id {0} doesn't exist.".format(id))

    if check_author and note['author_id'] != g.user['id']:
        abort(403)

    return note


@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    """Update selected note, and also allows for deleting it."""
    note = get_note(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']

        if not title:
            title = ""

        if not body:
            error = 'Body is required.'
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE post SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('note.index'))

    return render_template('note/update.html', note=note)


@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_note(id)
    db = get_db()
    db.execute('DELETE FROM post WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('note.index'))


@bp.route('/archive', methods=('GET', 'POST',))
@login_required
def archive():
    """Loads archive page of notes."""
    db = get_db()
    ar_notes = db.execute(
        'SELECT p.id, title, body, created, author_id, username, archived'
        ' FROM post p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'  # Load note info as well as user info
    ).fetchall()

    return render_template( 'note/archive.html', notes=ar_notes)


@bp.route('/<int:id>/to_archive', methods=('GET', 'POST',))
@login_required
def to_archive(id):
    """Sends selected note to archive page and remove from main page."""
    get_note(id)
    db = get_db()
    db.execute( 'UPDATE post SET archived = 1 WHERE id = ?', (id,) )
    db.commit()
    return redirect( url_for( 'note.archive' ) )


@bp.route('/<int:id>/unarchive', methods=('GET', 'POST',))
@login_required
def unarchive(id):
    """Sends selected archived note to main page and remove from archived page."""
    get_note(id)
    db = get_db()
    db.execute( 'UPDATE post SET archived = 0 WHERE id = ?', (id,) )
    db.commit()
    return redirect( url_for( 'note.index' ) )
