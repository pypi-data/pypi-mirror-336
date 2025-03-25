#
# Copyright (c) 2024 Joshua Watt
#
# SPDX-License-Identifier: MIT
#

import subprocess
import sys

from spdx3toopenvex import VERSION


def test_program_exists():
    """
    Tests that the spdx3toopenvex program exists
    """
    subprocess.run(["spdx3toopenvex", "--help"], check=True)


def test_module_invocation():
    subprocess.run([sys.executable, "-m", "spdx3toopenvex", "--help"], check=True)


def test_version():
    """
    Tests that the version subcommand works
    """
    p = subprocess.run(
        ["spdx3toopenvex", "-V"],
        check=True,
        stdout=subprocess.PIPE,
        encoding="utf-8",
    )

    assert p.stdout.rstrip() == VERSION
