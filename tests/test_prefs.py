# Copyright (c) 2013 - The IBus Cangjie authors
#
# This file is part of ibus-cangjie, the IBus Cangjie input method engine.
#
# ibus-cangjie is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-cangjie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-cangjie.  If not, see <http://www.gnu.org/licenses/>.


import os
import unittest


class PrefsTestCase(unittest.TestCase):
    def setUp(self):
        self.ui_file = os.path.join(os.environ["PREFERENCES_UI_DIR"],
                                    "setup.ui")

    def tearDown(self):
        pass

    def test_ui_file_is_valid_xml(self):
        from xml.etree import ElementTree as ET

        try:
            ET.parse(self.ui_file)

        except ET.ParseError as e:
            raise AssertionError(e)
