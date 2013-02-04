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
