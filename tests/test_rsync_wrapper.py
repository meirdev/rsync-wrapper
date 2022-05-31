from datetime import timedelta
from unittest.mock import patch

import rsync_wrapper
from rsync_wrapper import types


STDOUT = """myfile
       32768   0%    0.00kB/s    0:00:00
   310345728  31%  295.94MB/s    0:00:02
   625246208  62%  298.27MB/s    0:00:01
   939294720  93%  298.78MB/s    0:00:00
  1000000000 100%  299.04MB/s    0:00:03 (xfer#1, to-check=0/1)

sent 1000122155 bytes  received 42 bytes  222249377.11 bytes/sec
total size is 1000000000  speedup is 1.00"""

EXCEPTED = [
    types.StdOut("myfile"),
    types.ProgressBar("       32768", 0, 0.0, "kB/s", timedelta()),
    types.ProgressBar("   310345728", 31, 295.94, "MB/s", timedelta(seconds=2)),
    types.ProgressBar("   625246208", 62, 298.27, "MB/s", timedelta(seconds=1)),
    types.ProgressBar("   939294720", 93, 298.78, "MB/s", timedelta(seconds=0)),
    types.ProgressBar("  1000000000", 100, 299.04, "MB/s", timedelta(seconds=3)),
    types.StdOut(""),
    types.StdOut("sent 1000122155 bytes  received 42 bytes  222249377.11 bytes/sec"),
    types.StdOut("total size is 1000000000  speedup is 1.00"),
    types.ExitCode(0),
]


def process_open_return_value():
    for line in STDOUT.splitlines():
        yield types.StdOut(line)
    yield types.ExitCode(0)


@patch("rsync_wrapper.process.popen")
def test_rsync(process_open_mock):
    process_open_mock.return_value = process_open_return_value()

    assert list(rsync_wrapper.rsync("rsync myfile myfile2 -P")) == EXCEPTED
