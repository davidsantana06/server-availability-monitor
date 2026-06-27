from datetime import datetime, timedelta

from app.__main__ import _is_reminder_due


def test_reminder_due_without_previous_notification():
    # arrange / act / assert
    assert _is_reminder_due(None, 60) is True


def test_reminder_not_due_within_interval():
    # a
    just_notified = datetime.now()

    # a / a
    assert _is_reminder_due(just_notified, 60) is False


def test_reminder_due_after_interval():
    # a
    long_ago = datetime.now() - timedelta(seconds=120)

    # a / a
    assert _is_reminder_due(long_ago, 60) is True
