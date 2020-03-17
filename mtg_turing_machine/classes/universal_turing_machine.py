import sys
import os

from .turing_machine import TuringMachine


class UniversalTuringMachine:
    """Definition of a Universal Turing Machine. A UTM is a regular turing machine with a special program
    that allows it to simulate any Turing machine encoded on its tape. This UTM uses a UTM(2,18) developed by
    Yurii Rogozhin. It has two states and 18 symbols.
    Attributes:
        _tm:                        The Turing machine running the emulation
        from_two_tag_system:        Flag whether the UTM has been created from a two tag system definition.
        from_binary_turing_machine: Flag whether the UTM's two tag system has been created from a binary Turing machine
        symbol_encodings:           Each symbol of the emulated machine must be encoded to the UTM's symbol set. (dict)
        """
    def __init__(self):
        """Initialize UTM"""
        current_dir = os.path.dirname(__file__)
        definition_path = os.path.join(current_dir, "rogozhin_utm_2_18.txt")
        self._tm = TuringMachine(definition_path)
        self._tm.definition.blank = "1<"  # set the UTM(2,18)'s blank symbol
        self.from_two_tag_system = False
        self.from_binary_turing_machine = False
        self.symbol_encodings = {}

    def set_tape_string(self, string):
        """Set the UTM's tape.
        Arguments:
            string: The tape in string form.
            Expects to find exactly one head marker (^) right before the head position."""
        assert string.count("^") == 1
        self._tm.definition.tape_index = string.index("^")
        self._tm.definition.tape = [symbol for symbol in string if symbol != "^"]
        self.from_two_tag_system = False

    def set_tape_string_from_two_tag(self, two_tag_system, brief=False, write_to_file_only=False, silent=True):
        """Encode a two tag system as Turing tape interpretable by a UTM(2,18).
        For details on the encoding scheme, refer to Rogozhin's paper in the literature directory.
        Arguments:
            two_tag_system:     The two tag system to be encoded
            brief:              Print output in brief form
            write_to_file_only: Write the encoding to file and exit
            silent:             Suppress printing"""

        fid = None
        if write_to_file_only:
            fid = open("utm_tape.txt", "w")

        production_rules = two_tag_system.production_rules

        # production rules have the form "symbol (letter) -> production (word)"
        left_hand_symbols = set()  # the set of symbols on the left side of the production rules
        right_hand_symbols = set()  # the set of symbols on the right side of the production rules
        for left_hand_symbol, production in production_rules.items():
            left_hand_symbols.add(left_hand_symbol)
            for right_hand_symbol in production:
                right_hand_symbols.add(right_hand_symbol)
        symbols_only_on_right_hand = right_hand_symbols.difference(left_hand_symbols)

        # The alphabet is a list of all symbols.
        # Since symbols are encoded by increasingly long strings, it makes sense to place frequent
        # symbols in the beginning and less frequent ones at the end.
        # For simplicity, the very frequent symbol 'x' goes to the front, while the rare halting symbol goes to the end.
        # todo: There might be some room for optimization here by further ordering the alphabet
        alphabet = left_hand_symbols.union(right_hand_symbols)
        alphabet = sorted(alphabet)
        alphabet = [a for a in alphabet if a != two_tag_system.halting_symbol]
        alphabet.append(two_tag_system.halting_symbol)
        if "x" in alphabet:
            alphabet = [a for a in alphabet if a != "x"]
            alphabet = ["x"] + alphabet

        input_symbols = set(two_tag_system.current_word)

        # make sure all input symbols are part of the production rules
        assert set(alphabet) == set(alphabet).union(input_symbols)

        # Make sure that no symbols occur only on the right hand side.
        # This is not strictly necessary in a two-tag system but seems to be required during conversion to UTM.
        # It is realized by adding a dummy rule for each unused symbol that should never be reached
        # todo: Test putting the dummy symbols to the end of the alphabet for optimization
        for only_right_hand_symbol in symbols_only_on_right_hand:
            if only_right_hand_symbol != two_tag_system.halting_symbol:
                production_rules[only_right_hand_symbol] = [only_right_hand_symbol]

        input_word = two_tag_system.current_word
        if not silent:
            print(input_word)

        symbol_encodings = {}

        # the symbols are encoded by assigning a number to each symbol whose value is determined by
        # the previous symbol's number and the previous production length.
        # A "production" is the right hand side of a production rule.
        # For details refer to Rogozhin's paper.
        previous_production_length = 0
        previous_encoding = 0
        for symbol in alphabet:
            symbol_encodings[symbol] = previous_encoding + previous_production_length + 1
            previous_encoding = symbol_encodings[symbol]
            if symbol != two_tag_system.halting_symbol:
                production = production_rules[symbol]
                previous_production_length = len(production)
            else:
                previous_production_length = 0

        # After encoding the alphabet, set up the Turing tape as a program and data section
        # For details on the encoding scheme refer to Rogozhin's paper.

        # start with the beginning markers and the program section (encoding the production rules)
        symbol_count = 2
        tape_program_section = ["c1<", "c1<"]
        if write_to_file_only:
            fid.write("c1< c1< ")

        for i, symbol in enumerate(reversed(alphabet)):
            if symbol != two_tag_system.halting_symbol:
                production = production_rules[symbol]
                production = reversed(production)
                # the symbol encodings are represented here as a string of ones
                # whose length corresponds to the symbol's encoding number
                encoded_production = ["1" * symbol_encodings[symbol] for symbol in production]
                encoded_production = "bb" + "1b".join(encoded_production)  # add spacers
                encoded_production = list(encoded_production)  # all symbols used here have only one letter

                if not brief and not silent:
                    print("production {i}: encoding: {enc}".format(i=i, enc=encoded_production))

                symbol_count += len(encoded_production)
                tape_program_section += encoded_production
                if write_to_file_only:
                    fid.write(" ".join(encoded_production) + " ")

        if brief and not silent:
            print("encoded an alphabet that has {} letters".format(len(alphabet)))

        # add spacers and the Turing head marker (^)
        symbol_count += 2
        tape_program_section += list("b^b")
        if write_to_file_only:
            fid.write("b ^ b ")

        # encode the data section next (right of the head)

        tape_data_section = []
        for i, symbol in enumerate(input_word):
            # the symbol encodings are represented here as a string of ones
            # whose length corresponds to the symbol's encoding number
            string_encoding = "1" * symbol_encodings[symbol]
            if not silent:
                print("input word[{i}]: encoding: {enc}".format(i=i, enc=string_encoding))
            tape_data_section += list(string_encoding + "c")  # add spacer

        if write_to_file_only:
            fid.write(" ".join(tape_data_section) + " ")

        turing_tape = tape_program_section + tape_data_section

        # the tape now contains the program and data section, with the Turing head right in between.

        if not brief and not silent:
            print()
            print("letter encodings:")
            print()
            for symbol in alphabet:
                print(symbol, "1" * symbol_encodings[symbol])
            print()
            print("initial Turing tape:", turing_tape)
            print("two tag system initial word: ", input_word)
            print("    encoded as ", tape_data_section)

        print("The tape contains {} symbols, ".format(len(turing_tape)))
        print("    {} in the program section and {} in the data section".format(len(tape_program_section),
                                                                                len(tape_data_section)))

        if write_to_file_only:
            fid.close()
            sys.exit("'write_to_file_only' is set to True, stopping computation here.")

        self.set_tape_string(turing_tape)
        self.symbol_encodings = symbol_encodings
        self.from_two_tag_system = True
        self.from_binary_turing_machine = two_tag_system.from_turing_machine

    def decode_tape_as_two_tag_word(self):
        """Decodes the Turing tape's data section to the corresponding two tag system word.
        Only works if the UTM has been created via two tag system and after the UTM stopped"""

        assert self.from_two_tag_system

        inverse_encoding = {value: key for key, value in self.symbol_encodings.items()}
        output_word = []
        count = 0
        for symbol in self._tm.definition.tape:
            if symbol == "1":
                count += 1
            if symbol == "c" and count > 0:  # count all ones until a spacer "c" is reached
                output_word.append(inverse_encoding[count])
                count = 0
        return ["#"] + output_word

    def decode_tape_as_binary_tm(self):
        """Decodes the Turing tape's data section to the corresponding two tag system word, which in turn is
        decoded into a binary Turing machine's tape, in case the two tag system was based on a binary TM."""

        assert self.from_two_tag_system and self.from_binary_turing_machine

        two_tag_word = self.decode_tape_as_two_tag_word()
        left = []
        right = []
        print(two_tag_word)
        for symbol in two_tag_word:
            if symbol == "x":
                continue
            if right or symbol == "B_#":  # once we started filling the right side, continue to do so
                right.append(symbol)
            else:
                left.append(symbol)  # fill left side first
        print(left + right)
        assert right[0] == "B_#"
        right = right[1:]

        # count side lengths and convert to binary.
        m = len(left)
        n = len(right)
        left_str = bin(m)[2:]
        right_str = bin(n)[2:] if n > 0 else ""
        right_str = "".join((reversed(right_str)))
        return left_str + right_str

    def get_tape(self):
        """Return UTM's tape"""
        return self._tm.definition.tape

    def run(self, line_break=False, write_to_file=False, brief=False):
        """Run the UTM until it finishes.
        Arguments:
            line_break:     todo: check if still needed
            write_to_file:  Write the output to a log file instead of printing it
            brief:          only provide brief output."""
        if write_to_file:
            # write symbol encodings
            with open("symbol_encodings.txt", "w") as fid:
                max_len = max([len(s) for s in self.symbol_encodings.keys()])
                for key, encoding in self.symbol_encodings.items():
                    left = str(key) + ": "
                    left = left.ljust(max_len + 3)
                    fid.write("{left}{encoding}\n".format(left=left, encoding=encoding))

        self._tm.run(line_break=line_break, write_to_file=write_to_file, brief=brief)

        if self.from_two_tag_system:
            print()
            print("Output:")
            print(self.decode_tape_as_two_tag_word())
            if self.from_binary_turing_machine:
                print(self.decode_tape_as_binary_tm())
