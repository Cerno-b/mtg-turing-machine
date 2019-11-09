from turing_machine import TuringMachine
from turing_machine import TuringDefinition
from two_tag_system import TwoTagSystem


def load_tm2_test():
    transitions = {
        ("qs", "0"): ("qs",   "0", ">"),
        ("qs", "1"): ("q0",   "0", ">"),
        ("q0", "0"): ("q1",   "0", ">"),
        ("q0", "1"): ("q0",   "1", ">"),
        ("q1", "0"): ("q1",   "0", ">"),
        ("q1", "1"): ("q2",   "1", ">"),
        ("q2", "0"): ("q6",   "0", "<"),
        ("q2", "1"): ("q3",   "0", "<"),
        ("q3", "0"): ("qerr", "0", "<"),
        ("q3", "1"): ("q4",   "0", "<"),
        ("q4", "0"): ("q4",   "0", "<"),
        ("q4", "1"): ("q5",   "1", ">"),
        ("q5", "0"): ("q0",   "1", ">"),
        ("q5", "1"): ("qerr", "1", ">"),
        ("q6", "0"): ("qerr", "0", ">"),
        ("q6", "1"): ("qend", "0", "<"),
    }
    tape = "11011001101"
    tape_index = 0
    initial_state = "qs"
    blank = "0"
    stop_states = ["qend", "qerr"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def load_tm_add_unary():
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


def load_tm_write_one():
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


def load_two_tag_divide_by_2():
    transitions = {
        "X": ["X"],
        ":": ["i"],
    }
    halt_symbol = "#"
    string = "XX::XX::XX::#"
    string_list = list(string)

    two_tag = TwoTagSystem(transitions)
    two_tag.set_input_string(string_list, halt_symbol)
    return two_tag


def load_two_tag_collatz():
    transitions = {
        "a": ["b", "c"],
        "b": ["a"],
        "c": ["a", "a", "a"],
    }
    halt_symbol = "#"
    string = "aaa"
    string_list = list(string)

    two_tag = TwoTagSystem(transitions)
    two_tag.set_input_string(string_list, halt_symbol)
    return two_tag


def load_two_tag_manually_converted_from_simple_tm():
    transitions = {
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

    two_tag = TwoTagSystem(transitions)
    two_tag.set_input_string(string_list, halt_symbol)
    return two_tag

