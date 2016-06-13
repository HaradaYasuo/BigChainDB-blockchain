# Node Requirements (OS, Memory, Storage, etc.)

For now, we will assume that a BigchainDB node is just one server. In the future, a node may consist of several closely-coupled servers run by one node operator (federation member).


## OS Requirements

* RethinkDB Server [will run on any modern OS](https://www.rethinkdb.com/docs/install/). Note that the Fedora package isn't officially supported. Also, official support for Windows is fairly recent ([April 2016](https://rethinkdb.com/blog/2.3-release/)).
* Python 3.4+ [will run on any modern OS](https://docs.python.org/3.4/using/index.html).
* [Some functionality in the `multiprocessing` package doesn't work on OS X](https://docs.python.org/3.4/library/multiprocessing.html#multiprocessing.Queue.qsize). You can still use Mac OS X if you use Docker or a virtual machine.
* ZeroMQ [will run on any modern OS](http://zeromq.org/area:download).

The BigchainDB core dev team uses Ubuntu 14.04 or Fedora 23.


## Memory Requirements

Every OS has memory requirements; check the memory requirements of your OS.

There is [documentation about RethinkDB's memory requirements](https://rethinkdb.com/docs/memory-usage/). In particular: "RethinkDB requires data structures in RAM on each server proportional to the size of the data on that server’s disk, usually around 1% of the size of the total data set." ([source](https://rethinkdb.com/limitations/))


## Storage Requirements

If you want a RethinkDB cluster to store an amount of data D, with a replication factor of R (on every table), and the cluster has N nodes, then each node will need to be able to store R×D/N data plus the storage required for the OS and various other software (RethinkDB, Python, etc.). The secondary indexes also require some storage.

For failover to work, [every RethinkDB table must have at least three replicas](https://rethinkdb.com/docs/failover/), i.e. R ≥ 3.

Also, RethinkDB tables can have [at most 64 shards](https://rethinkdb.com/limitations/). For example, if you have only one table and more than 64 nodes, some nodes won't have the primary of any shard, i.e. they will have replicas only. In other words, once you pass 64 nodes, adding more nodes won't provide storage space for new data; it will only add more space for shard replicas. If the biggest single-node storage available is d, then the most you can store in a RethinkDB cluster is < 64×d: accomplished by putting one primary shard in each of 64 nodes, with all replica shards on other nodes. (This is assuming one table. If there are T tables, then the most you can store is < 64×d×T.)


## Compatible File Systems

RethinkDB has [issues with `btrfs`](https://github.com/rethinkdb/rethinkdb/issues/2781) (B-tree file system).

If you want to use RethinkDB's `--direct-io` command-line option, then you need a file system which supports that. (Many compressed or encrypted file systems do not.)


## CPU Requirements

Most servers will have enough CPUs (or vCPUs) to run a BigchainDB node. The more you have, the higher throughput will be.

