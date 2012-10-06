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

import gobject
import pango
import ibus
from ibus import keysyms
from ibus import modifier

class Engine(ibus.EngineBase):
    def __init__(self, bus, object_path):
        super(Engine, self).__init__(bus, object_path)
        # TODO: Implement the specific stuff

    def process_key_event(self, keyval, keycode, state):
        # TODO: Implement that stuff
        pass

    def __invalidate(self):
        if self.__is_invalidate:
            return
        self.__is_invalidate = True
        gobject.idle_add(self.__update, priority = gobject.PRIORITY_LOW)

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

    def cursor_up(self):
        if self.__lookup_table.cursor_up():
            self.cursor_up_lookup_table()
            return True
        return False

    def cursor_down(self):
        if self.__lookup_table.cursor_down():
            self.cursor_down_lookup_table()
            return True
        return False

    def __commit_string(self, text):
        self.commit_text(ibus.Text(text))
        self.__preedit_string = u""
        self.__update()

    def __update(self):
        preedit_len = len(self.__preedit_string)
        attrs = ibus.AttrList()
        self.__lookup_table.clean()
        if preedit_len > 0:
            if not self.__dict.check(self.__preedit_string):
                attrs.append(ibus.AttributeForeground(0xff0000, 0, preedit_len))
                for text in self.__dict.suggest(self.__preedit_string):
                    self.__lookup_table.append_candidate(ibus.Text(text))
        self.update_auxiliary_text(ibus.Text(self.__preedit_string, attrs), preedit_len > 0)
        attrs.append(ibus.AttributeUnderline(pango.UNDERLINE_SINGLE, 0, preedit_len))
        self.update_preedit_text(ibus.Text(self.__preedit_string, attrs), preedit_len, preedit_len > 0)
        self.__update_lookup_table()
        self.__is_invalidate = False

    def __update_lookup_table(self):
        visible = self.__lookup_table.get_number_of_candidates() > 0
        self.update_lookup_table(self.__lookup_table, visible)

    def focus_in(self):
        self.register_properties(self.__prop_list)

    def focus_out(self):
        pass

    def reset(self):
        pass

    def property_activate(self, prop_name):
        print "PropertyActivate(%s)" % prop_name
