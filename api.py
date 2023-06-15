import logging

from flask import Flask
from flask.logging import create_logger
from app import APP_BLUEPRINT

APP = Flask(__name__)
LOGGER = create_logger(APP)
APP.register_blueprint(APP_BLUEPRINT)


class HTTPError(Exception):
    """HTTPError class"""

    status_code = 500

    def __init__(self, message, status_code=None, payload=None):

        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
        Exception.__init__(self, status_code, message)

    def to_dict(self):
        """This function exports payload to dictionary"""
        dict_output = {}
        if self.payload is not None:
            dict_output['payload'] = self.payload
        dict_output['message'] = self.message
        dict_output['status_code'] = self.status_code
        return dict_output


@APP.errorhandler(HTTPError)
def handle_invalid_usage(error):
    response = jsonify(error.__dict__)
    response.status_code = error.status_code
    return response

if __name__ != '__main__':
    GUNICORN_LOGGER = logging.getLogger('gunicorn.error')
    LOGGER.handlers = GUNICORN_LOGGER.handlers
    LOGGER.setLevel(GUNICORN_LOGGER.level)
    LOGGER.info('api.py started')

else:
    APP.run(
        host=APP.config.get('HOST', '127.0.0.1'),
        port=int(APP.config.get('PORT', 8080)),
        processes=int(APP.config.get('PROCESSES', 1)),
        threaded=False,
        debug=True,
    ) # pragma: no cover
