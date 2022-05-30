import selectors
import subprocess
from typing import AnyStr, IO

from . import types


def popen(command: str) -> types.BasicOutputIterator:
    process = subprocess.Popen(
        command,
        shell=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    assert process.stdout is not None
    assert process.stderr is not None

    stdout, stderr = process.stdout, process.stderr

    selector = selectors.DefaultSelector()

    def read(fp: IO[AnyStr]) -> str | None:
        if output := fp.readline():
            return output

        selector.unregister(fp)
        fp.close()

        return None

    selector.register(stdout, selectors.EVENT_READ, (types.StdOut, read))
    selector.register(stderr, selectors.EVENT_READ, (types.StdErr, read))

    while not stdout.closed or not stderr.closed:
        for key, _ in selector.select():
            output_type, callback = key.data
            if data := callback(key.fileobj):
                yield output_type(data)

    yield types.ExitCode(process.wait())
