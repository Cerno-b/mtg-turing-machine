import unittest

import mtg_turing_machine.classes.instances as examples


def run_tm(tm, tape=None, convert_to_two_symbol=False):
    if tape:
        tm.set_tape_string(tape)
    if convert_to_two_symbol:
        tm.convert_to_two_symbol()
    tm.run()
    return tm.get_stripped_tape(decode_binarized=tm.is_binarized_tm)


class TestTuringMachine(unittest.TestCase):

    #def test_test2(self, convert_to_two_symbol=False):
    #    tm = examples.load_tm2_test()
    #    result = run_tm(tm, convert_to_two_symbol=convert_to_two_symbol)
    #    self.assertEqual(["1", "1", "1", "1", "1", "x"], result)
    #
    def test_run_add_unary(self, convert_to_two_symbol=False):
        tm = examples.load_tm_add_unary()
        result = run_tm(tm, tape="111x11", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1", "1", "x"], result)

    def test_run_add_unary_2_symbol(self, convert_to_two_symbol=False):
        tm = examples.load_tm_add_unary_two_symbol()
        result = run_tm(tm, tape="111011", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1", "1"], result)

    def test_run_write_one(self, convert_to_two_symbol=False):
        tm = examples.load_tm_write_one()
        result = run_tm(tm, tape="", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1"], result)

        tm = examples.load_tm_write_one()
        result = run_tm(tm, tape="111^", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1"], result)

        tm = examples.load_tm_write_one()
        result = run_tm(tm, tape="011", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1"], result)

    def test_run_write_one_two(self, convert_to_two_symbol=False):
        tm = examples.load_tm_write_one_two()
        result = run_tm(tm, tape="", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "2"], result)

    def test_run_add_one(self, convert_to_two_symbol=False):
        tm = examples.load_tm_add_one()
        result = run_tm(tm, tape="", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1"], result)

        tm = examples.load_tm_add_one()
        result = run_tm(tm, tape="1^11", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1"], result)

    def test_run_palindrome(self, convert_to_two_symbol=False):
        tm = examples.load_tm_make_palindrome()
        result = run_tm(tm, tape="100", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "0", "0", "0", "0", "1"], result)

        tm = examples.load_tm_make_palindrome()
        result = run_tm(tm, tape="10", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "0", "0", "1"], result)

    def test_run_dec_to_bin(self, convert_to_two_symbol=False):
        tm = examples.load_tm_dec_to_bin()
        result = run_tm(tm, tape="9", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(["1", "0", "0", "1"], result)

    def test_run_add_unary_as_2_symbol(self):
        self.test_run_add_unary(convert_to_two_symbol=True)

    def test_run_write_one_as_2_symbol(self):
        self.test_run_write_one(convert_to_two_symbol=True)

    def test_run_write_one_two_as_2_sybol(self):
        self.test_run_write_one_two(convert_to_two_symbol=True)

    def test_run_add_one_as_2_symbol(self):
        self.test_run_add_one(convert_to_two_symbol=True)

    def test_run_palindrome_as_2_symbol(self):
        self.test_run_palindrome(convert_to_two_symbol=True)

    def test_run_dec_to_bin_as_2_symbol(self):
        self.test_run_dec_to_bin(convert_to_two_symbol=True)


if __name__ == '__main__':
    unittest.main()
