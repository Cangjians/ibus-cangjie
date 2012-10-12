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


__all__ = ["EngineCangjie", "EngineQuick"]


from gi.repository import IBus


class Engine(IBus.Engine):
    def __init__(self):
        super(Engine, self).__init__()
        # TODO: Implement the specific stuff

    def do_process_key_event(self, keyval, keycode, state):
        # TODO: Implement that stuff
        pass

    def page_up(self):
        if self.__lookup_table.page_up():
            self.page_up_lookup_table()
            return True
        return False

    def page_down(self):
        if self.__lookup_table.page_down():
            self.page_down_lookup_table()
            return True
        return False


class EngineCangie(Engine):
    __gtype_name__ = "EngineCangjie"

class EngineQuick(Engine):
    __gtype_name__ = "EngineQuick"
