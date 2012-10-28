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
    """The base class for Cangjie and Quick engines."""
    def __init__(self):
        super(Engine, self).__init__()

        self.lookuptable = IBus.LookupTable()
        self.lookuptable.set_page_size(9)
        self.lookuptable.set_round(True)
        self.lookuptable.set_orientation(IBus.Orientation.VERTICAL)

    def do_process_key_event(self, keyval, keycode, state):
        """Handle `process-key-event` events.

        This event is fired when the user presses a key."""
        # Ignore key release events
        if (state & IBus.ModifierType.RELEASE_MASK):
            return False

        # Ignore arrow keys
        if keyval in (IBus.Up, IBus.Down, IBus.Left, IBus.Right):
            return False

        return False


class EngineCangjie(Engine):
    """The Cangjie engine."""
    __gtype_name__ = "EngineCangjie"


class EngineQuick(Engine):
    """The Quick engine."""
    __gtype_name__ = "EngineQuick"
