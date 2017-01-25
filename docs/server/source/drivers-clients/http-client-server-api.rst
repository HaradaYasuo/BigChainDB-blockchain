The HTTP Client-Server API
==========================

.. note::

   The HTTP client-server API is currently quite rudimentary. For example,
   there is no ability to do complex queries using the HTTP API. We plan to add
   more querying capabilities in the future.

This page assumes you already know an API Root URL
for a BigchainDB node or reverse proxy.
It should be something like ``http://apihosting4u.net:9984``
or ``http://12.34.56.78:9984``.

If you set up a BigchainDB node or reverse proxy yourself,
and you're not sure what the API Root URL is,
then see the last section of this page for help.


API Root URL
------------

If you send an HTTP GET request to the API Root URL
e.g. ``http://localhost:9984`` 
or ``http://apihosting4u.net:9984``
(with no ``/api/v1/`` on the end), 
then you should get an HTTP response 
with something like the following in the body:

.. code-block:: json

    {
      "keyring": [
        "6qHyZew94NMmUTYyHnkZsB8cxJYuRNEiEpXHe1ih9QX3",
        "AdDuyrTyjrDt935YnFu4VBCVDhHtY2Y6rcy7x2TFeiRi"
      ],
      "public_key": "AiygKSRhZWTxxYT4AfgKoTG4TZAoPsWoEt6C6bLq4jJR",
      "software": "BigchainDB",
      "version": "0.6.0"
    }

Transactions
-------------------

.. http:get:: /transactions/{txid}

   Get the transaction with the ID ``txid``.

   This endpoint returns only a transaction from a ``VALID`` or ``UNDECIDED``
   block on ``bigchain``, if exists.

   :param txid: transaction ID
   :type txid: hex string

   **Example request**:

   .. sourcecode:: http

      GET /transactions/2d431073e1477f3073a4693ac7ff9be5634751de1b8abaa1f4e19548ef0b4b0e HTTP/1.1
      Host: example.com

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      {
        "transaction": {
          "conditions": [
            {
              "cid": 0,
              "condition": {
                "uri": "cc:4:20:GG-pi3CeIlySZhQoJVBh9O23PzrOuhnYI7OHqIbHjkk:96",
                "details": {
                  "signature": null,
                  "type": "fulfillment",
                  "type_id": 4,
                  "bitmask": 32,
                  "public_key": "2ePYHfV3yS3xTxF9EE3Xjo8zPwq2RmLPFAJGQqQKc3j6"
                }
              },
              "amount": 1,
              "owners_after": [
                "2ePYHfV3yS3xTxF9EE3Xjo8zPwq2RmLPFAJGQqQKc3j6"
              ]
            }
          ],
          "operation": "CREATE",
          "asset": {
            "divisible": false,
            "updatable": false,
            "data": null,
            "id": "aebeab22-e672-4d3b-a187-bde5fda6533d",
            "refillable": false
          },
          "metadata": null,
          "timestamp": "1477578978",
          "fulfillments": [
            {
              "fid": 0,
              "input": null,
              "fulfillment": "cf:4:GG-pi3CeIlySZhQoJVBh9O23PzrOuhnYI7OHqIbHjkn2VnQaEWvecO1x82Qr2Va_JjFywLKIOEV1Ob9Ofkeln2K89ny2mB-s7RLNvYAVzWNiQnp18_nQEUsvwACEXTYJ",
              "owners_before": [
                "2ePYHfV3yS3xTxF9EE3Xjo8zPwq2RmLPFAJGQqQKc3j6"
              ]
            }
          ]
        },
        "id": "2d431073e1477f3073a4693ac7ff9be5634751de1b8abaa1f4e19548ef0b4b0e",
        "version": 1
      }

   :statuscode 200: A transaction with that ID was found.
   :statuscode 404: A transaction with that ID was not found.

.. http:get:: /transactions?fields=id,conditions&fulfilled=false&owner_afters={owners_after}

   is an `alias for retrieving unfulfilled conditions for a set of public keys. <#get--conditions?fulfilled=false&owner_afters=owners_after>`_

.. http:post:: /transactions/

   Push a new transaction.

   .. note::
       The posted transaction should be valid `transaction
       <https://bigchaindb.readthedocs.io/en/latest/data-models/transaction-model.html>`_.
       The steps to build a valid transaction are beyond the scope of this page.
       One would normally use a driver such as the `BigchainDB Python Driver
       <https://docs.bigchaindb.com/projects/py-driver/en/latest/index.html>`_
       to build a valid transaction.

   **Example request**:

   .. literalinclude:: samples/post-tx-request.http
      :language: http

   **Example response**:

   .. literalinclude:: samples/post-tx-response.http
      :language: http

   :statuscode 202: The pushed transaction was accepted, but the processing has not been completed.
   :statuscode 400: The transaction was invalid and not created.


Statuses
--------------------------------

.. http:get:: /statuses/{txid}

   Get the status of a transaction with the ID ``txid``, if a transaction
   with that ``txid`` exists.

   The possible status values are ``backlog``, ``undecided``, ``valid`` or
   ``invalid``.

   If a transaction is persisted to the chain and it's status is set to
   ``valid`` or ``undecided``, a ``303 See Other`` status code is returned, as
   well as a URL to the resource in the location header.

   :param txid: transaction ID
   :type txid: hex string

   **Example request**:

   .. literalinclude:: samples/get-tx-status-request.http
      :language: http

   **Example response**:

   .. literalinclude:: samples/get-tx-status-response.http
      :language: http

   :statuscode 200: A transaction with that ID was found. The status is either ``backlog``, ``invalid``.
   :statuscode 303: A transaction with that ID was found and persisted to the chain. A location header to the resource is provided.
   :statuscode 404: A transaction with that ID was not found.


Conditions
-------------------------

.. http:get:: /conditions?fulfilled=false&owner_afters={owners_after}

   Get a list of transactions with unfulfilled conditions (conditions that have
   not been used yet in a persisted transaction.

   If the querystring ``fulfilled`` is set to ``false`` and all conditions for
   ``owners_after`` happen to be fulfilled already, this endpoint will return
   an empty list.

   This endpoint will return a ``HTTP 400 Bad Request`` if the querystring
   ``owners_after`` happens to not be defined in the request.

   This endpoint returns only a transaction from a ``VALID`` or ``UNDECIDED``
   block on ``bigchain``, if exists.

   :param fulfilled: A flag to indicate if transaction's with fulfilled conditions should be returned.
   :type fulfilled: boolean

   :param owners_after: Public keys able to validly spend an output of a transaction, assuming the user also has the corresponding private key.
   :type owners_after: base58 encoded string

   **Example request**:

   .. sourcecode:: http

      GET /conditions?fulfilled=false&owners_after=1AAAbbb...ccc HTTP/1.1
      Host: example.com

   **Example response**:

   .. sourcecode:: http

      HTTP/1.1 200 OK
      Content-Type: application/json

      [{
        "transaction": {
          "conditions": [
            {
              "cid": 0,
              "condition": {
                "uri": "cc:4:20:GG-pi3CeIlySZhQoJVBh9O23PzrOuhnYI7OHqIbHjkk:96",
                "details": {
                  "signature": null,
                  "type": "fulfillment",
                  "type_id": 4,
                  "bitmask": 32,
                  "public_key": "1AAAbbb...ccc"
                }
              },
              "amount": 1,
              "owners_after": [
                "1AAAbbb...ccc"
              ]
            }
          ],
        "id": "2d431073e1477f3073a4693ac7ff9be5634751de1b8abaa1f4e19548ef0b4b0e",
      }]

   :statuscode 200: A list of transaction's containing unfulfilled conditions was found and returned.
   :statuscode 400: The request wasn't understood by the server, e.g. the ``owners_after`` querystring was not included in the request.
