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

from vkparse.dumpres.not_save import NotSave

_STR_TO_SAVE_STRATEGY = {
    "all-in-one": AllInOneSaveStrategy,
    "directory": DirectorySaveStrategy,
    "as-is": AsIsSaveStrategy,
}

_STR_TO_PARSER = {"bs4": BS4Parser}

_STR_TO_CONVERTER = {"json": JsonConverter}

logger = logging.getLogger(__name__)


def process(
    root: Path, parser: str, file_ext: str, save_strategy: str, out_dir: Path
) -> None:
    converter_cls = _STR_TO_CONVERTER[file_ext]
    saver_cls = _STR_TO_SAVE_STRATEGY[save_strategy]
    if os.getenv("VKPARSE_DEBUG"):
        # Preventing hard drive wear
        logger.warning("You running vkparse in DEBUG mode")
        saver_cls = NotSave
    saver = saver_cls(path=out_dir, file_ext=file_ext, converter=converter_cls())
    parser_cls = _STR_TO_PARSER[parser]

    dirs = list(map(lambda x: root / x, os.listdir(root)))
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
    # TODO:
    parser.add_argument("-q", "--quite", action="store_true", help="disable any output")
    parser.add_argument(
        "-f",
        "--format",
        choices=("json", "csv", "sqlite3"),
        default="json",
        help="convert format",
    )
    parser.add_argument(
        "-p",
        "--parser",
        choices=("bs4",),
        default="bs4",
        help="parser implementation",
    )
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

    process(
        args.directory,
        args.parser,
        args.format,
        args.save_strategy,
        args.output,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
