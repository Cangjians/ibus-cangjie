import unittest

from gi.repository import IBus

from ibus_cangjie.engine import *


class CangjieTestCase(unittest.TestCase):
    def setUp(self):
        self.engine = EngineCangjie()

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

    def test_max_input(self):
        # Get to max char
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.engine.do_process_key_event(IBus.a, 0, 0)

        # Try adding one more and get the error bell
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.assertEqual(len(self.engine._mock_auxiliary_text), 5)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
        self.assertEqual(len(self.engine.canberra._mock_played_events), 1)

        # And once more
        self.engine.do_process_key_event(IBus.a, 0, 0)
        self.assertEqual(len(self.engine._mock_auxiliary_text), 5)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
        self.assertEqual(len(self.engine.canberra._mock_played_events), 2)

    def test_inexistent_combination(self):
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 5)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
        self.assertEqual(len(self.engine.canberra._mock_played_events), 1)

    def test_wildcard(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.asterisk, 0, 0)
        self.engine.do_process_key_event(IBus.d, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 3)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 3)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertTrue(self.engine.lookuptable.get_number_of_candidates() > 1)

    def test_wildcard_first(self):
        self.engine.do_process_key_event(IBus.asterisk, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 1)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_wildcard_last(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.asterisk, 0, 0)

        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 2)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
        self.assertEqual(len(self.engine.canberra._mock_played_events), 1)

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

    def test_backspace_on_multiple_keys_and_candidates(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.asterisk, 0, 0)
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.engine.do_process_key_event(IBus.BackSpace, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 2)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_escape(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.d, 0, 0)

        self.engine.do_process_key_event(IBus.Escape, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_escape_on_candidates(self):
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.asterisk, 0, 0)
        self.engine.do_process_key_event(IBus.d, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)

        self.engine.do_process_key_event(IBus.Escape, 0, 0)

        self.assertEqual(len(self.engine._mock_auxiliary_text), 0)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)

    def test_autoclear_on_error(self):
        # First make an error on purpose
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.engine.do_process_key_event(IBus.space, 0, 0)
        self.assertEqual(len(self.engine._mock_auxiliary_text), 2)
        self.assertEqual(len(self.engine.canberra._mock_played_events), 1)

        # Now go on inputting
        self.engine.do_process_key_event(IBus.z, 0, 0)
        self.assertEqual(len(self.engine._mock_auxiliary_text), 1)
        self.assertEqual(len(self.engine._mock_committed_text), 0)
        self.assertEqual(self.engine.lookuptable.get_number_of_candidates(), 0)
