.. raw:: html

   <style>
    .rst-content a.internal[href*='/schema/'] {
        border: solid 1px #e1e4e5;
        font-family: monospace;
        font-size: 12px;
        color: blue;
        padding: 2px 4px;
        background-color: white;
    }
   </style>

=====================
The Transaction Model
=====================

A transaction has the following structure:

.. code-block:: json

    {
        "id": "<hash of transaction, excluding signatures (see explanation)>",
        "version": "<version number of the transaction model>",
        "transaction": {
            "fulfillments": ["<list of fulfillments>"],
            "conditions": ["<list of conditions>"],
            "operation": "<string>",
            "asset": "<digital asset description (explained in the next section)>",
            "metadata": {
                "id": "<uuid>",
                "data": "<any JSON document>"
            }
        }
    }

Here's some explanation of the contents of a :ref:`transaction <transaction>`:

- :ref:`id <transaction.id>`: The id of the transaction, and also the database primary key.
- :ref:`version <transaction.version>`: Version number of the transaction model, so that software can support different transaction models.
- :ref:`transaction <Transaction Body>`:
    - **fulfillments**: List of fulfillments. Each :ref:`fulfillment <Fulfillment>` contains a pointer to an unspent asset
      and a *crypto fulfillment* that satisfies a spending condition set on the unspent asset. A *fulfillment*
      is usually a signature proving the ownership of the asset.
      See :doc:`./crypto-conditions`.

    - **conditions**: List of conditions. Each :ref:`condition <Condition>` is a *crypto-condition* that needs to be fulfilled by a transfer transaction in order to transfer ownership to new owners.
      See :doc:`./crypto-conditions`.

    - **operation**: String representation of the :ref:`operation <transaction.operation>` being performed (currently either "CREATE", "TRANSFER" or "GENESIS"). It determines how the transaction should be validated.

	- **asset**: Definition of the digital :ref:`asset <Asset>`. See next section.

    - **metadata**:
        - :ref:`id <metadata.id>`: UUID version 4 (random) converted to a string of hex digits in standard form.
        - :ref:`data <metadata.data>`: Can be any JSON document. It may be empty in the case of a transfer transaction.

Later, when we get to the models for the block and the vote, we'll see that both include a signature (from the node which created it). You may wonder why transactions don't have signatures... The answer is that they do! They're just hidden inside the ``fulfillment`` string of each fulfillment. A creation transaction is signed by whoever created it. A transfer transaction is signed by whoever currently controls or owns it.

What gets signed? For each fulfillment in the transaction, the "fullfillment message" that gets signed includes the ``operation``, ``data``, ``version``, ``id``, corresponding ``condition``, and the fulfillment itself, except with its fulfillment string set to ``null``. The computed signature goes into creating the ``fulfillment`` string of the fulfillment.

One other note: Currently, transactions contain only the public keys of asset-owners (i.e. who own an asset or who owned an asset in the past), inside the conditions and fulfillments. A transaction does *not* contain the public key of the client (computer) which generated and sent it to a BigchainDB node. In fact, there's no need for a client to *have* a public/private keypair. In the future, each client may also have a keypair, and it may have to sign each sent transaction (using its private key); see `Issue #347 on GitHub <https://github.com/bigchaindb/bigchaindb/issues/347>`_. In practice, a person might think of their keypair as being both their "ownership-keypair" and their "client-keypair," but there is a difference, just like there's a difference between Joe and Joe's computer.
