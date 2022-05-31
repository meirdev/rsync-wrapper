import selectors
import subprocess
from typing import IO

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

    def read(fp: IO[str]) -> str | None:
        if output := fp.readline():
            return output

        selector.unregister(fp)
        fp.close()

        return None

    selector.register(stdout, selectors.EVENT_READ)
    selector.register(stderr, selectors.EVENT_READ)

    output_type = {
        stdout: types.StdOut,
        stderr: types.StdErr,
    }

    while not stdout.closed or not stderr.closed:
        for key, _ in selector.select():
            fileobj: IO[str] = key.fileobj  # type: ignore

            if data := read(fileobj):
                yield output_type[fileobj](data)

    yield types.ExitCode(process.wait())
