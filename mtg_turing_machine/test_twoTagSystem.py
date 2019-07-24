import unittest

import definitions

from two_tag_system import TwoTagSystem


def run_two_tag(two_tag, string):
    two_tag.set_input_string(string, "#")
    two_tag.run()
    return two_tag.state


def run_two_tag_from_tm(tm, tape):
    tm.set_tape_string(tape)
    tm.convert_to_two_symbol()
    two_tag = TwoTagSystem(tm)
    two_tag.run(brief=True)
    tape = two_tag.get_tm_tape()
    if tm.is_binarized_tm:
        tm.set_tape_string(tape)
        tape = tm.get_stripped_tape(decode_binarized=True)
    tape = list(tape)
    return [t for t in tape if t != "^"]


class TestTwoTagSystem(unittest.TestCase):
    def test_divide_by_two(self):
        two_tag = definitions.load_two_tag_divide_by_2()
        state = run_two_tag(two_tag, "XXXXXXXX#")
        self.assertEqual(state, ["#", "X", "X", "X", "X"])

        two_tag = definitions.load_two_tag_divide_by_2()
        state = run_two_tag(two_tag, "X:X:X:X:#")
        self.assertEqual(state, ["#", "X", "X", "X", "X"])

        two_tag = definitions.load_two_tag_divide_by_2()
        state = run_two_tag(two_tag, "XX::XX::#")
        self.assertEqual(state, ["#", "X", "i", "X", "i"])

    def test_collatz(self):
        two_tag = definitions.load_two_tag_collatz()
        state = run_two_tag(two_tag, "aaa")
        self.assertEqual(state, ["a"])

    def test_manually_converted_from_simple_tm(self):
        two_tag = definitions.load_two_tag_manually_converted_from_simple_tm()
        state = run_two_tag(two_tag, ["A_q_init_0", "x", 'B_q_init_0', "x"])
        self.assertEqual(state, ["#", "x", 'a_#', 'x', 'B_#', "x"])

    def test_from_tm(self):
        tm = definitions.load_tm_write_one()
        result = run_two_tag_from_tm(tm, "")
        self.assertEqual(result, ["1"])

        tm = definitions.load_tm_add_one()
        result = run_two_tag_from_tm(tm, "11")
        self.assertEqual(result, ["1", "1", "1"])

        tm = definitions.load_tm_write_one_two()
        result = run_two_tag_from_tm(tm, "")
        self.assertEqual(result, ["1", "2"])

        tm = definitions.load_tm_make_palindrome()
        #result = run_two_tag_from_tm(tm, "10")
        #self.assertEqual(result, ["1", "0", "0", "1"])

        # tm = definitions.load_tm_dec_to_bin()
        # result = run_two_tag_from_tm(tm, "9")
        # self.assertEqual(result, ["1", "0", "0", "1"])


if __name__ == '__main__':
    unittest.main()
