import abc
import datetime
import re
from typing import Generic, TypeVar

from . import types


T = TypeVar("T")


class StringParser(abc.ABC, Generic[T]):
    @classmethod
    @abc.abstractmethod
    def parse(cls, string: str) -> T | None:
        ...


class Remain(StringParser[datetime.timedelta]):
    PATTERN = r"(?P<hours>\d{,4}):(?P<minutes>\d{2}):(?P<seconds>\d{2})"

    @classmethod
    def parse(cls, string: str) -> datetime.timedelta | None:
        if remain_match := re.match(cls.PATTERN, string):
            remain_groups: types.RemainMatch = remain_match.groupdict()  # type: ignore

            return datetime.timedelta(
                hours=float(remain_groups["hours"]),
                minutes=float(remain_groups["minutes"]),
                seconds=float(remain_groups["seconds"]),
            )

        return None


class ProgressBar(StringParser[types.ProgressBar]):
    PATTERN = (
        r"(?P<offset>.+?)"
        r"\s+"
        r"(?P<percentage>\d{,3})%"
        r"\s+"
        r"(?P<rate>\d{,7}\.\d{2})"
        r"(?P<units>[GMk]B/s)"
        r"\s+"
        r"(?P<remain>(\?{2}:\?{2}:\?{2})|(\d{,4}:\d{2}:\d{2}))"
    )

    @classmethod
    def parse(cls, string: str) -> types.ProgressBar | None:
        if match := re.match(cls.PATTERN, string):
            groups: types.ProgressBarMatch = match.groupdict()  # type: ignore

            remain = Remain.parse(groups["remain"])

            return types.ProgressBar(
                offset=groups["offset"],
                percentage=int(groups["percentage"]),
                rate=float(groups["rate"]),
                units=groups["units"],
                remain=remain,
            )

        return None
