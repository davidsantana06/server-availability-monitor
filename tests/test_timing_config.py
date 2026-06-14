from app.dtos import TimingConfig


def test_valid_timing_passes():
    # arrange
    timing = TimingConfig(
        check_interval_in_seconds=60,
        check_timeout_in_seconds=3,
        notification_interval_in_seconds=300,
    )

    # act
    is_valid, errors = timing.validate()

    # assert
    assert is_valid
    assert errors == ""


def test_timeout_above_its_max_fails():
    # arrange — check_timeout tem teto próprio de 60s
    timing = TimingConfig(
        check_interval_in_seconds=60,
        check_timeout_in_seconds=300,
        notification_interval_in_seconds=300,
    )

    # act
    is_valid, errors = timing.validate()

    # assert
    assert not is_valid
    assert "check_timeout_in_seconds" in errors


def test_zero_value_fails_min():
    # arrange
    timing = TimingConfig(
        check_interval_in_seconds=0,
        check_timeout_in_seconds=3,
        notification_interval_in_seconds=300,
    )

    # act
    is_valid, errors = timing.validate()

    # assert
    assert not is_valid
    assert "check_interval_in_seconds" in errors
