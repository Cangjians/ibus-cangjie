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


from gi.repository import GLib
from gi.repository import GObject
from gi.repository import IBus

from .engine import *


class IMApp(object):
    def __init__(self, exec_by_ibus, engine_name, componentdir):
        component_path = GLib.build_filenamev([componentdir,
                                               "%s.xml" % engine_name])
        self.__component = IBus.Component.new_from_file(component_path)

        self.__mainloop = GLib.MainLoop()

        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)

        self.__factory = IBus.Factory.new(self.__bus.get_connection())
        engine_classtype = "Engine%s" % engine_name.capitalize()
        self.__factory.add_engine(engine_name,
                                  GObject.type_from_name(engine_classtype))

        if exec_by_ibus:
            self.__bus.request_name(self.__component.get_name(), 0)
        else:
            self.__bus.register_component(self.__component)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()
