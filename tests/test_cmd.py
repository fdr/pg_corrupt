import pytest

from pg_corrupt import cmd


def test_scan_rel():
    with pytest.raises(SystemExit) as e:
        cmd.run('scan-relation')

    assert e.value.code == 2


def test_help():
    with pytest.raises(SystemExit) as e:
        cmd.run('-h')

    assert e.value.code == 2
