from app import __main__ as monitor
from app.dtos import ServerConfig
from app.enums import ServerStatus
from app.repositories import servers_config_repository


def _seed(*hostnames: str):
    servers_config_repository._server_configs = [
        ServerConfig(hostname=h, host="1.1.1.1", port=443) for h in hostnames
    ]


def test_detects_new_offline():
    # arrange
    _seed("a")
    previous = {"a": ServerStatus.ONLINE}
    current = {"a": ServerStatus.OFFLINE}

    # act
    diff = monitor._diff_statuses(previous, current)

    # assert
    assert [s.hostname for s in diff.new_offline] == ["a"]
    assert [s.hostname for s in diff.still_offline] == ["a"]
    assert diff.recovered == []


def test_detects_recovery():
    # arrange
    _seed("a")
    previous = {"a": ServerStatus.OFFLINE}
    current = {"a": ServerStatus.ONLINE}

    # act
    diff = monitor._diff_statuses(previous, current)

    # assert
    assert [s.hostname for s in diff.recovered] == ["a"]
    assert diff.new_offline == []
    assert diff.still_offline == []


def test_still_offline_without_state_change():
    # arrange
    _seed("a")
    previous = {"a": ServerStatus.OFFLINE}
    current = {"a": ServerStatus.OFFLINE}

    # act
    diff = monitor._diff_statuses(previous, current)

    # assert
    assert [s.hostname for s in diff.still_offline] == ["a"]
    assert diff.new_offline == []
    assert diff.recovered == []
