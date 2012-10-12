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

# Note: This script is only used to manually start the engine, the IBus daemon
# will normally just load the XML file.

import argparse
import locale
import os
import sys

import gobject
import ibus

import factory

class IMApp(object):
    def __init__(self, exec_by_ibus):
        self.__component = ibus.Component("org.freedesktop.IBus.Cangjie",
                                          "Cangjie Component",
                                          "0.1.0",
                                          "LGPLv3+",
                                          "The IBus Cangjie authors")

        # TODO: Add the engines, based on the XML file

        self.__mainloop = gobject.MainLoop()
        self.__bus = ibus.Bus()
        self.__bus.connect("disconnected", self.__bus_disconnected_cb)
        self.__factory = factory.EngineFactory(self.__bus)
        if exec_by_ibus:
            self.__bus.request_name("org.freedesktop.IBus.Cangjie", 0)
        else:
            self.__bus.register_component(self.__component)

    def run(self):
        self.__mainloop.run()

    def __bus_disconnected_cb(self, bus):
        self.__mainloop.quit()


def launch_engine(exec_by_ibus):
    IMApp(exec_by_ibus).run()

def main():
    try:
        locale.setlocale(locale.LC_ALL, "")
    except:
        pass

    parser = argparse.ArgumentParser(description="Cangjie input method engine")
    parser.add_argument("--ibus", "-i", action="store_true",
                        help="let the engine know it is executed by IBus")
    parser.add_argument("--daemonize", "-d", action="store_true",
                        help="daemonize the engine")
    args = parser.parse_args()

    if args.daemonize:
        if os.fork():
            sys.exit()

    launch_engine(exec_by_ibus)

if __name__ == "__main__":
    main()
