from . import parser, process, types


RSYNC = "rsync"


def rsync(*args) -> types.OutputIterator:
    cmd = " ".join([RSYNC, *args])

    for output in process.popen(cmd):
        if isinstance(output, types.StdOut):
            if (progress_bar := parser.ProgressBar.parse(output)) is not None:
                yield progress_bar
                continue

        yield output
