# Copyright (c) 2012-2013 - The IBus Cangjie authors
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


from gettext import dgettext

from gi.repository import Gdk
from gi.repository import Gio
from gi.repository import GLib
from gi.repository import Gtk


class Setup(object):
    def __init__ (self, engine, datadir, gettext_package):
        self.settings = Gio.Settings("org.cangjians.ibus.%s" % engine)
        self.settings.connect("changed", self.on_value_changed)

        ui_file = GLib.build_filenamev([datadir, "setup.ui"])
        self.__builder = Gtk.Builder()
        self.__builder.set_translation_domain(gettext_package)
        self.__builder.add_from_file(ui_file)

        for key in ("version", ):
            combo = self.__builder.get_object(key)
            active = self.__get_active_combo_index(combo.get_model(),
                                                   self.settings.get_int(key))
            combo.set_active(active)
            combo.connect("changed", self.on_combo_changed, key)
            setattr(self, "widget_%s" % key, combo)

        for key in ("include-allzh", "include-jp",
                    "include-zhuyin", "include-symbols"):
            switch = self.__builder.get_object(key)
            switch.set_active(self.settings.get_boolean(key))
            switch.connect("notify::active", self.on_switch_toggled, key)
            setattr(self, "widget_%s" % key, switch)

        self.__window = self.__builder.get_object("setup_dialog")

        if engine == "cangjie":
            title = dgettext(gettext_package, "Cangjie Preferences")
        elif engine == "quick":
            title = dgettext(gettext_package, "Quick Preferences")

        self.__window.set_title(title)

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

    def __get_active_combo_index(self, store, value):
        for i, n in enumerate(store):
            v = store.get_value(store.get_iter(i), 0)
            if v == value:
                return i

    def run(self):
        res = self.__window.run()
        self.__window.destroy()

    def on_value_changed(self, settings, key):
        """Callback when the value of a widget is changed.

        We need to react, in case the value was changed from somewhere else,
        for example from another setup UI.
        """
        if key == "version":
            new_value = self.settings.get_int(key)

        else:
            new_value = self.settings.get_boolean(key)

        widget = getattr(self, "widget_%s" % key)

        if isinstance(widget, Gtk.ComboBox):
            store = widget.get_model()
            v = store.get_value(store.get_iter(widget.get_active()), 0)
            if v != new_value:
                active = self.__get_active_combo_index(widget.get_model(),
                                                       new_value)
                widget.set_active(active)

        else:
            if widget.get_active() != new_value:
                widget.set_active(new_value)

    def on_switch_toggled(self, widget, active, key):
        self.settings.set_boolean(key, widget.get_active())

    def on_combo_changed(self, widget, key):
        store = widget.get_model()
        value = store.get_value(store.get_iter(widget.get_active()), 0)
        self.settings.set_int(key, value)
