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
Test case for module Update
"""


from tests import common
import bleachbit
from bleachbit import logger
from bleachbit.Update import user_agent
import bleachbit.Update

import os
import os.path


class UpdateTestCase(common.BleachbitTestCase):
    """Test case for module Update"""

    def test_update_url(self):
        """Check connection to the update URL"""
        from bleachbit.Update import build_opener
        opener = build_opener()
        opener.addheaders = [('accept','text/*')]
        import urllib
        try:
            handle = opener.open(bleachbit.update_check_url)
        except urllib.error.HTTPError as e:
            logger.exception('HTTP error, url: %s\nheaders:\n%s', bleachbit.update_check_url, e.headers)
            raise e
        doc = handle.read()
        import xml
        xml.dom.minidom.parseString(doc)

    def test_user_agent(self):
        """Unit test for method user_agent()"""
        agent = user_agent()
        logger.debug("user agent = '%s'", agent)
        self.assertIsString(agent)

    def test_environment(self):
        """Check the sanity of the environment"""
        import http.client
        self.assertTrue(hasattr(http.client, 'HTTPSConnection'))
