from enum import Enum
from typing import NamedTuple


class Code(NamedTuple):
    code: int
    message: str | None = None


class RErr(Code, Enum):
    # See: https://github.com/WayneD/rsync/blob/master/errcode.h

    OK = Code(0)
    SYNTAX = Code(1, "syntax or usage error")
    PROTOCOL = Code(2, "protocol incompatibility")
    FILESELECT = Code(3, "errors selecting input/output files, dirs")
    UNSUPPORTED = Code(4, "requested action not supported")
    STARTCLIENT = Code(5, "error starting client-server protocol")

    SOCKETIO = Code(10, "error in socket IO")
    FILEIO = Code(11, "error in file IO")
    STREAMIO = Code(12, "error in rsync protocol data stream")
    MESSAGEIO = Code(13, "errors with program diagnostics")
    IPC = Code(14, "error in IPC code")
    CRASHED = Code(15, "sibling crashed")
    TERMINATED = Code(16, "sibling terminated abnormally")

    SIGNAL1 = Code(19, "status returned when sent SIGUSR1")
    SIGNAL = Code(20, "status returned when sent SIGINT, SIGTERM, SIGHUP")
    WAITCHILD = Code(21, "some error returned by waitpid()")
    MALLOC = Code(22, "error allocating core memory buffers")
    PARTIAL = Code(23, "partial transfer")
    VANISHED = Code(24, "file(s) vanished on sender side")
    DEL_LIMIT = Code(25, "skipped some deletes due to --max-delete")

    TIMEOUT = Code(30, "timeout in data send/receive")
    CONTIMEOUT = Code(35, "timeout waiting for daemon connection")

    CMD_FAILED = Code(124)
    CMD_KILLED = Code(125)
    CMD_RUN = Code(126)
    CMD_NOTFOUND = Code(127)


def get_error_code(code: int) -> RErr | None:
    for err in RErr:
        if err.code == code:
            return err
    return None
