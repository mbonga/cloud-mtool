"""Simple smoke test to verify imports and singleton behavior without network calls."""
from cmdb_clients import CMDB, VALI, JIRA, Config, Logger


def test_singleton_instances():
    c1 = CMDB('https://example.com')
    c2 = CMDB('https://example.com')
    assert c1 is c2

    v1 = VALI('https://example.com')
    v2 = VALI('https://example.com')
    assert v1 is v2

    j1 = JIRA('https://example.com')
    j2 = JIRA('https://example.com')
    assert j1 is j2

    cfg1 = Config()
    cfg2 = Config()
    assert cfg1 is cfg2

    log1 = Logger()
    log2 = Logger()
    assert log1 is log2


if __name__ == '__main__':
    test_singleton_instances()
    print('smoke test passed')
