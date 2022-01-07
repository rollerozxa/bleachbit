#!/usr/bin/env python
# vim: ts=4:sw=4:expandtab

# BleachBit
# Copyright (C) 2008-2021 Andrew Ziem
# https://www.bleachbit.org
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
Build BleachBit tarballs and exe
"""

import glob
import os
import sys
import tempfile
from setuptools import setup

import bleachbit
import bleachbit.General
import bleachbit.FileUtilities

APP_NAME = "BleachBit - Free space and maintain privacy"
APP_DESCRIPTION = "BleachBit frees space and maintains privacy by quickly wiping files you don't need and didn't know you had. Supported applications include Edge, Firefox, Google Chrome, VLC, and many others."

data_files = []
if sys.platform.startswith('linux'):
    data_files.append(('/usr/share/applications', ['./org.bleachbit.BleachBit.desktop']))
    data_files.append(('/usr/share/pixmaps/', ['./bleachbit.png']))
elif sys.platform[:6] == 'netbsd':
    data_files.append(('/usr/pkg/share/applications', ['./org.bleachbit.BleachBit.desktop']))
    data_files.append(('/usr/pkg/share/pixmaps/', ['./bleachbit.png']))
elif sys.platform.startswith('openbsd') or sys.platform.startswith('freebsd'):
    data_files.append(
        ('/usr/local/share/applications', ['./org.bleachbit.BleachBit.desktop']))
    data_files.append(('/usr/local/share/pixmaps/', ['./bleachbit.png']))

args = {}

def run_setup():
    setup(name='bleachbit',
          version=bleachbit.APP_VERSION,
          description=APP_NAME,
          long_description=APP_DESCRIPTION,
          author="Andrew Ziem",
          author_email="andrew@bleachbit.org",
          download_url="https://www.bleachbit.org/download",
          license="GPLv3",
          url=bleachbit.APP_URL,
          platforms='Linux; Python v2.6 and 2.7; GTK v3.12+',
          packages=['bleachbit', 'bleachbit.markovify'],
          **args)


if __name__ == '__main__':
    run_setup()
