import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def init_app(app):
    """Initialise app with initialise database command."""
    app.teardown_appcontext(close_db)  # calls close_db when cleaning up
    app.cli.add_command(init_db_command)


def get_db():
    """Connect to database. The connection is unique for each request and will be reused if this is called again."""
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    """If connected to a database, then close it."""
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    """Clear existing data and create new tables for database."""
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


@click.command('init-db')
@with_appcontext
def init_db_command():
    """On command, clear the existing data and create new tables for database."""
    init_db()
    click.echo('Initialized the database.')
