from rsync_wrapper import error_codes


def test_exists():
    assert error_codes.get_error_code(19) == error_codes.RErr.SIGNAL1


def test_not_exists():
    assert error_codes.get_error_code(40) is None
