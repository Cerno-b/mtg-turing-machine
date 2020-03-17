import sys
import re
import math


def _strip_list(input_list, item):
    """Strip all occurrences of an item from the beginning and end of a list"""
    while True:
        if input_list:
            if input_list[0] == item:
                input_list = input_list[1:]
            else:
                break
        else:
            break
    while True:
        if input_list:
            if input_list[-1] == item:
                input_list = input_list[0:-1]
            else:
                break
        else:
            break
    return input_list


def _to_binary(number, bit_depth):
    """Convert a number to its binary representation with fixed bit depth"""
    binary = str(bin(number))[2:]
    while len(binary) < bit_depth:
        binary = "0" + binary
    return binary


class TuringDefinition:
    """Definition of a Turing Machine"""

    def __init__(self, transitions, initial_state, stop_states, tape=None, tape_index=0, blank=" "):
        """
        Arguments:
            transitions:        The transition function as dictionary in the form
                                    {(source_state, read_symbol): (target_state, write_symbol, head_direction)}
                                    head_direction can be '<', '-', '>'
            initial_state:      The Turing machine's initial state (string)
            stop_states:        A list of states to halt the machine when reached (list of string)
            tape:               A pre-filled Turing tape (list of strings or single string)
                                    list input supports multiple character symbols
                                    string input requires single-character symbols
            tape_index:         The head position where the Turing machine should start
            blank:              The blank symbol"""

        self.transitions = transitions
        self.initial_state = initial_state
        self.stop_states = stop_states
        if tape:
            self.tape = list(tape)
        else:
            self.tape = [blank]
        self.tape_index = tape_index
        self.blank = blank

        # store length of the longest symbol (for multi-character symbols), for output formatting
        alphabet = [symbol for _, symbol in transitions.keys()]
        alphabet_lengths = [len(a) for a in alphabet]
        self.max_symbol_length = max(alphabet_lengths)


class TuringMachine:
    """Turing machine main class.
    Allows converting to binary Turing machine that only contains two symbols, including the blank.

    Attributes:
        prev_out_string:
        has_been_binarized:         Flag that tracks whether the machine has been binarized
                                        This is not the same as having a binary TM. If the original TM was binary
                                        to begin with, binarization will be skipped and the flag will be False
        binarized_bit_depth:        Binarization requires fixed bit_depth to encode the original machine's alphabet
        binarized_symbol_lookup:    Look up table for converting the original machine's alphabet to binary and back
        pre_binarize_blank:         The original machine's blank symbol (the binary machine uses 0 as blank)
        definition:                 The machine's definition
        current_state:              The machine's current state
        steps:                      The number of steps the machine has taken so far
        """

    def __init__(self, definition):
        """
        Arguments:
            definition: Turing machine definition (TuringDefinition or string)
                            if definition is a string, it will be interpreted as an input path
        """
        self.prev_out_string = ""
        self.has_been_binarized = False
        self.binarized_bit_depth = None
        self.binarized_symbol_lookup = None
        self.pre_binarize_blank = None

        if isinstance(definition, TuringDefinition):
            self.definition = definition
        elif isinstance(definition, str):
            self.definition = self.read_definition_from_path(definition)
        else:
            assert False

        self.current_state = self.definition.initial_state
        self.steps = 0

        # run a check to see if the Turing machine is valid
        self.sanity_check()

    def sanity_check(self):
        """Run some checks on the machine"""
        assert 0 <= self.definition.tape_index < len(self.definition.tape)
        for (_, _), (_, _, head_dir) in self.definition.transitions.items():
            assert head_dir in ["<", "-", ">"]

    @staticmethod
    def read_definition_from_path(path):
        """Read a Turing machine definition from a text file configuration. See rogozhin.txt for a format example.
        The format is roughly based on the one used in https://turingmachinesimulator.com/ so the file can be adapted
        to run a simulation there. It differs from the format used in this class.

        The main differences:
            The order of the transition function elements is
                (source state, read, write, head direction, target state).
            The blank symbol is '_' by default and will be internally converted to a ' '.
                If a different blank shall be used, it needs to be set manually after calling this function.
            The head directions are defined as 'L', 'R' and '-', which will be converted to '<', '>' and '-'."""
        transitions = {}
        initial_state = None
        stop_states = ["-"]

        with open(path, 'r') as fid:
            first_line = True
            for line in fid.readlines():
                line = re.sub(r"#.*", "", line)  # remove comments
                line = line.strip()
                if line:
                    source_state, read_symbol, write_symbol, head_dir, target_state = line.split("\t")

                    if first_line:
                        # the first line defines the initial state
                        assert initial_state is None
                        initial_state = source_state
                        first_line = False
                    if read_symbol == "_":
                        read_symbol = " "
                    if write_symbol == "_":
                        write_symbol = " "
                    if head_dir == "L":
                        head_dir = "<"
                    elif head_dir == "R":
                        head_dir = ">"
                    elif head_dir == "-":
                        pass
                    else:
                        sys.exit("Error reading definition file: invalid head symbol: " + head_dir)

                    transitions[(source_state, read_symbol)] = (target_state, write_symbol, head_dir)
        definition = TuringDefinition(transitions, initial_state, stop_states)
        return definition

    def convert_to_two_symbol(self):
        """Convert the Turing machine to a binary Turing machine with only two symbols.
        This is done by encoding each symbol in binary using a fixed-width encoding.
        This is necessary as the resulting TM will not be able to distinguish between a meaningful blank
        and one of the infinite blanks at the start and end of the tape. So instead, each transition of
        the original TM will be converted to a set of transitions that reads and writes one
        fixed-length encoded block and then moves the head to the next or previous block."""
        # collect all symbols in the transitions (left and right side)
        alphabet = [symbol for _, symbol in self.definition.transitions.keys()]
        alphabet += [symbol for _, symbol, _ in self.definition.transitions.values()]
        alphabet = sorted(set(alphabet))
        alphabet.remove(self.definition.blank)
        alphabet = [self.definition.blank] + alphabet  # make sure that the blank has the index 0 (encoded as 000...0)

        if len(alphabet) == 2:
            print("Conversion to 2-symbol TM skipped: Was already 2-symbol")
            return

        symbol_to_idx_lookup = {symbol: i for i, symbol in enumerate(alphabet)}  # give each symbol a unique number
        alphabet_size = len(alphabet)
        bit_depth = int(math.ceil(math.log(alphabet_size)/math.log(2)))

        new_transitions = {}
        new_stop_states = []

        original_states = sorted(set(state for state, _ in self.definition.transitions.keys()))  # list of states

        # for each source state of the original Turing machine (left side of the transition)
        for original_source_state in original_states:
            source_id = 0
            target_id = 1

            # the binary TM needs this many transitions to encode a single transition of the original TM
            binary_read_transition_count = 2 ** (bit_depth+1) - 2

            # encode reading operation
            for _ in range(binary_read_transition_count//2):  # divide by 2. We handle reading 0 and 1 in one iteration

                # generate two transitions for reading each bit of the current origin state

                binary_source_state = original_source_state + "_" + str(source_id)
                binary_target_state = original_source_state + "_" + str(target_id)
                new_transitions[(binary_source_state, "0")] = (binary_target_state, "0", ">")

                target_id += 1

                binary_source_state = original_source_state + "_" + str(source_id)
                binary_target_state = original_source_state + "_" + str(target_id)
                new_transitions[(binary_source_state, "1")] = (binary_target_state, "1", ">")

                target_id += 1
                source_id += 1

            # encode write, move and state change for each read result

            # for each symbol that exists on the left side of a transition
            for symbol_idx, symbol in enumerate(alphabet):
                transition_left_side = (original_source_state, symbol)
                if transition_left_side in self.definition.transitions:

                    transition_right_side = self.definition.transitions[transition_left_side]
                    original_target_state, original_target_symbol, direction = transition_right_side

                    # convert original TM symbol to binary
                    original_target_symbol_idx = symbol_to_idx_lookup[original_target_symbol]
                    original_target_symbol_idx_binary = _to_binary(original_target_symbol_idx, bit_depth)

                    # after reading a binary encoded symbol, we need to backtrack to the beginning of the binary symbol
                    symbol_encoding = 2 ** bit_depth - 2 + symbol_idx + 1  # offset +1 from the initial state
                    source_id = symbol_encoding

                    # for each bit, move the head left without changing anything (backtrack after reading)
                    for _ in range(bit_depth):
                        binary_source_state = original_source_state + "_" + str(source_id)
                        binary_target_state = original_source_state + "_" + str(target_id)
                        new_transitions[(binary_source_state, "0")] = (binary_target_state, "0", "<")
                        new_transitions[(binary_source_state, "1")] = (binary_target_state, "1", "<")
                        source_id = target_id
                        target_id += 1

                    # write each bit of the target symbol (encode writing operation)
                    for i in range(bit_depth):
                        write_symbol = original_target_symbol_idx_binary[i]
                        binary_source_state = original_source_state + "_" + str(source_id)
                        binary_target_state = original_source_state + "_" + str(target_id)
                        new_transitions[(binary_source_state, "0")] = (binary_target_state, write_symbol, ">")
                        new_transitions[(binary_source_state, "1")] = (binary_target_state, write_symbol, ">")
                        source_id = target_id
                        target_id += 1

                    # for each bit, move the head left without changing anything (backtrack after writing)
                    for _ in range(bit_depth):
                        binary_source_state = original_source_state + "_" + str(source_id)
                        binary_target_state = original_source_state + "_" + str(target_id)
                        new_transitions[(binary_source_state, "0")] = (binary_target_state, "0", "<")
                        new_transitions[(binary_source_state, "1")] = (binary_target_state, "1", "<")
                        source_id = target_id
                        target_id += 1

                    # for each bit, move the head left or right without changing anything (encode head movement)
                    for _ in range(bit_depth-1):  # end one early to allow special transition of final state
                        binary_source_state = original_source_state + "_" + str(source_id)
                        binary_target_state = original_source_state + "_" + str(target_id)
                        new_transitions[(binary_source_state, "0")] = (binary_target_state, "0", direction)
                        new_transitions[(binary_source_state, "1")] = (binary_target_state, "1", direction)
                        source_id = target_id
                        target_id += 1

                    # move by the missing bit without changing anything (encode the state change)
                    binary_target_state = original_target_state + "_" + str(0)
                    if original_target_state in self.definition.stop_states:
                        new_stop_states.append(binary_target_state)
                    binary_source_state = original_source_state + "_" + str(source_id)
                    new_transitions[(binary_source_state, "0")] = (binary_target_state, "0", direction)
                    new_transitions[(binary_source_state, "1")] = (binary_target_state, "1", direction)

        # encode the tape to binary
        new_tape = ""
        for symbol in self.definition.tape:
            new_tape += _to_binary(symbol_to_idx_lookup[symbol], bit_depth)
        new_tape = list(new_tape)
        tape_index = self.definition.tape_index * bit_depth

        # overwrite members, the old definition will be lost
        self.has_been_binarized = True
        self.binarized_bit_depth = bit_depth
        self.binarized_symbol_lookup = alphabet
        self.pre_binarize_blank = self.definition.blank

        self.definition.transitions = new_transitions
        self.definition.stop_states = new_stop_states
        self.definition.tape_index = tape_index
        self.definition.tape = new_tape
        self.definition.blank = "0"
        self.definition.initial_state = self.definition.initial_state + "_" + str(0)
        self.current_state = self.definition.initial_state

    def set_tape_string(self, string):
        """Set the Turing machine's tape. Only possible if the machine has not been binarized yet.
        Arguments:
            string: The tape in the form of a string. May contain a caret (^) that indicates the head position.
            The head will be right to the caret. After setting the tape, the caret will be removed."""
        if "^" in string:
            self.definition.tape_index = string.find("^")
            if string == "^":
                self.definition.tape = [self.definition.blank]
            else:
                self.definition.tape = list(string.replace("^", ""))
        else:
            self.definition.tape_index = 0
            if string:
                self.definition.tape = list(string)
            else:
                self.definition.tape = [self.definition.blank]

    def get_stripped_tape(self, decode_binarized=False):
        """Return a version of the tape that has been stripped of leading and trailing blanks"""
        if decode_binarized:
            tape = self.decode_binarized_tape()
            blank = self.pre_binarize_blank
        else:
            tape = self.definition.tape
            blank = self.definition.blank
        return _strip_list(tape, blank)

    def step(self):
        """Execute a single step of the Turing machine.
        Returns True if the machine stops after this step, and False if it needs to continue"""

        if self.current_state in self.definition.stop_states:
            return True

        # add a blank if the end is reached
        if self.definition.tape_index == len(self.definition.tape):
            self.definition.tape += [self.definition.blank]

        read_symbol = self.definition.tape[self.definition.tape_index]
        if not (self.current_state, read_symbol) in self.definition.transitions:
            sys.exit("Invalid input: (state={state}, symbol={symbol})".format(state=self.current_state,
                                                                              symbol=read_symbol))

        # write to tape and change state
        new_state, write_symbol, direction = self.definition.transitions[(self.current_state, read_symbol)]
        self.current_state = new_state
        self.definition.tape[self.definition.tape_index] = write_symbol

        # move head
        if direction == "<":
            self.definition.tape_index -= 1
        elif direction == ">":
            self.definition.tape_index += 1
        else:
            assert direction == "-"  # no head movement

        # add a blank if the beginning or end is reached
        if self.definition.tape_index == -1:
            self.definition.tape = [self.definition.blank] + self.definition.tape
            self.definition.tape_index = 0
        elif self.definition.tape_index == len(self.definition.tape):
            self.definition.tape += [self.definition.blank]

        assert 0 <= self.definition.tape_index < len(self.definition.tape)
        self.steps += 1

        return False

    def print_summary(self):
        """Print a summary of the Turing machine."""
        states = set()
        for left_side, right_side in self.definition.transitions.items():
            states.add(left_side[0])
            states.add(right_side[0])

        alphabet = sorted(set([symbol for _, symbol in self.definition.transitions.keys()]))

        print("Turing Machine")
        print("--------------")
        print("Alphabet: {}".format(" ".join(alphabet)))
        print("Blank: {}".format(self.definition.blank))
        print("States: {}".format(" ".join(sorted(states))))
        print("Transitions:")
        for left_side, right_side in sorted(self.definition.transitions.items()):
            print("  ({}) -> ({})".format(" ".join(left_side), " ".join(right_side)))
        print("Tape: {}".format(" ".join(self.definition.tape)))

    def print(self, line_break=False, fid=None):
        """Print the current state of the machine, including the contents of its tape"""
        # TODO This needs to get cleaned up!
        variant = 1

        if variant == 1:
            cur_symbol = ""
            count = 0
            out_string = ""
            for symbol in reversed(self.definition.tape):
                if not cur_symbol:
                    cur_symbol = symbol
                if symbol != cur_symbol:
                    out_string = "{entry: >7}".format(entry=cur_symbol + "^" + str(count) + ",") + out_string
                    if "b" in cur_symbol:
                        break
                    # if fid:
                    #     fid.write("{count} {symbol}, ".format(count=count, symbol=cur_symbol))
                    # else:
                    #     print("{count} {symbol}, ".format(count=count, symbol=cur_symbol), end="")
                    cur_symbol = symbol
                    count = 1
                else:
                    count += 1
            # if "b" in cur_symbol:
            #     out_string = "{entry: >7}".format(entry=cur_symbol + "^" + str(count) + ",") + out_string
            if self.prev_out_string != out_string:
                if fid:
                    fid.write(out_string + "\n")
                else:
                    print(out_string)
            self.prev_out_string = out_string
        else:
            if not line_break:
                print("\r", end="")
            for i, symbol in enumerate(self.definition.tape):
                symbol += " "*(self.definition.max_symbol_length-len(symbol))
                if i == self.definition.tape_index:
                    if fid:
                        fid.write("[{symbol}]".format(symbol=symbol))
                    else:
                        print("[{symbol}]".format(symbol=symbol), end="")
                else:
                    if fid:
                        fid.write(" {symbol} ".format(symbol=symbol))
                    else:
                        print(" {symbol} ".format(symbol=symbol), end="")
            if line_break:
                print("   state: {state}, steps: {steps}".format(state=self.current_state, steps=self.steps),
                      flush=True)
            else:
                print("   state: {state}, steps: {steps}".format(state=self.current_state, steps=self.steps),
                      flush=True, end="" * 100)
            if fid:
                fid.write("\n")
            # time.sleep(0.1)

    def decode_binarized_tape(self):
        """Decodes the binarized tape back to the original alphabet"""
        assert self.has_been_binarized

        output = []
        tape_string = "".join(self.definition.tape)
        tape_index = self.definition.tape_index

        # fill the beginning and end of the tape with 0 to align the bit fields
        while tape_index % self.binarized_bit_depth != 0:
            tape_string = "0" + tape_string
            tape_index += 1
        while len(tape_string) % self.binarized_bit_depth != 0:
            tape_string += "0"

        # convert each bit field to its corresponding original TM symbol
        while len(tape_string) >= self.binarized_bit_depth:
            symbol = tape_string[0:self.binarized_bit_depth]
            tape_string = tape_string[self.binarized_bit_depth:]
            symbol_idx = int(symbol, 2)
            output.append(self.binarized_symbol_lookup[symbol_idx])
        return output

    def run(self, line_break=False, write_to_file=False, brief=False):
        """Run the Turing machine until it stops.
        Arguments:
            write_to_file:  Write the output to a log file instead of printing it
            brief:          Flag to indicate that output should be written in condensed form each 100.000 iterations"""
        # TODO: Needs to be refactored
        fid = None
        if write_to_file:
            fid = open("tm_log.txt", "w")
        while True:
            if brief:
                if self.steps % 100000 == 0:
                    print("steps: {}".format(self.steps))
            else:
                self.print(line_break=line_break, fid=fid)
            stopped = self.step()
            if stopped:
                if brief:
                    self.print(line_break=line_break, fid=fid)
                print("{} steps taken".format(self.steps))
                break
        if write_to_file:
            fid.close()
        print("\nDone.")
