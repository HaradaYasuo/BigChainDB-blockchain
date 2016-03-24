import copy

import pytest

import bigchaindb
from bigchaindb import exceptions


ORIGINAL_CONFIG = copy.deepcopy(bigchaindb._config)


@pytest.fixture(scope='function', autouse=True)
def clean_config(monkeypatch):
    monkeypatch.setattr('bigchaindb.config', copy.deepcopy(ORIGINAL_CONFIG))


def test_bigchain_instance_is_initialized_when_conf_provided():
    from bigchaindb import config_utils
    assert 'CONFIGURED' not in bigchaindb.config

    config_utils.dict_config({'keypair': {'public': 'a', 'private': 'b'}})

    assert bigchaindb.config['CONFIGURED'] is True
    b = bigchaindb.Bigchain()

    assert b.me
    assert b.me_private


def test_bigchain_instance_raises_when_not_configured(monkeypatch):
    from bigchaindb import config_utils
    assert 'CONFIGURED' not in bigchaindb.config

    # We need to disable ``bigchaindb.config_utils.autoconfigure`` to avoid reading
    # from existing configurations
    monkeypatch.setattr(config_utils, 'autoconfigure', lambda: 0)

    with pytest.raises(exceptions.KeypairNotFoundException):
        bigchaindb.Bigchain()


def test_load_consensus_plugin_loads_default_rules_without_name():
    from bigchaindb import config_utils
    from bigchaindb.consensus import BaseConsensusRules

    assert config_utils.load_consensus_plugin() == BaseConsensusRules


def test_load_consensus_plugin_raises_with_unknown_name():
    from pkg_resources import ResolutionError
    from bigchaindb import config_utils

    with pytest.raises(ResolutionError):
        config_utils.load_consensus_plugin('bogus')


def test_load_consensus_plugin_raises_with_invalid_subclass(monkeypatch):
    # Monkeypatch entry_point.load to return something other than a
    # ConsensusRules instance
    from bigchaindb import config_utils
    monkeypatch.setattr(config_utils,
                        'iter_entry_points',
                        lambda *args: [type('entry_point', (object), {'load': lambda: object})])

    with pytest.raises(TypeError):
        config_utils.load_consensus_plugin()


def test_map_leafs_iterator():
    from bigchaindb import config_utils

    mapping = {
        'a': {'b': {'c': 1},
              'd': {'z': 44}},
        'b': {'d': 2},
        'c': 3
    }

    result = config_utils.map_leafs(lambda x, path: x * 2, mapping)
    assert result == {
        'a': {'b': {'c': 2},
              'd': {'z': 88}},
        'b': {'d': 4},
        'c': 6
    }

    result = config_utils.map_leafs(lambda x, path: path, mapping)
    assert result == {
        'a': {'b': {'c': ['a', 'b', 'c']},
              'd': {'z': ['a', 'd', 'z']}},
        'b': {'d': ['b', 'd']},
        'c': ['c']
    }


def test_env_config(monkeypatch):
    monkeypatch.setattr('os.environ', {'BIGCHAINDB_DATABASE_HOST': 'test-host',
                                       'BIGCHAINDB_DATABASE_PORT': 'test-port'})

    from bigchaindb import config_utils

    result = config_utils.env_config({'database': {'host': None, 'port': None}})
    expected = {'database': {'host': 'test-host', 'port': 'test-port'}}

    assert result == expected


def test_autoconfigure_read_both_from_file_and_env(monkeypatch):
    monkeypatch.setattr('bigchaindb.config_utils.file_config', lambda: {})
    monkeypatch.setattr('os.environ', {'BIGCHAINDB_DATABASE_HOST': 'test-host',
                                       'BIGCHAINDB_DATABASE_PORT': '4242'})

    import bigchaindb
    from bigchaindb import config_utils
    config_utils.autoconfigure()

    assert bigchaindb.config['database']['host'] == 'test-host'
    assert bigchaindb.config['database']['port'] == 4242
    assert bigchaindb.config == {
        'CONFIGURED': True,
        'database': {
            'host': 'test-host',
            'port': 4242,
            'name': 'bigchain',
        },
        'keypair': {
            'public': None,
            'private': None,
        },
        'keyring': [],
        'statsd': {
            'host': 'localhost',
            'port': 8125,
            'rate': 0.01,
        },
        'api_endpoint': 'http://localhost:8008/api/v1',
        'consensus_plugin': 'default',
    }
