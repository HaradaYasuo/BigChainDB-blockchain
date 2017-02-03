from __future__ import with_statement, unicode_literals

from fabric.api import sudo, env, hosts
from fabric.api import task, parallel
from fabric.contrib.files import sed
from fabric.operations import run, put
from fabric.context_managers import settings

from hostlist import public_dns_names
from ssh_key import ssh_key_path

# Ignore known_hosts
# http://docs.fabfile.org/en/1.10/usage/env.html#disable-known-hosts
env.disable_known_hosts = True

# What remote servers should Fabric connect to? With what usernames?
env.user = 'ubuntu'
env.hosts = public_dns_names

# SSH key files to try when connecting:
# http://docs.fabfile.org/en/1.10/usage/env.html#key-filename
env.key_filename = ssh_key_path


@task
@parallel
def put_benchmark_utils():
    put('benchmark_utils.py')


@task
@parallel
def prepare_backlog(num_transactions=10000):
    run('python3 benchmark_utils.py add-backlog {}'.format(num_transactions))


@task
@parallel
def start_bigchaindb():
    run('screen -d -m bigchaindb start &', pty=False)


@task
@parallel
def kill_bigchaindb():
    run('killall bigchaindb')
