import os
from flask import Flask


# Create and configure app
def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(SECRET_KEY="dev", DATABASE=os.path.join(app.instance_path, "flaskr.sqlite"))

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Test page which prints 'Hello, World!'
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    from . import db
    db.init_app(app)

    # Add blueprints for authentication and note functions
    from . import auth
    from . import note
    app.register_blueprint(auth.bp)
    app.register_blueprint(note.bp)
    app.add_url_rule('/', endpoint='index')

    return app

