# Copyright (c) 2012 - The IBus Cangjie authors
#
# This file is part of ibus-cangjie, the IBus Cangjie input method engine.
#
# ibus-cangjie is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ibus-cangjie is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with ibus-cangjie.  If not, see <http://www.gnu.org/licenses/>.


import gettext
import locale
import sys

from gi.repository import GLib
from gi.repository import Gtk
from gi.repository import IBus

import config


_ = lambda a : gettext.dgettext(config.gettext_package, a)


class Setup(object):
    def __init__ (self, bus):
        self.__bus = bus
        self.__config = self.__bus.get_config()
        self.__config.connect("value-changed", self.on_value_changed, None)

        ui_file = GLib.build_filenamev([GLib.path_get_dirname(__file__),
                                       "setup.ui"])
        self.__builder = Gtk.Builder()
        self.__builder.set_translation_domain(config.gettext_package)
        self.__builder.add_from_file(ui_file)

        # setup dialog
        self.__window = self.__builder.get_object("setup_dialog")
        self.__window.set_title("Preferences for Cangjie")
        self.__window.show()

    def run(self):
        res = self.__window.run()
        self.__window.destroy()

    def on_value_changed(self, config, section, name, value, data):
        if section == "engine/Cangjie":
            print("[%s] Option %s was set to %s" % (section, name, value))
            print("     Data: %s" % data)

    def __read(self, name):
        return self.__config.get_value("engine/Cangjie", name)

    def __write(self, name, v):
        return self.__config.set_value("engine/Cangjie", name, v)


if __name__ == "__main__":
    locale.bindtextdomain(config.gettext_package, config.localedir)
    locale.bind_textdomain_codeset(config.gettext_package, "UTF-8")

    try:
        bus = IBus.Bus()

    except:
        message = [_("IBus daemon is not running."),
                   _("Cangjie engine settings cannot be saved.")]
        dialog = Gtk.MessageDialog(type = Gtk.MessageType.ERROR,
                                   buttons = Gtk.ButtonsType.CLOSE,
                                   message_format = "\n".join(message))
        dialog.run()
        sys.exit(1)

    Setup(bus).run()
