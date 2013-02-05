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

from gi.repository import Gdk
from gi.repository import GLib
from gi.repository import Gtk

from ibus_cangjie.config import options, Config


_ = lambda a : gettext.dgettext(gettext_package, a)


class Setup(object):
    def __init__ (self, bus, engine, datadir, gettext_package):
        self.__config = Config(bus, engine, self.on_value_changed)

        ui_file = GLib.build_filenamev([datadir, "setup.ui"])
        self.__builder = Gtk.Builder()
        self.__builder.set_translation_domain(gettext_package)
        self.__builder.add_from_file(ui_file)

        for option in options:
            prepare_func = getattr(self, "prepare_%s" % option["widget"])
            prepare_func(option)

        self.__window = self.__builder.get_object("setup_dialog")
        self.__window.set_title("%s Preferences" % engine.capitalize())

        try:
            # Pretend to be a GNOME Control Center dialog if appropriate
            self.gnome_cc_xid = int(GLib.getenv('GNOME_CONTROL_CENTER_XID'))
            self.__window.set_wmclass('gnome-control-center',
                                      'Gnome-control-center')
            self.__window.set_modal(True)
            self.__window.connect('notify::window', self.set_transient)
            self.__window.set_type_hint(Gdk.WindowTypeHint.DIALOG)

        except:
            # No problem here, we're just a normal dialog
            pass

        self.__window.show()

    def set_transient(self, obj, pspec):
        from gi.repository import GdkX11
        window = self.__window.get_window()
        if window != None:
            parent = GdkX11.X11Window.foreign_new_for_display(
                         Gdk.Display.get_default(), self.gnome_cc_xid)

        if parent != None:
            window.set_transient_for(parent)

    def prepare_switch(self, option):
        """Prepare a Gtk.Switch

        Set the switch named `option["name"]` (in)active based on the current
        engine config value.
        """
        name = option["name"]

        switch = self.__builder.get_object(name)

        v = self.__config.read(name)
        switch.set_active(v.unpack())
        switch.connect("notify::active", self.on_switch_toggled,
                       name, option["type"])

        setattr(self, name, switch)

    def prepare_combo(self, option):
        """Prepare a Gtk.ComboBox

        Set the combobox named `option['name']` to the current engine config
        value.
        """
        name = option["name"]
        values = option["values"]
        labels = option["labels"]
        current_value = self.__config.read(name).unpack()

        combo = self.__builder.get_object(name)

        store = Gtk.ListStore(type(values[0]), type(labels[0]))
        for i, n in enumerate(values):
            v = labels[i]
            store.append((n, v))
        combo.set_model(store)
        cell = Gtk.CellRendererText()
        combo.pack_start(cell, True)
        combo.add_attribute(cell, "text", 1)

        combo.set_active(values.index(current_value))
        combo.connect("changed", self.on_combo_changed, name, option)

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

        try:
            widget = getattr(self, name)
        except AttributeError:
            return

        value = value.unpack()

        if isinstance(widget, Gtk.ComboBox):
            for option in options:
                if option["name"] != name:
                    continue

                values = option["values"]
                if values[widget.get_active()] != value:
                    widget.set_active(values.index(value))

        else:
            if widget.get_active() != value:
                widget.set_active(value)

    def on_switch_toggled(self, widget, active, setting_name, variant_type):
        self.__config.write(setting_name, GLib.Variant(variant_type, widget.get_active()))

    def on_combo_changed(self, widget, setting_name, option):
        value = option["values"][widget.get_active()]
        self.__config.write(setting_name, GLib.Variant(option["type"], value))
