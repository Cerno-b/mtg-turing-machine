import unittest

import mtg_turing_machine.classes.instances as examples

from mtg_turing_machine.classes.mtg_turing_machine import MagicTheGatheringTuringMachine
from mtg_turing_machine.classes.universal_turing_machine import UniversalTuringMachine
from mtg_turing_machine.classes.two_tag_system import TwoTagSystem


_RUN_LONG_TESTS = False


def run_mtg_utm_from_two_tag(two_tag, string):
    two_tag.set_initial_word(string, "#")
    utm = UniversalTuringMachine()
    utm.set_tape_string_from_two_tag(two_tag)

    mtg_utm = MagicTheGatheringTuringMachine(utm)
    mtg_utm.run()
    utm = mtg_utm.get_utm()

    return utm.decode_tape_as_two_tag_word()


class TestMagicTuringMachine(unittest.TestCase):
    def test_divide_by_two(self):
        two_tag = examples.load_two_tag_cut_in_half()
        tape = run_mtg_utm_from_two_tag(two_tag, "XXXXXXXX#")
        self.assertEqual(tape, ["#", "X", "X", "X", "X"])

        two_tag = examples.load_two_tag_cut_in_half()
        state = run_mtg_utm_from_two_tag(two_tag, "X:X:X:X:#")
        self.assertEqual(state, ["#", "X", "X", "X", "X"])

        two_tag = examples.load_two_tag_cut_in_half()
        state = run_mtg_utm_from_two_tag(two_tag, "XX::XX::#")
        self.assertEqual(state, ["#", "X", "i", "X", "i"])


if __name__ == '__main__':
    unittest.main()
