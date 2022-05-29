import datetime
from typing import Iterator, NamedTuple, TypedDict


class ProgressBarMatch(TypedDict):
    offset: str
    percentage: str
    rate: str
    units: str
    remain: str


class RemainMatch(TypedDict):
    hours: str
    minutes: str
    seconds: str


class ProgressBar(NamedTuple):
    offset: str
    percentage: int
    rate: float
    units: str
    remain: datetime.timedelta | None


class StdErr(str):
    pass


class StdOut(str):
    pass


class ExitCode(int):
    pass


BasicOutput = StdErr | StdOut | ExitCode

BasicOutputIterator = Iterator[BasicOutput]

Output = ProgressBar | StdErr | StdOut | ExitCode

OutputIterator = Iterator[Output]
