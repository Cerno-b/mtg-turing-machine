import unittest

import mtg_turing_machine.classes.instances as examples

from mtg_turing_machine.classes.universal_turing_machine import UniversalTuringMachine
from mtg_turing_machine.classes.two_tag_system import TwoTagSystem


def run_utm_from_two_tag(two_tag, string):
    two_tag.set_input_string(string, "#")
    utm = UniversalTuringMachine()
    utm.set_tape_string_from_2tag(two_tag)
    utm.run(brief=True)
    return utm.get_tape_as_2tag()


def run_utm_from_tm(tm, string):
    tm.convert_to_two_symbol()
    tm.set_tape_string(string)

    two_tag = TwoTagSystem(tm)

    utm = UniversalTuringMachine()
    utm.set_tape_string_from_2tag(two_tag)
    utm.run(brief=True)

    two_tag_state = utm.get_tape_as_2tag()
    two_tag.set_input_string(two_tag_state, two_tag.halt_symbol)
    tape = two_tag.get_tm_tape()

    if tm.is_binarized_tm:
        tm.set_tape_string(tape)
        tape = tm.get_stripped_tape(decode_binarized=True)
    tape = list(tape)

    return [t for t in tape if t != "^"]


class TestUniversalTuringMachine(unittest.TestCase):
    def test_divide_by_two(self):
        two_tag = examples.load_two_tag_divide_by_2()
        tape = run_utm_from_two_tag(two_tag, "XXXXXXXX#")
        self.assertEqual(tape, ["#", "X", "X", "X", "X"])

        two_tag = examples.load_two_tag_divide_by_2()
        state = run_utm_from_two_tag(two_tag, "X:X:X:X:#")
        self.assertEqual(state, ["#", "X", "X", "X", "X"])

        two_tag = examples.load_two_tag_divide_by_2()
        state = run_utm_from_two_tag(two_tag, "XX::XX::#")
        self.assertEqual(state, ["#", "X", "i", "X", "i"])

    # this runs for a long time (forever?) maybe the utm cannot handle a 2-tag system without stopping symbol
    # that would normally stop when it runs out of readable letters
    #def test_collatz(self):
    #    two_tag = definitions.load_two_tag_collatz()
    #    state = run_utm_from_two_tag(two_tag, "aaa")
    #    self.assertEqual(state, ["a"])

    def test_from_tm(self):
        tm = examples.load_tm_write_one()
        result = run_utm_from_tm(tm, "")
        self.assertEqual(result, ["1"])

        tm = examples.load_tm_add_one()
        result = run_utm_from_tm(tm, "11")
        self.assertEqual(result, ["1", "1", "1"])

        tm = examples.load_tm_write_one_two()
        result = run_utm_from_tm(tm, "")
        self.assertEqual(result, ["1", "2"])

#        tm = definitions.load_tm_make_palindrome()
#        result = run_utm_from_tm(tm, "10")
#        self.assertEqual(result, ["1", "0", "0", "1"])


if __name__ == '__main__':
    unittest.main()
