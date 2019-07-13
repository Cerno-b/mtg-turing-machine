import sys

from turing_machine import TuringMachine, TuringDefinition
from universal_turing_machine import UniversalTuringMachine
from two_tag_system import TwoTagSystem, encode_tm_to_2tag


# def load_tm_test():
#     transitions = {
#         ("q0", "A"): ("q0", "B", ">"),
#         ("q0", "B"): ("q0", "A", ">"),
#         ("q0", " "): ("qend", " ", "-")
#     }
#     tape = "AAAAAABBBBB"
#     tape_index = 0
#     initial_state = "q0"
#     stop_states = ["qend"]
#
#     definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index)
#     return TuringMachine(definition)


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


def load_tm_test():
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
    tape = "11"
    tape_index = 0
    initial_state = "q0"
    blank = "_"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    return TuringMachine(definition)


def main():

    # version = "utm"
    # version = "tm"
    # version = "2tm"
    # version = "2tm_2tag"
    # version = "2tag"
    # version = "2tm_2tag_utm"
    # version = "tm_2tm"
    version = "tm_2tm_2tag"

    transitions = {
        "X": ["X"]}
    halt_symbol = "#"
    string = "XXXXXXXXXX#"
    string_list = list(string)

    two_tag = TwoTagSystem(transitions)
    two_tag.set_input_string(string_list, halt_symbol)

    if version == "utm":
        utm = UniversalTuringMachine()
        # turing_machine.set_tape_string("ttbb1111111bb11b111111b1111111bb^1c1c")
        # turing_machine.set_tape_string("ttbb1bb^1c1c1c1c1c1c1c1c1c1c111c")
        utm.set_tape_string_from_2tag(two_tag)
        utm.run(linebreak=True)
    elif version == "2tag":
        two_tag.run()
    elif version == "2tm":
        tm = load_tm2_test()
        tm.run(linebreak=True)
    elif version == "2tm_2tag":
        tm = load_tm2_test()
        two_tag = TwoTagSystem(tm)
        two_tag.run()
    elif version == "2tm_2tag_utm":
        tm = load_tm2_test()
        two_tag = TwoTagSystem(tm)
        utm = UniversalTuringMachine()
        utm.set_tape_string_from_2tag(two_tag)
        utm.run(linebreak=True)
    elif version == "tm":
        tm = load_tm_test()
        tm.run(linebreak=True)
    elif version == "tm_2tm":
        tm = load_tm_test()
        tm.convert_to_two_symbol()
        tm.run(linebreak=True)
        print("Decoded tape:", tm.decode_binarized_tape())
    elif version == "tm_2tm_2tag":
        tm = load_tm_test()
        tm.convert_to_two_symbol()
        two_tag = TwoTagSystem(tm)
        two_tag.run(brief=True)


if __name__ == '__main__':
    main()
