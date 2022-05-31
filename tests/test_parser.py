import datetime

from rsync_wrapper import parser, types


def test_remain():
    assert parser.Remain.parse("12:30:10") == datetime.timedelta(
        hours=12, minutes=30, seconds=10
    )
    assert parser.Remain.parse("??:??:??") is None


def test_progress_bar():
    assert parser.ProgressBar.parse(
        "32768   0%    0.00kB/s    0:00:00"
    ) == types.ProgressBar("32768", 0, 0.0, "kB/s", datetime.timedelta())

    assert parser.ProgressBar.parse(
        "310345728  31%  295.94MB/s    0:00:02"
    ) == types.ProgressBar(
        "310345728", 31, 295.94, "MB/s", datetime.timedelta(seconds=2)
    )

    assert parser.ProgressBar.parse(
        "1000000000 100%  299.04MB/s    0:00:03 (xfer#1, to-check=0/1)"
    ) == types.ProgressBar(
        "1000000000", 100, 299.04, "MB/s", datetime.timedelta(seconds=3)
    )
