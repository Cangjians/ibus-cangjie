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

from gi.repository import GLib
from gi.repository import Gtk

from ibus_cangjie.config import (datadir, gettext_package,
                                 options, Config)


_ = lambda a : gettext.dgettext(gettext_package, a)


class Setup(object):
    def __init__ (self, bus, engine):
        self.__config = Config(bus, engine, self.on_value_changed,
                               read_only=False)

        ui_file = GLib.build_filenamev([datadir, "setup.ui"])
        self.__builder = Gtk.Builder()
        self.__builder.set_translation_domain(gettext_package)
        self.__builder.add_from_file(ui_file)

        for option in options:
            if option["name"] == "punctuation_chars":
                self.__prepare_combo(option)

            else:
                self.__prepare_button(option)

        self.__window = self.__builder.get_object("setup_dialog")
        self.__window.set_title("%s settings" % engine.capitalize())
        self.__window.show()

    def __prepare_button(self, option):
        """Prepare a Gtk.CheckButton

        Set the button named `option['name']` (in)active based on the current
        engine config value.
        """
        name = option["name"]

        button = self.__builder.get_object(name)

        v = self.__config.read(name)
        button.set_active(v.unpack())
        button.connect("toggled", self.on_widget_changed, name, option["type"])

        setattr(self, name, button)

    def __prepare_combo(self, option):
        """Prepare a Gtk.ComboBox

        Set the combobox named `name` to the current engine config value, or
        to the provided `default_value` as a fallback.
        """
        name = option["name"]
        values = option["values"]

        combo = self.__builder.get_object(name)

        store = Gtk.ListStore(*[type(v) for v in values[0]])
        for n, v in values:
            store.append((n, v))
        combo.set_model(store)
        cell = Gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, "text", 1)

        v = self.__config.read(name)
        combo.set_active(v.unpack())
        combo.connect("changed", self.on_widget_changed, name, option["type"])

        setattr(self, name, combo)

    def run(self):
        res = self.__window.run()
        self.__window.destroy()

    def on_value_changed(self, config, section, name, value, data):
        """Callback when the value of a widget is changed.

        We need to react, in case the value was changed from somewhere else,
        for example from another setup UI.
        """
        if section != self.__config.config_section:
            return

        value = value.unpack()
        widget = getattr(self, name)

        if widget.get_active() != value:
            widget.set_active(value)

    def on_widget_changed(self, widget, setting_name, variant_type):
        self.__config.write(setting_name, GLib.Variant(variant_type, widget.get_active()))
