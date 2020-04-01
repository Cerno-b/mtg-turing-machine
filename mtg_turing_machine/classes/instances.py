from .turing_machine import TuringMachine
from .turing_machine import TuringDefinition
from .two_tag_system import TwoTagSystem
from .universal_turing_machine import UniversalTuringMachine


def load_tm_add_unary():
    """Turing Machine 'Unary Adder'.
    Computes the sum of two numbers in unary.
    This machine has three symbols for testing purposes.
    Check load_tm_add_unary_two_symbol() for an example with just two symbols"""
    transitions = {
        ("q0", "1"): ("q0", "1", ">"),
        ("q0", "x"): ("q1", "x", ">"),
        ("q1", "_"): ("qend", "_", "<"),
        ("q1", "1"): ("q2", "x", "<"),
        ("q2", "x"): ("q0", "1", ">")
    }
    tape = "111x11"
    tape_index = 0
    initial_state = "q0"
    blank = "_"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_tm_add_unary_two_symbol():
    """Turing Machine 'Unary Adder'.
    Optimized version of load_tm_add_unary() that only has two symbols.
    This makes the machine a binary Turing Machine."""
    transitions = {
        ("q0", "1"): ("q0", "1", ">"),
        ("q0", "0"): ("q1", "0", ">"),
        ("q1", "0"): ("qend", "0", "<"),
        ("q1", "1"): ("q2", "0", "<"),
        ("q2", "0"): ("q3", "1", ">"),
        ("q3", "0"): ("q1", "0", ">"),
    }
    tape = "111011"
    tape_index = 0
    initial_state = "q0"
    blank = "0"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_tm_write_one():
    """Turing Machine 'Write 1'.
    Very simplistic machine that replaces the current symbol with 1."""
    transitions = {
        ("q0", "0"): ("qend", "1", ">"),
        ("q0", "1"): ("qend", "1", ">")
    }
    tape = "0"
    tape_index = 0
    initial_state = "q0"
    blank = "0"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_tm_write_one_two():
    """Turing Machine 'Write 1 2'.
    Simplistic machine that replaces the next two symbols with 1 and 2"""
    transitions = {
        ("q0", "0"): ("q1", "1", ">"),
        ("q0", "1"): ("q1", "1", ">"),
        ("q1", "0"): ("qend", "2", ">"),
        ("q1", "1"): ("qend", "2", ">")
    }
    tape = "0"
    tape_index = 0
    initial_state = "q0"
    blank = "0"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_tm_add_one():
    """Turing Machine 'Add 1'.
    Adds an additional 1 to the end of a string of ones."""
    transitions = {
        ("q0", "1"): ("q0", "1", ">"),
        ("q0", "0"): ("qend", "1", ">")
    }
    tape = "11"
    tape_index = 0
    initial_state = "q0"
    blank = "0"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_tm_make_palindrome():
    """Turing Machine 'Make Palindrome'.
    Appends the input tape to the end in reversed form to create a palindrome."""
    transitions = {
        ("q0", "0"): ("q0", "0", ">"),
        ("q0", "1"): ("q0", "1", ">"),
        ("q0", "o"): ("q0", "0", ">"),
        ("q0", "i"): ("q0", "1", ">"),
        ("q0", "_"): ("q1", "_", "<"),
        ("q1", "0"): ("q2", "o", ">"),
        ("q1", "1"): ("q3", "i", ">"),
        ("q1", "o"): ("q1", "o", "<"),
        ("q1", "i"): ("q1", "i", "<"),
        ("q2", "_"): ("q1", "o", "<"),
        ("q3", "_"): ("q1", "i", "<"),
        ("q2", "0"): ("q2", "0", ">"),
        ("q2", "1"): ("q2", "1", ">"),
        ("q2", "o"): ("q2", "o", ">"),
        ("q2", "i"): ("q2", "i", ">"),
        ("q3", "0"): ("q3", "0", ">"),
        ("q3", "1"): ("q3", "1", ">"),
        ("q3", "o"): ("q3", "o", ">"),
        ("q3", "i"): ("q3", "i", ">"),
        ("q1", "_"): ("q4", "_", ">"),
        ("q4", "o"): ("q4", "0", ">"),
        ("q4", "i"): ("q4", "1", ">"),
        ("q4", "0"): ("q4", "0", "<"),
        ("q4", "1"): ("q4", "1", "<"),
        ("q4", "_"): ("qend", "_", ">")
    }
    tape = "10"
    tape_index = 0
    initial_state = "q0"
    blank = "_"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_tm_dec_to_bin():
    """Turing Machine 'Decimal to Binary Converter'.
    Reads a decimal number from the tape and replaces it with its binary representation."""
    transitions = {
        ("q0", "0"): ("q0", "0", ">"),
        ("q0", "1"): ("q0", "1", ">"),
        ("q0", "2"): ("q0", "2", ">"),
        ("q0", "3"): ("q0", "3", ">"),
        ("q0", "4"): ("q0", "4", ">"),
        ("q0", "5"): ("q0", "5", ">"),
        ("q0", "6"): ("q0", "6", ">"),
        ("q0", "7"): ("q0", "7", ">"),
        ("q0", "8"): ("q0", "8", ">"),
        ("q0", "9"): ("q0", "9", ">"),
        ("q0", "_"): ("q1", "0", "<"),
        ("q1", "0"): ("q1", "0", "<"),
        ("q1", "1"): ("q2", "0", ">"),
        ("q1", "2"): ("q1", "1", "<"),
        ("q1", "3"): ("q2", "1", ">"),
        ("q1", "4"): ("q1", "2", "<"),
        ("q1", "5"): ("q2", "2", ">"),
        ("q1", "6"): ("q1", "3", "<"),
        ("q1", "7"): ("q2", "3", ">"),
        ("q1", "8"): ("q1", "4", "<"),
        ("q1", "9"): ("q2", "4", ">"),
        ("q2", "0"): ("q3", "5", "<"),
        ("q2", "1"): ("q3", "6", "<"),
        ("q2", "2"): ("q3", "7", "<"),
        ("q2", "3"): ("q3", "8", "<"),
        ("q2", "4"): ("q3", "9", "<"),
        ("q3", "0"): ("q1", "0", "<"),
        ("q3", "1"): ("q1", "1", "<"),
        ("q3", "2"): ("q1", "2", "<"),
        ("q3", "3"): ("q1", "3", "<"),
        ("q3", "4"): ("q1", "4", "<"),
        ("q1", "_"): ("q4", "_", ">"),
        ("q4", "0"): ("q4", "_", ">"),
        ("q4", "1"): ("q5", "1", ">"),
        ("q4", "2"): ("q5", "2", ">"),
        ("q4", "3"): ("q5", "3", ">"),
        ("q4", "4"): ("q5", "4", ">"),
        ("q4", "5"): ("q5", "5", ">"),
        ("q4", "6"): ("q5", "6", ">"),
        ("q4", "7"): ("q5", "7", ">"),
        ("q4", "8"): ("q5", "8", ">"),
        ("q4", "9"): ("q5", "9", ">"),
        ("q4", "_"): ("qend", "_", ">"),
        ("q5", "0"): ("q5", "0", ">"),
        ("q5", "1"): ("q5", "1", ">"),
        ("q5", "2"): ("q5", "2", ">"),
        ("q5", "3"): ("q5", "3", ">"),
        ("q5", "4"): ("q5", "4", ">"),
        ("q5", "5"): ("q5", "5", ">"),
        ("q5", "6"): ("q5", "6", ">"),
        ("q5", "7"): ("q5", "7", ">"),
        ("q5", "8"): ("q5", "8", ">"),
        ("q5", "9"): ("q5", "9", ">"),
        ("q5", "_"): ("q6", "_", "<"),
        ("q6", "0"): ("q10", "_", ">"),
        ("q10", "_"): ("q7", "_", ">"),
        ("q6", "5"): ("q11", "_", ">"),
        ("q11", "_"): ("q8", "_", ">"),
        ("q7", "0"): ("q7", "0", ">"),
        ("q7", "1"): ("q7", "1", ">"),
        ("q8", "0"): ("q8", "0", ">"),
        ("q8", "1"): ("q8", "1", ">"),
        ("q7", "_"): ("q9", "0", "<"),
        ("q8", "_"): ("q9", "1", "<"),
        ("q9", "0"): ("q9", "0", "<"),
        ("q9", "1"): ("q9", "1", "<"),
        ("q9", "_"): ("q12", "_", "<"),
        ("q12", "_"): ("q1", "0", "<")
    }
    tape = "3"
    tape_index = 0
    initial_state = "q0"
    blank = "_"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_dummy_utm():
    """A simple dummy UTM. Does not really encode anything sensible, but is capable to run as a UTM program for
    a few iteration and then stops."""
    utm = UniversalTuringMachine()
    tape = ["1>", "^", "1", "c1>", "b2", "c1>"]
    utm.set_tape_string(tape)
    return utm


def load_two_tag_cut_in_half():
    """Two Tag System 'Cut In Half'. 
    Trivial two tag system that takes the input word and removes each second letter."""
    production_rules = {
        "X": ["X"],
        ":": ["i"],
    }
    halt_symbol = "#"
    initial_word = "XX::XX::XX::#"

    two_tag = TwoTagSystem(production_rules)
    two_tag.set_initial_word(initial_word, halt_symbol)
    return two_tag


def load_two_tag_collatz():
    """Two Tag System 'Compute Collatz Sequence'.
    Computes a Collatz sequence (https://en.wikipedia.org/wiki/Tag_system#Example:_Computation_of_Collatz_sequences)"""
    production_rules = {
        "a": ["b", "c"],
        "b": ["a"],
        "c": ["a", "a", "a"],
    }
    halt_symbol = "#"
    initial_word = "aaa"

    two_tag = TwoTagSystem(production_rules)
    two_tag.set_initial_word(initial_word, halt_symbol)
    return two_tag


def load_two_tag_manually_converted_from_simple_tm():
    """Two Tag System 'Converted From TM'.
    A two tag system manually converted from a simple Turing machine unit testing the conversion process."""
    production_rules = {
        'A_q_init_0': ['C_q_init_0', 'x'],
        'C_q_init_0': ['D_q_init_0_1', 'D_q_init_0_0'],
        'D_q_init_0_0': ['x', 'A_q0_0', 'x'],
        'D_q_init_0_1': ['A_q0_1', 'x'],
        'B_q_init_0': ['S_q_init_0'],
        'S_q_init_0': ['T_q_init_0_1', 'T_q_init_0_0'],
        'T_q_init_0_0': ['B_q0_0', 'x'],
        'T_q_init_0_1': ['B_q0_1', 'x'],
        'A_q0_0': ['C_q0_0', 'x', 'c_q0_0', 'x'],
        'A_q0_1': ['C_q0_1', 'x', 'c_q0_1', 'x'],
        'C_q0_0': ['D_q0_0_1', 'D_q0_0_0'],
        'C_q0_1': ['D_q0_1_1', 'D_q0_1_0'],
        'c_q0_0': ['d_q0_0_1', 'd_q0_0_0'],
        'c_q0_1': ['d_q0_1_1', 'd_q0_1_0'],
        'D_q0_0_0': ['x', '#', 'x'],
        'D_q0_0_1': ['#', 'x'],
        'D_q0_1_0': ['x', '#', 'x'],
        'D_q0_1_1': ['#', 'x'],
        'd_q0_0_0': ['a_#', 'x'],
        'd_q0_0_1': ['a_#', 'x'],
        'd_q0_1_0': ['a_#', 'x'],
        'd_q0_1_1': ['a_#', 'x'],
        'B_q0_0': ['S_q0_0'],
        'B_q0_1': ['S_q0_1'],
        'S_q0_0': ['T_q0_0_1', 'T_q0_0_0'],
        'S_q0_1': ['T_q0_1_1', 'T_q0_1_0'],
        'T_q0_0_0': ['B_#', 'x'],
        'T_q0_0_1': ['B_#', 'x'],
        'T_q0_1_0': ['B_#', 'x'],
        'T_q0_1_1': ['B_#', 'x'],
        'a_q_init_0': ['c_q_init_0', 'x', 'c_q_init_0', 'x'],
        'c_q_init_0': ['d_q_init_0_1', 'd_q_init_0_0'],
        'd_q_init_0_0': ['a_q0_0', 'x'],
        'd_q_init_0_1': ['a_q0_1', 'x'],
        'a_q0_0': ['c_q0_0', 'x', 'c_q0_0', 'x'],
        'a_q0_1': ['c_q0_1', 'x', 'c_q0_1', 'x'],
        'b_q_init_0': ['s_q_init_0'],
        's_q_init_0': ['t_q_init_0_1', 't_q_init_0_0'],
        't_q_init_0_0': ['b_q0_0', 'x'],
        't_q_init_0_1': ['b_q0_1', 'x'],
        'b_q0_0': ['s_q0_0'],
        'b_q0_1': ['s_q0_1'],
        's_q0_0': ['t_q0_0_1', 't_q0_0_0'],
        's_q0_1': ['t_q0_1_1', 't_q0_1_0'],
        't_q0_0_0': ['b_#', 'x'],
        't_q0_0_1': ['b_#', 'x'],
        't_q0_1_0': ['b_#', 'x'],
        't_q0_1_1': ['b_#', 'x']
    }

    halt_symbol = "#"
    string_list = ["A_q_init_0", "x", 'B_q_init_0', "x"]

    two_tag = TwoTagSystem(production_rules)
    two_tag.set_initial_word(string_list, halt_symbol)
    return two_tag
