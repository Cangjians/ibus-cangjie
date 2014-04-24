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


__all__ = ["EngineCangjie", "EngineQuick"]


import gettext
from operator import attrgetter

from gi.repository import Gio
from gi.repository import IBus

import cangjie

from .canberra import Canberra


# FIXME: Find a way to de-hardcode the gettext package
_ = lambda x: gettext.dgettext("ibus-cangjie", x)


def is_inputnumber(keyval):
    """Is the `keyval` param a numeric input, e.g to select a candidate."""
    return ((keyval in range(getattr(IBus, "0"), getattr(IBus, "9")+1)) or
            (keyval in range(IBus.KP_0, IBus.KP_9+1)))


class Engine(IBus.Engine):
    """The base class for Cangjie and Quick engines."""
    def __init__(self):
        super(Engine, self).__init__()

        self.canberra = Canberra()

        self.settings = Gio.Settings("org.cangjians.ibus.%s" % self.__name__)
        self.settings.connect("changed", self.on_value_changed)

        self.current_input = ""
        self.current_radicals = ""
        self.clear_on_next_input = False

        self.lookuptable = IBus.LookupTable()
        self.lookuptable.set_page_size(9)
        self.lookuptable.set_round(True)
        self.lookuptable.set_orientation(IBus.Orientation.VERTICAL)

        self.init_properties()
        self.init_cangjie()

    def init_properties(self):
        self.prop_list = IBus.PropList()

        for (key, label) in (("halfwidth-chars", _("Half-Width Characters")),
                             ):
            stored_value = self.settings.get_boolean(key)
            state = IBus.PropState.CHECKED if stored_value else IBus.PropState.UNCHECKED

            try:
                # Try the new constructor from IBus >= 1.5
                prop = IBus.Property(key=key,
                                     prop_type=IBus.PropType.TOGGLE,
                                     label=label,
                                     icon='',
                                     sensitive=True,
                                     visible=True,
                                     state=state,
                                     sub_props=None)

            except TypeError:
                # IBus 1.4.x didn't have the GI overrides for the nice
                # constructor, so let's do it the old, non-pythonic way.
                #   IBus.Property.new(key, type, label, icon, tooltip,
                #                     sensitive, visible, state, sub_props)
                prop = IBus.Property.new(key, IBus.PropType.TOGGLE,
                                         IBus.Text.new_from_string(label),
                                         '', IBus.Text.new_from_string(''),
                                         True, True, state, None)

            self.prop_list.append(prop)

    def do_property_activate(self, prop_name, state):
        active = state == IBus.PropState.CHECKED
        self.settings.set_boolean(prop_name, active)

    def do_focus_in(self):
        self.register_properties(self.prop_list)

    def init_cangjie(self):
        version = self.settings.get_int("version")
        version = getattr(cangjie.versions, "CANGJIE%d"%version)

        filters = (cangjie.filters.BIG5 | cangjie.filters.HKSCS
                                        | cangjie.filters.PUNCTUATION)

        if self.settings.get_boolean("include-allzh"):
            filters |= cangjie.filters.CHINESE
        if self.settings.get_boolean("include-jp"):
            filters |= cangjie.filters.KANJI
            filters |= cangjie.filters.HIRAGANA
            filters |= cangjie.filters.KATAKANA
        if self.settings.get_boolean("include-zhuyin"):
            filters |= cangjie.filters.ZHUYIN
        if self.settings.get_boolean("include-symbols"):
            filters |= cangjie.filters.SYMBOLS

        self.cangjie = cangjie.Cangjie(version, filters)

    def on_value_changed(self, settings, key):
        # Only recreate the Cangjie object if necessary
        if key not in ("halfwidth-chars", ):
            self.init_cangjie()

    def do_focus_out(self):
        """Handle focus out event

        This happens, for example, when switching between application windows
        or input contexts.

        Such events should clear the current input.
        """
        self.clear_current_input()

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

    def do_space(self):
        """Handle the space key.

        This is our "power key". It implements most of the behaviour behind
        Cangjie and Quick.

        It can be used to fetch the candidates if there are none, scroll to
        the next page of candidates if appropriate or just commit the first
        candidate when we have only one page.

        Of course, it can also be used to input a "space" character.
        """
        if not self.current_input:
            return self.do_fullwidth_char(" ")

        if not self.lookuptable.get_number_of_candidates():
            try:
                self.get_candidates()

            except (cangjie.errors.CangjieNoCharsError,
                    cangjie.errors.CangjieInvalidInputError):
                self.play_error_bell()
                self.clear_on_next_input = True

            return True

        if self.lookuptable.get_number_of_candidates() <= 9:
            self.do_select_candidate(1)
            return True

        self.do_page_down()
        return True

    def do_number(self, keyval):
        """Handle numeric input."""
        if self.lookuptable.get_number_of_candidates():
            return self.do_select_candidate(int(IBus.keyval_to_unicode(keyval)))

        return self.do_fullwidth_char(IBus.keyval_to_unicode(keyval))

    def do_other_key(self, keyval):
        """Handle all otherwise unhandled key presses."""
        c = IBus.keyval_to_unicode(keyval)
        if not c or c == '\n' or c == '\r':
            return False

        if not self.lookuptable.get_number_of_candidates() and \
               self.current_input:
            # FIXME: This is really ugly
            if len(self.current_input) == 1 and \
               not self.cangjie.is_input_key(self.current_input):
                self.get_candidates(by_shortcode=True)

            else:
                self.get_candidates()

        if self.lookuptable.get_number_of_candidates():
            self.do_select_candidate(1)

        return self.do_fullwidth_char(IBus.keyval_to_unicode(keyval))

    def do_fullwidth_char(self, inputchar):
        """Commit the full-width version of an input character."""
        if self.settings.get_boolean("halfwidth-chars"):
            return False

        self.update_current_input(append=inputchar)

        try:
            self.get_candidates(code=inputchar, by_shortcode=True)

        except cangjie.errors.CangjieNoCharsError:
            self.clear_current_input()
            return False

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
        self.clear_current_input()
        return True

    def do_process_key_event(self, keyval, keycode, state):
        """Handle `process-key-event` events.

        This event is fired when the user presses a key.
        """
        # Ignore key release events
        if (state & IBus.ModifierType.RELEASE_MASK):
            return False

        # Work around integer overflow bug on 32 bits systems:
        #     https://bugzilla.gnome.org/show_bug.cgi?id=693121
        # The bug is fixed in pygobject 3.7.91, but many distributions will
        # ship the previous version for some time. (e.g Fedora 18)
        if (state & 1073741824):
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

        if c and c == "*":
            return self.do_star()

        if c and self.cangjie.is_input_key(c):
            return self.do_inputchar(c)

        return self.do_other_key(keyval)

    def clear_current_input(self):
        """Clear the current input."""
        self.current_input = ""
        self.current_radicals = ""

        self.clear_on_next_input = False

        self.update_lookup_table()
        self.update_auxiliary_text()

    def update_current_input(self, append=None, drop=None):
        """Update the current input."""
        if append is not None:
            if self.clear_on_next_input:
                self.clear_current_input()

            if len(self.current_input) < self.input_max_len:
                self.current_input += append

                try:
                    self.current_radicals += self.cangjie.get_radical(append)

                except cangjie.errors.CangjieInvalidInputError:
                    # That character doesn't have a radical
                    self.current_radicals += append

            else:
                self.play_error_bell()

        elif drop is not None:
            self.clear_on_next_input = False

            self.current_input = self.current_input[:-drop]
            self.current_radicals = self.current_radicals[:-drop]

        else:
            raise ValueError("You must specify either 'append' or 'drop'")

        self.update_auxiliary_text()

    def get_candidates(self, code=None, by_shortcode=False):
        """Get the candidates based on the user input.

        If the optional `code` parameter is not specified, then use the
        current input instead.
        """
        self.lookuptable.clear()
        num_candidates = 0

        if not code:
            code = self.current_input

        if not by_shortcode:
            chars = self.cangjie.get_characters(code)

        else:
            chars = self.cangjie.get_characters_by_shortcode(code)

        for c in sorted(chars, key=attrgetter("frequency"), reverse=True):
            self.lookuptable.append_candidate(IBus.Text.new_from_string(c.chchar))
            num_candidates += 1

        if num_candidates == 1:
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

    def play_error_bell(self):
        """Play an error sound, to notify the user of invalid input."""
        self.canberra.play_error()


class EngineCangjie(Engine):
    """The Cangjie engine."""
    __gtype_name__ = "EngineCangjie"
    __name__ = "cangjie"
    input_max_len = 5

    def do_inputchar(self, inputchar):
        """Handle user input of valid Cangjie input characters."""
        if self.lookuptable.get_number_of_candidates():
            self.do_select_candidate(1)

        self.update_current_input(append=inputchar)

        return True

    def do_star(self):
        """Handle the star key (*)

        For Cangjie, this can in some cases be a wildcard key.
        """
        if self.current_input:
            return self.do_inputchar("*")

        return self.do_other_key(IBus.asterisk)


class EngineQuick(Engine):
    """The Quick engine."""
    __gtype_name__ = "EngineQuick"
    __name__ = "quick"
    input_max_len = 2

    def do_inputchar(self, inputchar):
        """Handle user input of valid Cangjie input characters."""
        if self.lookuptable.get_number_of_candidates():
            self.do_select_candidate(1)

        if len(self.current_input) < self.input_max_len:
            self.update_current_input(append=inputchar)

        # Now that we appended/committed, let's check the new length
        if len(self.current_input) == self.input_max_len:
            current_input = "*".join(self.current_input)
            try:
                self.get_candidates(current_input)

            except cangjie.errors.CangjieNoCharsError:
                self.play_error_bell()
                self.clear_on_next_input = True

        return True

    def do_star(self):
        """Handle the star key (*)

        For Quick, this should just be considered as any other key.
        """
        return self.do_other_key(IBus.asterisk)
