#!/usr/bin/env python3
import logging
import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from parsers.bs4_parser import BS4Parser
from pipe import Pipe

from vkparse import logger
from vkparse.driver.json_driver import JsonDriver
from vkparse.models.message import Message


def process(root: Path, out_dir: Path, *, debug_mode: bool) -> None:
    dirs = [root / x for x in os.listdir(root)]
    driver = JsonDriver(out_dir)
    if debug_mode:
        from vkparse.driver.driver import Driver

        class DummyDriver(Driver):
            def on_message(self, message: Message) -> None:
                pass

        driver = DummyDriver()

    pipe = Pipe(dirs, BS4Parser(), driver)
    pipe.process()


def main() -> int:
    parser = ArgumentParser(
        prog="vkgdprparse",
        description="%(prog)s: Convert VK GDPR dumps to JSON/CSV/SQLite3",
    )
    parser.add_argument("directory", type=Path, help="directory with messages dump")
    # TODO:
    parser.add_argument(
        "-i",
        "--ids",
        nargs="+",
        help="specified conversations id(by default parse all messages)",
    )
    parser.add_argument("-q", "--quite", action="store_true", help="disable any output")
    # FIXME: file extension
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default="./converted",
        help="directory with converted messages",
    )

    args = parser.parse_args()

    debug_mode = False
    if os.getenv("VKPARSE_DEBUG"):
        logger.warning("You running vkparse in DEBUG mode")
        logger.setLevel(logging.DEBUG)
        debug_mode = True

    try:
        process(args.directory, args.output, debug_mode=debug_mode)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        logger.exception("an exception occurred", exc_info=e)
        return -1
    return 0


if __name__ == "__main__":
    sys.exit(main())
