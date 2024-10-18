#!/usr/bin/env python3
#
# This file is part of the JetBrains Manager Tool distribution
# (https://github.com/diogocaveiro/jetbrains-manager-tool).
# Copyright (c) 2024 Diogo Caveiro.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
import re
import shutil
from pprint import pformat

import requests
import argparse
import os
import subprocess
import sys
import xml.etree.ElementTree as elementTree
import json
import logging

__author__ = "Diogo Caveiro"
__date__ = "2024-09-18"
__version__ = "0.4.5"
__github__ = "https://github.com/diogocaveiro"
__license__ = "GPLv3 License"

SCRIPT_DIRECTORY = os.path.dirname(os.path.realpath(__file__))


class Help:
    @staticmethod
    def show_help_documentation():
        """
        Displays the help documentation using the 'less' command.

        This function attempts to open a Markdown file containing help documentation with the 'less' command.

        Raises:
            FileNotFoundError: If the 'less' command is not installed or the documentation file does not exist.
            Exception: For any other exceptions that occur when attempting to open the documentation.
        """

        help_path = os.path.join(SCRIPT_DIRECTORY, 'help_pages.md')

        try:
            subprocess.run(['less', docs_path], shell=False)

        except FileNotFoundError:
            print(f"Unable to open documentation. Make sure 'less' is installed and the documentation file exists "
                    f"at {docs_path}")

        except Exception:
            print('Error opening documentation.')

