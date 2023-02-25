#!/usr/bin/env python3
import logging
import os
import sys
from argparse import ArgumentParser
from pathlib import Path

from converters.json_converter import JsonConverter
from dumpres.all_in_one import AllInOneSaveStrategy
from dumpres.as_is_save_strategy import AsIsSaveStrategy
from dumpres.directory_save_strategy import DirectorySaveStrategy
from parsers.bs4_parser import BS4Parser
from pipe import Pipe

from vkparse import logger
from vkparse.dumpres.not_save import NotSave

_STR_TO_SAVE_STRATEGY = {
    "all-in-one": AllInOneSaveStrategy,
    "directory": DirectorySaveStrategy,
    "as-is": AsIsSaveStrategy,
}
_STR_TO_PARSER = {"bs4": BS4Parser}
_STR_TO_CONVERTER = {"json": JsonConverter}


def process(root: Path, save_strategy: str, out_dir: Path, *, debug_mode: bool) -> None:
    converter_cls = JsonConverter
    saver_cls = _STR_TO_SAVE_STRATEGY[save_strategy]
    if debug_mode:
        # Preventing hard drive wear
        saver_cls = NotSave

    saver = saver_cls(path=out_dir, file_ext="json", converter=converter_cls())
    parser_cls = BS4Parser

    dirs = [root / x for x in os.listdir(root)]
    pipe = Pipe(dirs, parser_cls(), saver)
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
    parser.add_argument(
        "--save-strategy",
        choices=("as-is", "directory", "all-in-one"),
        default="as-is",
        help="""collect converted.json messages in:
                as-is - single html to single converted file;
                directory - all files in directory to single converted file;
                all-in-one - all files in dump to single converted file;
                """,
    )

    args = parser.parse_args()

    debug_mode = False
    if os.getenv("VKPARSE_DEBUG"):
        logger.warning("You running vkparse in DEBUG mode")
        logger.setLevel(logging.DEBUG)
        debug_mode = True

    try:
        process(args.directory, args.save_strategy, args.output, debug_mode=debug_mode)
    except KeyboardInterrupt:
        return 0
    except Exception as e:
        logger.exception("an exception occurred", exc_info=e)
        return -1
    return 0


if __name__ == "__main__":
    sys.exit(main())
