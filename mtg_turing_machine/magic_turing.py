import sys

from turing_machine import TuringMachine, TuringDefinition
from universal_turing_machine import UniversalTuringMachine
from two_tag_system import TwoTagSystem, encode_tm_to_2tag


def load_tm_test():
    transitions = {
        ("q0", "A"): ("q0", "B", ">"),
        ("q0", "B"): ("q0", "A", ">"),
        ("q0", " "): ("qend", " ", "-")
    }
    tape = "AAAAAABBBBB"
    tape_index = 0
    initial_state = "q0"
    stop_states = ["qend"]

    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index)
    return TuringMachine(definition)


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


def main():

    # version = "utm"
    # version = "tm"
    # version = "2tm"
    # version = "2tm2tag"
    # version = "2tag"
    version = "2tm_2tag_utm"

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
    elif version == "2tm2tag":
        tm = load_tm2_test()
        two_tag = TwoTagSystem(tm)
        two_tag.run()
    elif version == "2tm_2tag_utm":
        tm = load_tm2_test()
        two_tag = TwoTagSystem(tm)
        utm = UniversalTuringMachine()
        utm.set_tape_string_from_2tag(two_tag)
        utm.run(linebreak=True)


if __name__ == '__main__':
    main()
