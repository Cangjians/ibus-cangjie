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


def has_graphical():
    """Detect if we have graphical capabilities

    It is very common to run the unit tests in an environment which does not
    have any graphical capabilities.

    This is for example the case in a CI server, or when building RPMs for
    Fedora.

    This function is useful to detect these situation, so that we can
    automatically skip the tests which can't run without.
    """
    try:
        import gi
        gi.require_version('Gtk', '3.0')
        from gi.repository import Gtk

    except RuntimeError as e:
        # On some platforms (e.g Ubuntu 12.04 where our CI is running) we
        # can't import Gtk without a display.
        return False

    # But other platforms (e.g Fedora 21) can import Gtk just fine even
    # without a display...

    gi.require_version('Gdk', '3.0')
    from gi.repository import Gdk

    if Gdk.Display.get_default() is None:
        # ... We don't have a display
        return False

    return True


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

    @unittest.skipUnless(has_graphical(), "Can't use GtkBuilder")
    def test_ui_file_is_valid_gtk_builder(self):
        from gi.repository import Gtk
        b = Gtk.Builder()

        try:
            b.add_from_file(self.ui_file)

        except Exception as e:
            raise AssertionError(e)
