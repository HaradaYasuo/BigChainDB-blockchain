.. _the-vote-schema-file:

The Vote Schema File
====================

BigchainDB checks all :ref:`votes <the-vote-model>`
(JSON documents) against a formal schema
defined in a JSON Schema file named vote.yaml.
The contents of that file are copied below.
To understand those contents
(i.e. JSON Schema), check out
`"Understanding JSON Schema"
<https://spacetelescope.github.io/understanding-json-schema/index.html>`_
by Michael Droettboom or
`json-schema.org <http://json-schema.org/>`_.


vote.yaml
---------

.. literalinclude:: ../../../../bigchaindb/common/schema/vote.yaml
   :language: yaml