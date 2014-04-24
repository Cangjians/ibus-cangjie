# Copyright (c) 2013 - The IBus Cangjie authors
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


import os
import unittest

from gi.repository import IBus

from ibus_cangjie.engine import *


class QuickTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = EngineQuick()

    def tearDown(self):
        del self.engine

    def test_single_key(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)

    def test_single_key_space_single_char(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 1)

    def test_single_key_space_two_candidates(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 2)

    def test_two_candidates_space(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)

        # Keep track of the first candidate, check later if it was committed
        expected = self.engine.lookuptable.get_candidate(0).text

        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
        self.assertEqual(self.engine._mock_committed_text, expected)

    def test_two_candidates_continue_input(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)

        # Keep track of the first candidate, check later if it was committed
        expected = self.engine.lookuptable.get_candidate(0).text

        self.engine.do_process_key_event(IBus.a, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
        self.assertEqual(self.engine._mock_committed_text, expected)

    def test_auto_candidates(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.a, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 2)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertTrue(self.engine.lookuptable.get_number_of_candidates() > 1)

    def test_inexistent_combination(self):
        self.engine.do_process_key_event(IBus.x, 0, 0)
        self.engine.do_process_key_event(IBus.z, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 2)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
        self.assertEqual(len(self.engine.canberra._mock_played_events), 1)

    def test_nowildcard(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.asterisk, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 2)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

        self.engine.do_process_key_event(IBus.d, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 2)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_nowildcard_first(self):
        self.engine.do_process_key_event(IBus.asterisk, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_backspace(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.BackSpace, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_backspace_on_multiple_keys(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.BackSpace, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_backspace_on_candidates(self):
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)
        self.engine.do_process_key_event(IBus.BackSpace, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_escape(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.d, 0, 0)

        self.engine.do_process_key_event(IBus.Escape, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_symbol(self):
        self.engine.do_process_key_event(IBus.at, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_multiple_punctuation(self):
        self.engine.do_process_key_event(IBus.comma, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertTrue(self.engine.lookuptable.get_number_of_candidates() > 1)

    def test_char_then_multiple_punctuation(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.comma, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertTrue(self.engine.lookuptable.get_number_of_candidates() > 1)

    def test_punctuation_then_punctuation(self):
        self.engine.do_process_key_event(IBus.comma, 0, 0)
        self.engine.do_process_key_event(IBus.comma, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertTrue(self.engine.lookuptable.get_number_of_candidates() > 1)

    def test_commit_with_numpad(self):
        self.engine.do_process_key_event(IBus.h, 0, 0)
        self.engine.do_process_key_event(IBus.i, 0, 0)
        self.engine.do_process_key_event(getattr(IBus, "7"), 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

        # Reset the committed text, but keep the value first
        expected = self.engine._mock_committed_text[:]
        self.engine._mock_committed_text = ''

        self.engine.do_process_key_event(IBus.h, 0, 0)
        self.engine.do_process_key_event(IBus.i, 0, 0)
        self.engine.do_process_key_event(IBus.KP_7, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

        # Now check that the same character was committed
        self.assertEqual(expected, self.engine._mock_committed_text)
