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

try:
    import pycanberra
except ImportError:
    # Fall back on the bundled version, until upstream ports to Python 3:
    # https://github.com/psykoyiko/pycanberra/pull/2
    import ibus_cangjie.pycanberra as pycanberra

import cangjie

from .config import Config


def is_inputnumber(keyval):
    """Is the `keyval` param a numeric input, e.g to select a candidate."""
    return keyval in range(getattr(IBus, "0"), getattr(IBus, "9")+1)


class Engine(IBus.Engine):
    """The base class for Cangjie and Quick engines."""
    def __init__(self):
        super(Engine, self).__init__()

        self.config = Config(IBus.Bus(), self.config_name,
                             self.on_value_changed)

        self.current_input = ""
        self.current_radicals = ""

        self.lookuptable = IBus.LookupTable()
        self.lookuptable.set_page_size(9)
        self.lookuptable.set_round(True)
        self.lookuptable.set_orientation(IBus.Orientation.VERTICAL)

        self.init_cangjie()

    def init_cangjie(self):
        new_version = self.config.read("use_new_version")
        version = getattr(cangjie.versions,
                          "CANGJIE%d" % (5 if new_version else 3))

        all_zh = self.config.read("include_all_zh")
        lang = getattr(cangjie.languages,
                       "COMMON" if all_zh else "TRADITIONAL")

        self.cangjie = cangjie.CangJie(version, lang)

    def on_value_changed(self, config, section, name, value, data):
        if section != self.config.config_section:
            return

        self.init_cangjie()

    def do_cancel_input(self):
        """Cancel the current input.

        However, if there isn't any current input, then we shouldn't try to do
        anything at all, so that the key can fulfill its original function.
        """
        if not self.current_input:
            return False

        self.clear_current_input()
        return True

    def do_page_down(self):
        """Present the next page of candidates.

        However, if there isn't any current input, then we shouldn't try to do
        anything at all, so that the key can fulfill its original function.
        """
        if not self.lookuptable.get_number_of_candidates():
            return False

        self.lookuptable.page_down()
        self.update_lookup_table()
        self.update_auxiliary_text()
        return True

    def do_page_up(self):
        """Present the previous page of candidates.

        However, if there isn't any current input, then we shouldn't try to do
        anything at all, so that the key can fulfill its original function.
        """
        if not self.lookuptable.get_number_of_candidates():
            return False

        self.lookuptable.page_up()
        self.update_lookup_table()
        self.update_auxiliary_text()
        return True

    def do_backspace(self):
        """Go back from one input character.

        This doesn't cancel the current input, only removes the last
        user-inputted character from the current input, and clear the list of
        candidates.

        However, if there isn't any pre-edit, then we shouldn't handle the
        backspace key at all, so that it can fulfill its original function:
        deleting characters backwards.
        """
        if not self.current_input:
            return False

        self.update_current_input(drop=1)

        self.lookuptable.clear()
        self.update_lookup_table()
        return True

    def do_number(self, keyval):
        """Handle numeric input."""
        if self.lookuptable.get_number_of_candidates():
            return self.do_select_candidate(int(IBus.keyval_to_unicode(keyval)))

        return self.do_fullwidth_char(IBus.keyval_to_unicode(keyval))

    def do_other_key(self, keyval):
        """Handle all otherwise unhandled key presses."""
        c = IBus.keyval_to_unicode(keyval)
        if c:
            return self.do_fullwidth_char(IBus.keyval_to_unicode(keyval))

        return False

    def do_fullwidth_char(self, inputchar):
        """Commit the full-width version of an input character."""
        if self.config.read("halfwidth_chars"):
            return False

        try:
            t = self.cangjie.getFullWidthChar(inputchar)
        except Exception as e:
            return False

        self.commit_text(IBus.Text.new_from_string(t))
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

        if state & (IBus.ModifierType.CONTROL_MASK |
                    IBus.ModifierType.MOD1_MASK):
            # Ignore Alt+<key> and Ctrl+<key>
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

        if is_inputnumber(keyval):
            return self.do_number(keyval)

        c = IBus.keyval_to_unicode(keyval)
        # TODO: should wildcard support be optional?
        if c and self.cangjie.isCangJieInputKey(c) or c == "*":
            return self.do_inputchar(c)

        return self.do_other_key(keyval)

    def clear_current_input(self):
        """Clear the current input."""
        self.current_input = ""
        self.current_radicals = ""

        self.update_lookup_table()
        self.update_auxiliary_text()

    def update_current_input(self, append=None, drop=None):
        """Update the current input."""
        if append is not None:
            self.current_input += append
            self.current_radicals += self.cangjie.translateInputKeyToCangJie(append)

        elif drop is not None:
            self.current_input = self.current_input[:-drop]
            self.current_radicals = self.current_radicals[:-drop]

        else:
            raise ValueError("You must specify either 'append' or 'drop'")

        self.update_auxiliary_text()

    def get_candidates(self, code=None):
        """Get the candidates based on the user input.

        If the optional `code` parameter is not specified, then use the
        current input instead.
        """
        self.lookuptable.clear()
        num_candidates = 0

        if not code:
            code = self.current_input

        if code:
            for c in self.cangjie.getCharacters(code):
                self.lookuptable.append_candidate(IBus.Text.new_from_string(c))
                num_candidates += 1

        if num_candidates == 0:
            self.play_error_bell()

        elif num_candidates == 1:
            self.do_select_candidate(1)

        else:
            # More than one candidate, display them
            self.update_lookup_table()

    def update_preedit_text(self):
        """Update the preedit text.

        This is never used with Cangjie and Quick, so let's nullify it
        completely, in case something else in the IBus machinery calls it.
        """
        pass

    def update_auxiliary_text(self):
        """Update the auxiliary text.

        This should contain the radicals for the current input.
        """
        text = IBus.Text.new_from_string(self.current_radicals)
        super(Engine, self).update_auxiliary_text(text, len(self.current_radicals)>0)

    def update_lookup_table(self):
        """Update the lookup table."""
        if not self.current_input:
            self.lookuptable.clear()

        num_candidates = self.lookuptable.get_number_of_candidates()
        super(Engine, self).update_lookup_table(self.lookuptable,
                                                num_candidates>0)

    def commit_text(self, text):
        """Commit the `text` and prepare for future input."""
        super(Engine, self).commit_text(text)
        self.clear_current_input()

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
    input_max_len = 5

    def do_inputchar(self, inputchar):
        """Handle user input of valid Cangjie input characters."""
        if self.lookuptable.get_number_of_candidates():
            self.do_select_candidate(1)

        if len(self.current_input) < self.input_max_len:
            self.update_current_input(append=inputchar)

        else:
            self.play_error_bell()

        return True

    def do_space(self):
        """Handle the space key.

        For Cangjie, that's the key which will do everything.
        """
        if not self.current_input:
            return self.do_fullwidth_char(" ")

        if self.lookuptable.get_number_of_candidates():
            self.do_select_candidate(1)

        else:
            self.get_candidates()

        return True


class EngineQuick(Engine):
    """The Quick engine."""
    __gtype_name__ = "EngineQuick"
    config_name = "quick"
    input_max_len = 2

    def do_inputchar(self, inputchar):
        """Handle user input of valid Cangjie input characters."""
        if len(self.current_input) < self.input_max_len:
            self.update_current_input(append=inputchar)

        else:
            self.do_select_candidate(1)

        # Now that we appended/committed, let's check the new length
        if len(self.current_input) == self.input_max_len:
            current_input = "*".join(self.current_input)
            self.get_candidates(current_input)

        return True

    def do_space(self):
        """Handle the space key.

        For Quick, this is either a page-down on the candidates table.
        """
        if self.do_page_down():
            return True

        return self.do_fullwidth_char(" ")
