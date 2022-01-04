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

def recompile_mo(langdir, app, langid, dst):
    """Recompile gettext .mo file"""

    if not bleachbit.FileUtilities.exe_exists('msgunfmt') and not bleachbit.FileUtilities.exe_exists('msgunfmt.exe'):
        print('warning: msgunfmt missing: skipping recompile')
        return

    mo_pathname = os.path.normpath('%s/LC_MESSAGES/%s.mo' % (langdir, app))
    if not os.path.exists(mo_pathname):
        print('info: does not exist: %s', mo_pathname)
        return

    # decompile .mo to .po
    po = os.path.join(dst, langid + '.po')
    __args = ['msgunfmt', '-o', po,
              mo_pathname]
    ret = bleachbit.General.run_external(__args)
    if ret[0] != 0:
        raise RuntimeError(ret[2])

    # shrink .po
    po2 = os.path.join(dst, langid + '.po2')
    __args = ['msgmerge', '--no-fuzzy-matching', po,
              os.path.normpath('windows/%s.pot' % app),
              '-o', po2]
    ret = bleachbit.General.run_external(__args)
    if ret[0] != 0:
        raise RuntimeError(ret[2])

    # compile smaller .po to smaller .mo
    __args = ['msgfmt', po2, '-o', mo_pathname]
    ret = bleachbit.General.run_external(__args)
    if ret[0] != 0:
        raise RuntimeError(ret[2])

    # clean up
    os.remove(po)
    os.remove(po2)


def supported_languages():
    """Return list of supported languages by scanning ./po/"""
    langs = []
    for pathname in glob.glob('po/*.po'):
        basename = os.path.basename(pathname)
        langs.append(os.path.splitext(basename)[0])
    return sorted(langs)


def clean_dist_locale():
    """Clean dist/share/locale"""
    tmpd = tempfile.mkdtemp('gtk_locale')
    langs = supported_languages()
    basedir = os.path.normpath('dist/share/locale')
    for langid in sorted(os.listdir(basedir)):
        langdir = os.path.join(basedir, langid)
        if langid in langs:
            print("recompiling supported GTK language = %s" % langid)
            # reduce the size of the .mo file
            recompile_mo(langdir, 'gtk30', langid, tmpd)
        else:
            print("removing unsupported GTK language = %s" % langid)
            # remove language supported by GTK+ but not by BleachBit
            cmd = 'rd /s /q ' + langdir
            print(cmd)
            os.system(cmd)
    os.rmdir(tmpd)


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
    if 2 == len(sys.argv) and sys.argv[1] == 'clean-dist':
        clean_dist_locale()
    else:
        run_setup()
