import sys

from turing_machine import TuringMachine, TuringDefinition
from universal_turing_machine import UniversalTuringMachine
from two_tag_system import TwoTagSystem


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


def main():

    # version = "utm"
    # version = "tm"
    version = "2tag"

    transitions = {
        "X": "X"}
    halt_symbol = "#"
    string = "XXXXXXXXXX#"

    two_tag = TwoTagSystem(transitions)
    two_tag.set_input_string(string, halt_symbol)

    if version == "utm":
        utm = UniversalTuringMachine()
        # turing_machine.set_tape_string("ttbb1111111bb11b111111b1111111bb^1c1c")
        # turing_machine.set_tape_string("ttbb1bb^1c1c1c1c1c1c1c1c1c1c111c")
        utm.set_tape_string_from_2tag(two_tag)
        utm.run(True)
    elif version == "2tag":
        two_tag.run()


if __name__ == '__main__':
    main()
