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


def is_inputchar(keyval, state=0):
    """Is the `keyval` param an acceptable input character for Cangjie.

    Only lower case letters from a to z are possible input characters.
    """
    # Note: MOD1_MASK used to be called ALT_MASK in the static bindings
    # Should that be reported to IBus devs?
    return ((keyval in range(IBus.a, IBus.z + 1)) and
            (state & (IBus.ModifierType.CONTROL_MASK |
                      IBus.ModifierType.MOD1_MASK)) == 0)


class Engine(IBus.Engine):
    """The base class for Cangjie and Quick engines."""
    def __init__(self):
        super(Engine, self).__init__()

        self.preedit = u""

        self.lookuptable = IBus.LookupTable()
        self.lookuptable.set_page_size(9)
        self.lookuptable.set_round(True)
        self.lookuptable.set_orientation(IBus.Orientation.VERTICAL)

    def do_process_inputchar(self, keyval):
        """Handle user input of valid Cangjie input characters."""
        self.preedit += IBus.keyval_to_unicode(keyval)
        self.update()
        return True

    def do_process_key_event(self, keyval, keycode, state):
        """Handle `process-key-event` events.

        This event is fired when the user presses a key."""
        # Ignore key release events
        if (state & IBus.ModifierType.RELEASE_MASK):
            return False

        # Ignore arrow keys
        if keyval in (IBus.Up, IBus.Down, IBus.Left, IBus.Right):
            return False

        if is_inputchar(keyval, state):
            return self.do_process_inputchar(keyval)

        return False

    def update(self):
        """Update the user-visible elements.

        This sets the pre-edit and auxiliary texts, and populate the list of
        candidates.

        This is where the engine actually implements its core function:
        associating user input to CJK characters.
        """
        preedit_len = len(self.preedit)

        self.lookuptable.clear()
        if preedit_len > 0:
            # Add some dummy candidates
            import string
            for c in string.letters:
                self.lookuptable.append_candidate(IBus.Text.new_from_string(c))

        text = IBus.Text.new_from_string(self.preedit)
        self.update_auxiliary_text(text, preedit_len>0)
        # TODO: Underline the preedit text
        self.update_preedit_text(text, preedit_len, preedit_len>0)

        self.update_lookup_table(self.lookuptable,
                                 self.lookuptable.get_number_of_candidates()>0)


class EngineCangjie(Engine):
    """The Cangjie engine."""
    __gtype_name__ = "EngineCangjie"


class EngineQuick(Engine):
    """The Quick engine."""
    __gtype_name__ = "EngineQuick"
