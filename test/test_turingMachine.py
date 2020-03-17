import unittest

import mtg_turing_machine.classes.instances as instances


def run_turing_machine(turing_machine, tape=None, convert_to_binary_tm=False):
    """Helper function: run a Turing machine and return its output tape
    Arguments:
        turing_machine: The Turing machine to run
        tape: If not None, set the Turing tape instead of using the one currently in the Turing machine
        convert_to_binary_tm: Flag to control whether the Turing machine should be converted to a binary TM"""
    if tape is not None:
        turing_machine.set_tape_string(tape)
    if convert_to_binary_tm:
        turing_machine.convert_to_two_symbol()
    turing_machine.run(brief=True)
    return turing_machine.get_stripped_tape(decode_binarized=turing_machine.has_been_binarized)


class TestTuringMachine(unittest.TestCase):

    def test_run_add_unary(self, convert_to_two_symbol=False):
        """Test: run the Turing machine 'Unary Adder'."""
        # Input: 3+2 in unary: 111 + 11
        # Output: 5 in unary 11111
        tm = instances.load_tm_add_unary()
        result = run_turing_machine(tm, tape="111x11", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1", "1", "x"], result)

    def test_run_add_unary_2_symbol(self, convert_to_two_symbol=False):
        """Test: run the Turing machine 'Unary Adder' (Optimized two symbol version)"""
        # Input: 3+2 in unary: 111 + 11
        # Output: 5 in unary 11111
        tm = instances.load_tm_add_unary_two_symbol()
        result = run_turing_machine(tm, tape="111011", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1", "1"], result)

    def test_run_write_one(self, convert_to_two_symbol=False):
        """Test: run the Turing Machine 'Write 1' that writes 1 at the current head position"""
        # Input: Empty tape
        # Output: 1
        tm = instances.load_tm_write_one()
        result = run_turing_machine(tm, tape="", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1"], result)

        # Input: 011 (Turing head at the left end)
        # Output: 111
        tm = instances.load_tm_write_one()
        result = run_turing_machine(tm, tape="011", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1"], result)

        # Input: 111 (Turing head at the right end)
        # Output: 1111
        tm = instances.load_tm_write_one()
        result = run_turing_machine(tm, tape="111^", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1"], result)

    def test_run_write_one_two(self, convert_to_two_symbol=False):
        """Test: run the Turing Machine 'Write 1 2' that writes 1 2 at the current head position"""
        # Input: Empty tape
        # Output: 1 2
        tm = instances.load_tm_write_one_two()
        result = run_turing_machine(tm, tape="", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "2"], result)

        # Input: 1 1 1 (Turing head at the left end)
        # Output: 1 2 1
        tm = instances.load_tm_write_one_two()
        result = run_turing_machine(tm, tape="111", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "2", "1"], result)

        # Input: 1 1 (Turing head at the right end)
        # Output: 1 1 1 2
        tm = instances.load_tm_write_one_two()
        result = run_turing_machine(tm, tape="11^", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "2"], result)

    def test_run_add_one(self, convert_to_two_symbol=False):
        """Test: run the Turing Machine 'Add 1' that adds 1 to a string of ones"""
        # Input: empty tape
        # Output: 1
        tm = instances.load_tm_add_one()
        result = run_turing_machine(tm, tape="", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1"], result)

        # Input: 1 1 1 (Turing head one to the right of the tape's left end)
        # Output: 1 1 1 1
        tm = instances.load_tm_add_one()
        result = run_turing_machine(tm, tape="1^11", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "1", "1", "1"], result)

    def test_run_palindrome(self, convert_to_two_symbol=False):
        """Test: Run the Turing Machine 'Palindrome'"""
        # Input: 1 0 0
        # Output: 1 0 0 0 0 1
        tm = instances.load_tm_make_palindrome()
        result = run_turing_machine(tm, tape="100", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "0", "0", "0", "0", "1"], result)

        # Input: 1 0
        # Output: 1 0 0 1
        tm = instances.load_tm_make_palindrome()
        result = run_turing_machine(tm, tape="10", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "0", "0", "1"], result)

    def test_run_dec_to_bin(self, convert_to_two_symbol=False):
        """Test: Run the Turing Machine 'Decimal to Binary'"""
        # Input: 11 (decimal)
        # Output: 1 1 0 1 (binary, written from right to left)
        tm = instances.load_tm_dec_to_bin()
        result = run_turing_machine(tm, tape="11", convert_to_binary_tm=convert_to_two_symbol)
        self.assertEqual(["1", "1", "0", "1"], result)

    def test_run_add_unary_as_2_symbol(self):
        """Rerun test as binary Turing machine"""
        self.test_run_add_unary(convert_to_two_symbol=True)

    def test_run_write_one_as_2_symbol(self):
        """Rerun test as binary Turing machine"""
        self.test_run_write_one(convert_to_two_symbol=True)

    def test_run_write_one_two_as_2_symbol(self):
        """Rerun test as binary Turing machine"""
        self.test_run_write_one_two(convert_to_two_symbol=True)

    def test_run_add_one_as_2_symbol(self):
        """Rerun test as binary Turing machine"""
        self.test_run_add_one(convert_to_two_symbol=True)

    def test_run_palindrome_as_2_symbol(self):
        """Rerun test as binary Turing machine"""
        self.test_run_palindrome(convert_to_two_symbol=True)

    def test_run_dec_to_bin_as_2_symbol(self):
        """Rerun test as binary Turing machine"""
        self.test_run_dec_to_bin(convert_to_two_symbol=True)


if __name__ == '__main__':
    unittest.main()
