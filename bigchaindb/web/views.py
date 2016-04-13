"""This module provides the blueprint for some basic API endpoints.

For more information please refer to the documentation in Apiary:
 - http://docs.bigchaindb.apiary.io/
"""

import flask
from flask import current_app, request, Blueprint

import bigchaindb
from bigchaindb import util


basic_views = Blueprint('basic_views', __name__)


# Unfortunately I cannot find a reference to this decorator.
# This answer on SO is quite useful tho:
# - http://stackoverflow.com/a/13432373/597097
@basic_views.record
def record(state):
    """This function checks if the blueprint can be initialized
    with the provided state."""

    bigchain = state.app.config.get('bigchain')
    monitor = state.app.config.get('monitor')

    if bigchain is None:
        raise ValueError('This blueprint expects you to provide '
                         'database access through `bigchain`.')

    if monitor is None:
        raise ValueError('This blueprint expects you to provide '
                         'a monitor instance to record system '
                         'performance.')


@basic_views.route('/transactions/<tx_id>')
def get_transaction(tx_id):
    """API endpoint to get details about a transaction.

    Args:
        tx_id (str): the id of the transaction.

    Return:
        A JSON string containing the data about the transaction.
    """

    bigchain = current_app.config['bigchain']

    tx = bigchain.get_transaction(tx_id)
    return flask.jsonify(**tx)


@basic_views.route('/transactions/', methods=['POST'])
def create_transaction():
    """API endpoint to push transactions to the Federation.

    Return:
        A JSON string containing the data about the transaction.
    """
    bigchain = current_app.config['bigchain']
    monitor = current_app.config['monitor']

    val = {}

    # `force` will try to format the body of the POST request even if the `content-type` header is not
    # set to `application/json`
    tx = request.get_json(force=True)

    if tx['transaction']['operation'] == 'CREATE':
        tx = util.transform_create(tx)
        tx = bigchain.consensus.sign_transaction(
            tx, private_key=bigchain.me_private)

    if not bigchain.consensus.verify_signature(tx):
        val['error'] = 'Invalid transaction signature'

    with monitor.timer('write_transaction',
                       rate=bigchaindb.config['statsd']['rate']):
        val = bigchain.write_transaction(tx)

    return flask.jsonify(**tx)

