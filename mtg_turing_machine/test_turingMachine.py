import unittest

import definitions


def run_tm(tm, tape, convert_to_two_symbol):
    tm.set_tape_string(tape)
    if convert_to_two_symbol:
        tm.convert_to_two_symbol()
    tm.run()
    return tm.get_stripped_tape(decode_binarized=tm.is_binarized_tm)


class TestTuringMachine(unittest.TestCase):
    def test_run_write_one(self, convert_to_two_symbol=False):
        tm = definitions.load_tm_write_one()
        result = run_tm(tm, tape="", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1"])

        tm = definitions.load_tm_write_one()
        result = run_tm(tm, tape="111^", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1", "1", "1", "1"])

        tm = definitions.load_tm_write_one()
        result = run_tm(tm, tape="011", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1", "1", "1"])

    def test_run_write_one_two(self, convert_to_two_symbol=False):
        tm = definitions.load_tm_write_one_two()
        result = run_tm(tm, tape="", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1", "2"])

    def test_run_add_one(self, convert_to_two_symbol=False):
        tm = definitions.load_tm_add_one()
        result = run_tm(tm, tape="", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1"])

        tm = definitions.load_tm_add_one()
        result = run_tm(tm, tape="1^11", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1", "1", "1", "1"])

    def test_run_palindrome(self, convert_to_two_symbol=False):
        tm = definitions.load_tm_make_palindrome()
        result = run_tm(tm, tape="100", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1", "0", "0", "0", "0", "1"])

        tm = definitions.load_tm_make_palindrome()
        result = run_tm(tm, tape="10", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1", "0", "0", "1"])

    def test_run_dec_to_bin(self, convert_to_two_symbol=False):
        tm = definitions.load_tm_dec_to_bin()
        result = run_tm(tm, tape="9", convert_to_two_symbol=convert_to_two_symbol)
        self.assertEqual(result, ["1", "0", "0", "1"])

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
