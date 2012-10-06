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

import ibus
import engine


class EngineFactory(ibus.EngineFactoryBase):
    def __init__(self, bus):
        self.__bus = bus
        super(EngineFactory, self).__init__(self.__bus)

        self.__id = 0

    def create_engine(self, engine_name):
        # TODO: Do the specific stuff
        return super(EngineFactory, self).create_engine(engine_name)

