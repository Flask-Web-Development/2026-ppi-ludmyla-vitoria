from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('filme', __name__)

@bp.route('/')
def index():
    db = get_db()
    posts = db.execute(
        'SELECT f.id, title, body, created, author_id, username'
        ' FROM filme f JOIN user u ON f.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('filme/index.html', posts=posts)

@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        titulo = request.form['titulo']
        tipo = request.form['tipo']
        genero = request.form['genero']
        nota = request.form['nota']
        comentario = request.form['comentario']


        if not titulo:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO filme (title, body, author_id)'
                ' VALUES (?, ?, ?)',
            )
            titulo;
            db.commit()
            return redirect(url_for('filmes.index'))

    return render_template('filmes/create.html')
def get_filme(id, check_author=True):
        filme = get_db().execute(
        'SELECT f.id, title, body, created, author_id, username'
        ' FROM filme f JOIN user u ON f.author_id = u.id'
        ' WHERE f.id = ?',
        (id,)
    ).fetchone()

        if filme is None:
         abort(404, f"filme id {id} doesn't exist.")

        if check_author and filme['author_id'] != g.user['id']:
         abort(403)

        return filme

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    filme = get_filme(id)

    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        error = None

        if not title:
            error = 'Title is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE filme SET title = ?, body = ?'
                ' WHERE id = ?',
                (title, body, id)
            )
            db.commit()
            return redirect(url_for('filmes.index'))

    return render_template('filmes/update.html', filme=filme)
    
@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
      get_filme(id)
      db = get_db()
      db.execute('DELETE FROM filme WHERE id = ?', (id,))
      db.commit()
      return redirect(url_for('filmes.index'))