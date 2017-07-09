"""
Common classes and methods for API handlers
"""
import logging

from flask import jsonify, request

from bigchaindb import config


logger = logging.getLogger(__name__)


def make_error(status_code, message=None):
    if status_code == 404 and message is None:
        message = 'Not found'

    response_content = {'status': status_code, 'message': message}
    request_info = {'method': request.method, 'path': request.path}
    request_info.update(response_content)

    logger.error('HTTP API error: %(status)s - %(method)s:%(path)s - %(message)s', request_info)

    response = jsonify(response_content)
    response.status_code = status_code
    return response


def base_ws_uri():
    """Base websocket uri."""
    scheme = config['wsserver']['scheme']
    host = config['wsserver']['host']
    port = config['wsserver']['port']
    return '{}://{}:{}'.format(scheme, host, port)
