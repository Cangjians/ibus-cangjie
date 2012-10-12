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


import argparse
import locale
import os
import sys

from gi.repository import GLib
from gi.repository import IBus

import engine


class IMApp(object):
    def __init__(self, exec_by_ibus, engine_name):
        self.__component = IBus.Component("org.freedesktop.IBus.Cangjie",
                                          "Cangjie Component",
                                          "0.1.0",
                                          "LGPLv3+",
                                          "The IBus Cangjie authors")

        # TODO: Add the engines, based on the XML file

        self.__mainloop = GLib.MainLoop()
        self.__bus = IBus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = IBus.Factory(self.__bus.__get_connection())
        if exec_by_ibus:
            self.__bus.request_name("org.freedesktop.IBus.Cangjie", 0)
        else:
            self.__bus.register_component(self.__component)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


if __name__ == "__main__":
    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass

    parser = argparse.ArgumentParser(description="Cangjie input method engine")
    parser.add_argument("--ibus", "-i", action="store_true",
                        help="let the engine know it is executed by IBus")
    parser.add_argument("--daemonize", "-d", action="store_true",
                        help="daemonize the engine")
    parser.add_argument("engine", choices=("cangjie", "quick"),
                        help="Input method engine to use")
    args = parser.parse_args()

    if args.daemonize:
        if os.fork():
            sys.exit()

    IBus.init()
    IMApp(args.ibus, args.engine).run()
