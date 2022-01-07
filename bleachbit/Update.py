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
Check for updates via the Internet
"""

import bleachbit
from bleachbit import _

import hashlib
import logging
import os
import os.path
import platform
import socket
import sys
import xml.dom.minidom
from urllib.request import build_opener
from urllib.error import URLError


logger = logging.getLogger(__name__)


def user_agent():
    """Return the user agent string"""
    __platform = platform.system()  # Linux or Windows
    __os = platform.uname()[2]  # e.g., 2.6.28-12-generic or XP
    if sys.platform.startswith('linux'):
        dist = platform.linux_distribution()
        # example: ('fedora', '11', 'Leonidas')
        # example: ('', '', '') for Arch Linux
        if 0 < len(dist[0]):
            __os = dist[0] + '/' + dist[1] + '-' + dist[2]
    elif sys.platform[:6] == 'netbsd':
        __sys = platform.system()
        mach = platform.machine()
        rel = platform.release()
        __os = __sys + '/' + mach + ' ' + rel

    try:
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk
        gtkver = 'GTK %s' % '.'.join([str(x) for x in Gtk.gtk_version])
    except:
        gtkver = ""

    agent = "BleachBit/%s (%s; %s; %s)" % (bleachbit.APP_VERSION,
                                             __platform, __os, gtkver)
    return agent
