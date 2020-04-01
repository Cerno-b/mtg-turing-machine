import unittest

import mtg_turing_machine.classes.instances as examples

from mtg_turing_machine.classes.mtg_turing_machine import MagicTheGatheringTuringMachine
from mtg_turing_machine.classes.universal_turing_machine import UniversalTuringMachine


_RUN_LONG_TESTS = False


def run_mtg_utm_from_two_tag(two_tag, string, verbose=True):
    two_tag.set_initial_word(string, "#")
    utm = UniversalTuringMachine()
    utm.set_tape_string_from_two_tag(two_tag)

    mtg_utm = MagicTheGatheringTuringMachine(utm)
    mtg_utm.print()
    # mtg_utm.run(verbose)
    utm = mtg_utm.get_utm()

    return utm.decode_tape_as_two_tag_word()


class TestMagicTuringMachine(unittest.TestCase):
    def test_basic(self):
        utm = examples.load_dummy_utm()
        mtg_tm = MagicTheGatheringTuringMachine(utm)

        mtg_tm.run()
        tape = mtg_tm.decode_tape()
        self.assertEqual(tape, ["11<", "1<", "^", "-", "b", "c2", "11>", "c2"])

    def test_divide_by_two(self):
        two_tag = examples.load_two_tag_cut_in_half()
        tape = run_mtg_utm_from_two_tag(two_tag, "XXXXXXXX#", verbose=False)
        self.assertEqual(tape, ["#", "X", "X", "X", "X"])

        two_tag = examples.load_two_tag_cut_in_half()
        state = run_mtg_utm_from_two_tag(two_tag, "X:X:X:X:#", verbose=False)
        self.assertEqual(state, ["#", "X", "X", "X", "X"])

        two_tag = examples.load_two_tag_cut_in_half()
        state = run_mtg_utm_from_two_tag(two_tag, "XX::XX::#", verbose=False)
        self.assertEqual(state, ["#", "X", "i", "X", "i"])

    if _RUN_LONG_TESTS:
        def test_collatz(self):
            two_tag = examples.load_two_tag_collatz()
            state = run_mtg_utm_from_two_tag(two_tag, "aaa", verbose=False)
            self.assertEqual(state, ["a"])

        def test_manually_converted_from_simple_tm(self):
            two_tag = examples.load_two_tag_manually_converted_from_simple_tm()
            state = run_mtg_utm_from_two_tag(two_tag, ["A_q_init_0", "x", 'B_q_init_0', "x"], verbose=False)
            self.assertEqual(state, ["#", "x", 'a_#', 'x', 'B_#', "x"])


if __name__ == '__main__':
    unittest.main()
