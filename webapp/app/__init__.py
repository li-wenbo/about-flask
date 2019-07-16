from flask import Flask
import logging

FLASK_CONFIGFILENAME = r'flask.conf'


def create_app(import_name):
    app = Flask(import_name)
    app.config.from_pyfile(FLASK_CONFIGFILENAME)
    return app


def init_logger(app):
    """
    http://flask.pocoo.org/docs/1.0/logging/#basic-configuration will overwrite gunicorn logging config
    cause logging.getLogger is a Singleton method， so we can set the attr before flask.logging.create_logger
    :param app:
    :return:
    """

    import os.path
    log_filename = os.path.join(app.root_path, 'logs', 'flask.log')

    logger = logging.getLogger(app.name)
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler(log_filename)
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter('%(asctime)s|%(process)d - %(name)s - %(levelname)s - %(message)s'))
    logger.addHandler(fh)
