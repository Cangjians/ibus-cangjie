# Copyright (c) 2012-2013 - The IBus Cangjie authors
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
# FIXME: Find a way to de-hardcode the gettext package
_ = lambda x: gettext.dgettext("ibus-cangjie", x)

from gi.repository import GLib


options = ({"name": "version",
            "type": "i",
            "widget": "combo",
            "default": 3},
           {"name": "include_sc",
            "type": "b",
            "widget": "switch",
            "default": False},
            )
properties = ({"name": "halfwidth_chars",
               "label": _("Half-Width Characters"),
               "type": "b",
               "default": False},
              )

class Config(object):
    def __init__(self, bus, engine, on_value_changed_cb):
        self.config_section = "engine/%s" % engine

        self.__ibus_config = bus.get_config()
        self.__ibus_config.connect("value-changed", on_value_changed_cb, None)

        self.__ensure_default_values()

    def __ensure_default_values(self):
        for option in options+properties:
            name = option["name"]
            value = self.read(name)

            if value is None:
                value = GLib.Variant(option["type"], option["default"])
                self.write(name, value)

    def read(self, name):
        return self.__ibus_config.get_value(self.config_section, name)

    def write(self, name, v):
        return self.__ibus_config.set_value(self.config_section, name, v)
