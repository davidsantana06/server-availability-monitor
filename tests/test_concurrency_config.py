from app.dtos import ConcurrencyConfig


def test_valid_concurrency_passes():
    # arrange
    concurrency = ConcurrencyConfig(check_workers=10)

    # act
    is_valid, errors = concurrency.validate()

    # assert
    assert is_valid
    assert errors == ""


def test_check_workers_above_max_fails():
    # arrange
    concurrency = ConcurrencyConfig(check_workers=128)

    # act
    is_valid, errors = concurrency.validate()

    # assert
    assert not is_valid
    assert "check_workers" in errors


def test_check_workers_below_min_fails():
    # arrange
    concurrency = ConcurrencyConfig(check_workers=0)

    # act
    is_valid, errors = concurrency.validate()

    # assert
    assert not is_valid
    assert "check_workers" in errors
