# The BigchainDB Command Line Interfaces (CLIs)

BigchainDB has some Command Line Interfaces (CLIs). One of them is the `bigchaindb` command which we already saw when we first started BigchainDB using:
```text
$ bigchaindb configure
$ bigchaindb start
```

When you run `bigchaindb configure`, it creates a default configuration file in `$HOME/.bigchaindb`. You can check that configuration using:
```text
$ bigchaindb show-config
```

To find out what else you can do with the `bigchain` command, use:
```text
$ bigchaindb -h
```

There's another command named `bigchaindb-benchmark`. It's used to run benchmarking tests. You can learn more about it using:
```text
$ bigchaindb-benchmark -h
$ bigchaindb-benchmark load -h
```

Note that you can always start `bigchaindb` using a different config file using the `-c` option.
For more information check the help with `bigchaindb -h`.

