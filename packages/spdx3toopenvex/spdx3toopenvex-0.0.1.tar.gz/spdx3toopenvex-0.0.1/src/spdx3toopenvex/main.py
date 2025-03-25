#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
#

import argparse
import json
import sys
from contextlib import contextmanager
from pathlib import Path

from . import convert
from .version import VERSION


@contextmanager
def input_file(arg):
    if arg == Path("-"):
        yield sys.stdin
    else:
        with arg.open("r") as f:
            yield f


@contextmanager
def output_file(arg):
    if arg == Path("-"):
        yield sys.stdout
    else:
        with arg.open("w") as f:
            yield f


def main():
    parser = argparse.ArgumentParser(description="Convert SPDX 3 VEX to OpenVEX")
    parser.add_argument(
        "--spdx-in",
        "-i",
        metavar="SPDX",
        type=Path,
        default=Path("-"),
        help="Input SPDX 3 file, or '-' for stdin. Default is '%(default)s'",
    )
    parser.add_argument(
        "--openvex-out",
        "-o",
        metavar="OPENVEX",
        type=Path,
        default=Path("-"),
        help="Output OpenVEX file or '-' for stdout. Default is '%(default)s'",
    )
    parser.add_argument(
        "--pretty",
        "-p",
        action="store_true",
        help="Write out pretty OpenVEX JSON",
    )
    parser.add_argument(
        "--author",
        "-a",
        metavar="NAME",
        required=True,
        help="Document author (a person or company)",
    )
    parser.add_argument(
        "--version",
        "-V",
        version=VERSION,
        action="version",
    )
    args = parser.parse_args()

    with input_file(args.spdx_in) as f:
        data = convert.convert_spdx_to_openvex(f, args.author)

    with output_file(args.openvex_out) as f:
        json.dump(data, f, indent="  " if args.pretty else None)

    return 0
