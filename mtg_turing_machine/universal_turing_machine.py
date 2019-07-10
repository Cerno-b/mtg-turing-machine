from turing_machine import TuringMachine
from two_tag_system import TwoTagSystem


def encode_2tag_to_utm(two_tag_system):
    transitions = two_tag_system.transitions
    alphabet = set()
    for key, targets in transitions.items():
        alphabet.add(key)
        for symbol in targets:
            alphabet.add(symbol)
    alphabet = sorted(alphabet)
    if two_tag_system.halt_symbol not in alphabet:
        alphabet.append(two_tag_system.halt_symbol)

    input_string = two_tag_system.state

    letter_encodings = {}

    previous_transition_length = 0
    previous_encoding = 0
    for letter in alphabet:
        letter_encodings[letter] = previous_encoding + previous_transition_length + 1
        previous_encoding = letter_encodings[letter]
        if letter in transitions:
            transition = transitions[letter]
            previous_transition_length = len(transition)
        else:
            previous_transition_length = 0

    initial_tape = "tt"

    for i, letter in enumerate(reversed(alphabet)):
        if letter in transitions:
            transition = transitions[letter]
            transition = reversed(transition)
            transition_list = ["1"*letter_encodings[t] for t in transition]
            transition_encoding = "bb" + "1b".join(transition_list)
            print("transition {i}: encoding: {enc}".format(i=i, enc=transition_encoding))

            initial_tape += transition_encoding

    initial_tape += "bb^"

    input_encoding = ""
    for i, letter in enumerate(input_string):
        string = "1"*letter_encodings[letter]
        print("data {i}: encoding: {enc}".format(i=i, enc=string))
        input_encoding += string + "c"

    initial_tape += input_encoding

    print()
    print("letter encodings:")
    print()
    for letter in alphabet:
        print(letter, "1"*letter_encodings[letter])
    print()
    print("initial tape:", initial_tape)
    print("input:", input_string, "->", input_encoding)

    return initial_tape


class UniversalTuringMachine:
    def __init__(self):
        self._tm = TuringMachine("rogozhin_enc.txt")

    def set_tape_string(self, string):
        self._tm.tape_index = string.find("^")
        self._tm.tape = list(string.replace("^", ""))

    def set_tape_string_from_2tag(self, two_tag_system):
        self.set_tape_string(encode_2tag_to_utm(two_tag_system))

    def run(self, linebreak=False):
        self._tm.run(linebreak)
