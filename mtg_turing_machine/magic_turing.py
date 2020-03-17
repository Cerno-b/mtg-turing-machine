import timeit

from mtg_turing_machine.classes.universal_turing_machine import UniversalTuringMachine
from mtg_turing_machine.classes.two_tag_system import TwoTagSystem, encode_tm_to_2tag

import mtg_turing_machine.classes.instances as examples


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


def main():

    # version = "utm"
    # version = "tm"
    # version = "2tm"
    # version = "2tm_2tag"
    # version = "2tag"
    # version = "2tm_2tag_utm"
    # version = "tm_2tm"
    # version = "tm_2tm_2tag"
    # version = "tm_2tm_2tag_utm"
    version = "add_unary"

    if version == "utm":
        two_tag = examples.load_two_tag_cut_in_half()
        utm = UniversalTuringMachine()
        # turing_machine.set_tape_string("ttbb1111111bb11b111111b1111111bb^1c1c")
        # turing_machine.set_tape_string("ttbb1bb^1c1c1c1c1c1c1c1c1c1c111c")
        utm.set_tape_string_from_two_tag(two_tag)
        utm.run(line_break=True)
    elif version == "add_unary":
        time = 0

        tm = examples.load_tm_add_unary()
        tm.set_tape_string("11x111")
        tm.print_summary()
        # tm.run()
        print("\n\n")
        tm.convert_to_two_symbol()
        tm.print_summary()
        two_tag = TwoTagSystem(tm)
        two_tag.print_summary()

        # time = timeit.timeit(lambda: two_tag.run(silent=True), number=1)

        utm = UniversalTuringMachine()
        utm.set_tape_string_from_two_tag(two_tag, silent=True)
        time = timeit.timeit(lambda: utm.run(brief=True), number=1)
        print(time)

    elif version == "2tag":
        two_tag = examples.load_two_tag_cut_in_half()
        two_tag.run()
    elif version == "2tm":
        tm = examples.load_tm2_test()
        tm.run(line_break=True)
    elif version == "2tm_2tag":
        tm = examples.load_tm2_test()
        two_tag = TwoTagSystem(tm)
        two_tag.run()
    elif version == "2tm_2tag_utm":
        tm = examples.load_tm2_test()
        two_tag = TwoTagSystem(tm)
        utm = UniversalTuringMachine()
        utm.set_tape_string_from_two_tag(two_tag)
        utm.run(line_break=True)
    elif version == "tm":
        tm = examples.load_tm_make_palindrome()
        tm.run(line_break=True)
    elif version == "tm_2tm":
        tm = examples.load_tm_make_palindrome()
        tm.convert_to_two_symbol()
        print(tm.binarized_bit_depth)
        tm.run(line_break=True)
        print("Decoded tape:", tm.decode_binarized_tape())
    elif version == "tm_2tm_2tag":
        tm = examples.load_tm_make_palindrome()
        print("Original Machine:")
        tm.print(line_break=True)
        tm.convert_to_two_symbol()
        print("2-Symbol Machine:")
        tm.print(line_break=True)
        two_tag = TwoTagSystem(tm)
        print("2-tag System")
        two_tag.run(brief=True)
    elif version == "tm_2tm_2tag_utm":
        tm = examples.load_tm_write_one()
        print("Original Machine:")
        alphabet = set([a for _, a in tm.transitions.keys()])
        print("  {} symbols, {} transitions".format(len(alphabet), len(tm.transitions)))
        tm.convert_to_two_symbol()
        print("2-Symbol Machine:")
        print("  2 symbols, {} transitions".format(len(tm.transitions)))
        two_tag = TwoTagSystem(tm)
        print("2-tag System:")
        alphabet = set([a for a in two_tag.production_rules.keys()])
        for key, value in two_tag.production_rules.items():
            print(key, value)
        print("  {} symbols, {} transitions".format(len(alphabet), len(tm.transitions)))
        # two_tag.print()
        print("UTM:")
        utm = UniversalTuringMachine()
        write_to_file = True
        brief = False
        utm.set_tape_string_from_two_tag(two_tag, write_to_file=False, brief=brief)
        utm.run(write_to_file=write_to_file, brief=brief)


if __name__ == '__main__':
    main()
