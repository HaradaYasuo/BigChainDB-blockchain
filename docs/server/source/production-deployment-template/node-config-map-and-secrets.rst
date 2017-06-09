How to Configure a BigchainDB Node
==================================

This page outlines the steps to set a bunch of configuration settings
in your BigchainDB node.
They are pushed to the Kubernetes cluster in two files,
named ``config-map.yaml`` (a set of ConfigMaps)
and ``secret.yaml`` (a set of Secrets).
They are stored in the Kubernetes cluster's key-value store (etcd).

Make sure you did all the things listed in the section titled
:ref:`Things Each Node Operator Must Do`
(including generation of all the SSL certificates needed
for MongoDB auth).


Edit config-map.yaml
--------------------

Make a copy of the file ``k8s/configuration/config-map.yaml``
and edit the data values in the various ConfigMaps.
That file already contains many comments to help you
understand each data value, but we make some additional
remarks on some of the values below.

Note: None of the data values in ``config-map.yaml`` need
to be base64-encoded. (This is unlike ``secret.yaml``,
where all data values must be base64-encoded.
This is true of all Kubernetes ConfigMaps and Secrets.)


vars
~~~~

Your BigchainDB cluster organization should have a standard way
of naming instances, so the instances in your BigchainDB node
should conform to that standard (i.e. you can't just make up some names).
There are some things worth noting about the ``mdb-instance-name``:

* MongoDB reads the local ``/etc/hosts`` file while bootstrapping a replica
  set to resolve the hostname provided to the ``rs.initiate()`` command.
  It needs to ensure that the replica set is being initialized in the same
  instance where the MongoDB instance is running.
* We use the value in the ``mdb-instance-name`` field to achieve this.
* This field will be the DNS name of your MongoDB instance, and Kubernetes
  maps this name to its internal DNS.
* This field will also be used by other MongoDB instances when forming a
  MongoDB replica set.
* We use ``mdb-instance-0``, ``mdb-instance-1`` and so on in our
  documentation. Your BigchainDB cluster may use a different naming convention.

bdb-keyring.bdb-keyring
~~~~~~~~~~~~~~~~~~~~~~~

This lists the BigchainDB public keys
of all *other* nodes in your BigchainDB cluster
(not including the public key of your BigchainDB node). Cases:

* If you're deploying the first node in the cluster,
  the value should be ``""`` (an empty string).
* If you're deploying the second node in the cluster,
  the value should be one public key inside double quotes.
  For example,
  ``"EPQk5i5yYpoUwGVM8VKZRjM8CYxB6j8Lu8i8SG7kGGce"``
* If there are two or more other nodes already in the cluster,
  the value should be a colon-separated list of public keys
  inside double quotes.
  For example,
  ``"DPjpKbmbPYPKVAuf6VSkqGCf5jzrEh69Ldef6TrLwsEQ:EPQk5i5yYpoUwGVM8VKZRjM8CYxB6j8Lu8i8SG7kGGce"``


Edit secret.yaml
----------------

Make a copy of the file ``k8s/configuration/secret.yaml``
and edit the data values in the various Secrets.
That file includes many comments to explain the required values.
**In particular, note that all values must be base64-encoded.**
There are tips at the top of the file
explaining how to convert values into base64-encoded values.

Your BigchainDB node might not need all the Secrets.
For example, if you plan to access the BigchainDB API over HTTP, you
don't need the ``https-certs`` Secret.
You can delete the Secrets you don't need,
or set their data values to ``""``.

Note that ``ca.pem`` is just another name for ``ca.crt``
(the certificate of your BigchainDB cluster's self-signed CA).


Deploy Your config-map.yaml and secret.yaml
-------------------------------------------

You can deploy your edited ``config-map.yaml`` and ``secret.yaml``
files to your Kubernetes cluster using the commands:

.. code:: bash

   $ kubectl apply -f config-map.yaml

   $ kubectl apply -f secret.yaml
