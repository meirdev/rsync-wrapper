import sys
from typing import NoReturn

from . import rsync, utils


def main() -> NoReturn:
    sys.exit(utils.rich_progress(rsync(*sys.argv[1:])))


if __name__ == "__main__":
    main()
