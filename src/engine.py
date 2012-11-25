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


import math

from gi.repository import IBus
import pycanberra

import cangjie

from .config import Config


def is_inputchar(keyval, state=0):
    """Is the `keyval` param an acceptable input character for Cangjie.

    Only lower case letters from a to z are possible input characters.
    """
    return ((keyval in range(IBus.a, IBus.z + 1)) and
            (state & (IBus.ModifierType.CONTROL_MASK |
                      IBus.ModifierType.MOD1_MASK)) == 0)

def get_inputnumber(keyval):
    """Is the `keyval` param a numeric input, to select a candidate."""
    if keyval in range(getattr(IBus, "1"), getattr(IBus, "9")+1):
         return IBus.keyval_to_unicode(keyval)

    else:
         return False


class Engine(IBus.Engine):
    """The base class for Cangjie and Quick engines."""
    def __init__(self):
        super(Engine, self).__init__()

        self.config = Config(IBus.Bus(), self.config_name,
                             self.on_value_changed)

        self.preedit = u""

        self.lookuptable = IBus.LookupTable()
        self.lookuptable.set_page_size(9)
        self.lookuptable.set_round(True)
        self.lookuptable.set_orientation(IBus.Orientation.VERTICAL)

        self.init_cangjie()

    def init_cangjie(self):
        new_version = self.config.read("use_new_version")
        version = getattr(cangjie.versions,
                          "CANGJIE%d" % (5 if new_version else 3))

        all_cjk = self.config.read("include_all_cjk")
        lang = getattr(cangjie.languages,
                       "ALL_CJK" if all_cjk else "TRADITIONAL")

        self.cangjie = cangjie.CangJie(version, lang)

    def on_value_changed(self, config, section, name, value, data):
        if section != self.config.config_section:
            return

        self.init_cangjie()

    def do_cancel_input(self):
        """Cancel the current input.

        However, if there isn't any pre-edit, then we shouldn't try to do
        anything at all, so that the key can fulfill its original function.
        """
        if not self.preedit:
            return False

        self.update_preedit_text(u"")
        self.update_lookup_table()
        self.update_auxiliary_text()
        return True

    def do_page_down(self):
        """Present the next page of candidates.

        However, if there isn't any pre-edit, then we shouldn't try to do
        anything at all, so that the key can fulfill its original function.
        """
        if not self.preedit:
            return False

        self.lookuptable.page_down()
        self.update_lookup_table()
        self.update_auxiliary_text()
        return True

    def do_page_up(self):
        """Present the previous page of candidates.

        However, if there isn't any pre-edit, then we shouldn't try to do
        anything at all, so that the key can fulfill its original function.
        """
        if not self.preedit:
            return False

        self.lookuptable.page_up()
        self.update_lookup_table()
        self.update_auxiliary_text()
        return True

    def do_backspace(self):
        """Go back from one input character.

        This doesn't cancel the current input, only removes the last
        user-inputted character from the pre-edit text.

        However, if there isn't any pre-edit, then we shouldn't handle the
        backspace key at all, so that it can fulfill its original function:
        deleting characters backwards.
        """
        if not self.preedit:
            return False

        self.update_preedit_text(self.preedit[:-1])
        self.update_auxiliary_text()
        return True

    def do_select_candidate(self, index):
        """Commit the selected candidate.

        Parameter `index` is the number entered by the user corresponding to
        the character she wishes to select on the current page.

        Note: user-visible index starts at 1, but start at 0 in the lookup
        table.
        """
        page_index = self.lookuptable.get_cursor_pos()
        selected = self.lookuptable.get_candidate(page_index+index-1)
        self.commit_text(selected)
        return True

    def do_process_key_event(self, keyval, keycode, state):
        """Handle `process-key-event` events.

        This event is fired when the user presses a key."""
        # Ignore key release events
        if (state & IBus.ModifierType.RELEASE_MASK):
            return False

        if keyval == IBus.Escape:
            return self.do_cancel_input()

        if keyval == IBus.space:
            return self.do_space()

        if keyval == IBus.Page_Down:
            return self.do_page_down()

        if keyval == IBus.Page_Up:
            return self.do_page_up()

        if keyval == IBus.BackSpace:
            return self.do_backspace()

        if is_inputchar(keyval, state):
            return self.do_process_inputchar(keyval)

        select_candidate = get_inputnumber(keyval)
        if select_candidate:
            return self.do_select_candidate(int(select_candidate))

        return self.do_other_key(keyval)

    def update_preedit_text(self, new_text):
        """Update the preedit text."""
        self.preedit = new_text

    def get_candidates(self):
        """Get the candidates based on the user input."""
        self.lookuptable.clear()

        # Add some dummy candidates for now...
        if self.preedit:
            for c in self.cangjie.getCharacters(self.preedit):
                self.lookuptable.append_candidate(IBus.Text.new_from_string(c))

    def update_lookup_table(self):
        """Update the lookup table."""
        if not self.preedit:
            self.lookuptable.clear()

        num_candidates = self.lookuptable.get_number_of_candidates()
        super(Engine, self).update_lookup_table(self.lookuptable,
                                                num_candidates>0)

    def commit_text(self, text):
        """Commit the `text` and prepare for future input."""
        super(Engine, self).commit_text(text)
        self.update_preedit_text(u"")
        self.update_lookup_table()
        self.update_auxiliary_text()

    def play_error_bell(self):
        """Play an error sound, to notify the user of invalid input."""
        if not hasattr(self, "canberra"):
            self.canberra = pycanberra.Canberra()

        self.canberra.play(1, pycanberra.CA_PROP_EVENT_ID, "dialog-error",
                           pycanberra.CA_PROP_MEDIA_ROLE, "error", None)


class EngineCangjie(Engine):
    """The Cangjie engine."""
    __gtype_name__ = "EngineCangjie"
    config_name = "cangjie"

    def do_process_inputchar(self, keyval):
        """Handle user input of valid Cangjie input characters."""
        self.update_preedit_text(self.preedit+IBus.keyval_to_unicode(keyval))
        self.update_auxiliary_text()
        return True

    def do_space(self):
        """Handle the space key.

        For Cangjie, that's the key which will do everything.
        """
        if not self.preedit:
            return False

        self.get_candidates()
        num_candidates = self.lookuptable.get_number_of_candidates()

        if num_candidates == 0:
            self.play_error_bell()

        elif num_candidates == 1:
            self.do_select_candidate(1)

        else:
            # More than one candidate, display them
            self.update_lookup_table()

        return True

    def update_auxiliary_text(self):
        """Update the auxiliary text.

        Somewhat counter-intuitively, this should contain the pre-edit text for
        Cangjie.
        """
        text = IBus.Text.new_from_string(self.preedit)
        super(EngineCangjie, self).update_auxiliary_text(text, len(self.preedit)>0)

class EngineQuick(Engine):
    """The Quick engine."""
    __gtype_name__ = "EngineQuick"
    config_name = "quick"
