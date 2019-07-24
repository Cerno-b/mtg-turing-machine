import sys

from turing_machine import TuringMachine


def simplify_tape(tape):
    temp_tape = []
    current_sub = []
    for t in tape:
        if not current_sub:
            current_sub.append(t)
        else:
            if current_sub[0] == t:
                current_sub.append(t)
            else:
                temp_tape.append(current_sub)
                current_sub = [t]

    out_tape = []
    for sub in temp_tape:
        out_tape.append((sub[0], len(sub)))
    return out_tape


def encode_2tag_to_utm(two_tag_system, brief=False, write_to_file=True):
    fid = None
    if write_to_file:
        fid = open("utm_tape.txt", "w")

    transitions = two_tag_system.transitions
    lefts = set()
    rights = set()
    for key, targets in transitions.items():
        lefts.add(key)
        for symbol in targets:
            rights.add(symbol)
    only_rights = rights.difference(lefts)

    inputs = set()
    for symbol in two_tag_system.state:
        inputs.add(symbol)

    # make sure all input symbols are part of the transitions
    assert lefts.union(rights).add(two_tag_system.halt_symbol) \
        == lefts.union(rights).union(inputs).add(two_tag_system.halt_symbol)

    # heal inconsistencies in the 2tag definition
    for symbol in only_rights:
        if symbol != two_tag_system.halt_symbol:
            transitions[symbol] = [symbol]

    alphabet = lefts.union(rights)
    alphabet = sorted(alphabet)
    alphabet = [a for a in alphabet if a != two_tag_system.halt_symbol]
    alphabet.append(two_tag_system.halt_symbol)  # make sure the halt symbol appears last for better encoding

    input_string = two_tag_system.state
    print(input_string)

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

    symbol_count = 0
    initial_tape = []
    if write_to_file:
        fid.write("c1< c1< ")
    else:
        initial_tape = ["c1<", "c1<"]
    symbol_count += 2

    if brief:
        print("encoding alphabet with {} letters".format(len(alphabet)))

    for i, letter in enumerate(reversed(alphabet)):
        if letter in transitions:
            transition = transitions[letter]
            transition = reversed(transition)
            transition_list = ["1"*letter_encodings[t] for t in transition]
            transition_encoding = "bb" + "1b".join(transition_list)
            transition_encoding = list(transition_encoding)
            if not brief:
                print("transition {i}: encoding: {enc}".format(i=i, enc=transition_encoding))

            if write_to_file:
                fid.write(" ".join(transition_encoding) + " ")
            else:
                initial_tape += transition_encoding
            symbol_count += len(transition_encoding)

    if write_to_file:
        fid.write("b ^ b ")
    else:
        initial_tape += list("b^b")
    symbol_count += 2

    input_encoding = ""
    for i, letter in enumerate(input_string):
        string = "1"*letter_encodings[letter]
        print("data {i}: encoding: {enc}".format(i=i, enc=string))
        input_encoding += string + "c"

    if write_to_file:
        fid.write(" ".join(list(input_encoding)) + " ")
    else:
        initial_tape += list(input_encoding)
    symbol_count += len(list(input_encoding))

    if not brief:
        print()
        print("letter encodings:")
        print()
        for letter in alphabet:
            print(letter, "1"*letter_encodings[letter])
        print()
        print("initial tape:", initial_tape)
        print("input:", input_string, "->", input_encoding)

    print("tape contains {} symbols".format(symbol_count))

    if write_to_file:
        fid.close()
        sys.exit("'write_to_file' is set to True, stopping computation here.")

    out_tape = simplify_tape(initial_tape)

    #inverted_encoding = {v: k for k, v in letter_encodings.items()}
    #for i, (sym, count) in enumerate(out_tape):
    #    print(sym, count, end=", ")
    #    if sym == "1":
    #        if out_tape[i+1] == ("b", 1):
    #            enc = inverted_encoding[count-1]
    #        else:
    #            enc = inverted_encoding[count]
    #        print("-->", enc, end="")
    #    print()

    return initial_tape, letter_encodings


class UniversalTuringMachine:
    def __init__(self):
        self._tm = TuringMachine("rogozhin.txt")
        self._tm.blank = "1<"
        self.letter_encodings = {}

    def set_tape_string(self, string):
        self._tm.tape_index = string.index("^")
        self._tm.tape = [symbol for symbol in string if symbol != "^"]

    def set_tape_string_from_2tag(self, two_tag_system, brief=False, write_to_file=False):
        tape, letter_encodings = encode_2tag_to_utm(two_tag_system, brief=brief, write_to_file=write_to_file)
        self.set_tape_string(tape)
        self.letter_encodings = letter_encodings

    def get_tape_from_2tag(self):
        inverse_encoding = {value: key for key, value in self.letter_encodings.items()}
        out_list = []
        count = 0
        for symbol in self._tm.tape:
            if symbol == "1":
                count += 1
            if symbol == "c" and count > 0:
                out_list.append(inverse_encoding[count])
                count = 0
        return out_list

    def get_tape(self):
        return self._tm.tape

    def run(self, linebreak=False, write_to_file=False, brief=False):
        if write_to_file:
            with open("letter_encodings.txt", "w") as fid:
                max_len = max([len(s) for s in self.letter_encodings.keys()])
                for key, value in self.letter_encodings.items():
                    left = str(key) + ": "
                    left = left.ljust(max_len + 3)
                    fid.write("{left}{enc}\n".format(left=left, enc=value))

        self._tm.run(linebreak=linebreak, write_to_file=write_to_file, brief=brief)

        print()
        print("Output:")
        print(self.get_tape_from_2tag())
