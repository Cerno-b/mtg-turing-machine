import sys
import re
import math


def _to_binary(number, bit_depth):
    binary = str(bin(number))[2:]
    while len(binary) < bit_depth:
        binary = "0" + binary
    return binary


def cat_ids(id1, id2):
    return str(id1) + "_" + str(id2)


class TuringDefinition:
    def __init__(self, transitions, initial_state, stop_states, tape=None, tape_index=0, blank=" "):
        self.transitions = transitions
        self.initial_state = initial_state
        self.stop_states = stop_states
        self.tape = tape
        self.tape_index = tape_index
        self.blank = blank


class TuringMachine:
    def __init__(self, data):
        self.is_binarized_tm = False
        self.binarized_bit_depth = None
        self.binarized_symbol_lookup = None
        if isinstance(data, TuringDefinition):
            self.transitions = data.transitions
            if data.tape is None:
                self.tape = [" "]
            else:
                self.tape = list(data.tape)
            self.tape_index = data.tape_index
            self.initial_state = data.initial_state
            self.current_state = data.initial_state
            self.stop_states = data.stop_states
            self.blank = data.blank
            self.steps = 0
            alphabet = [symbol for _, symbol in data.transitions.keys()]
            alphabet_lengths = [len(a) for a in alphabet]
            self.max_symbol_length = max(alphabet_lengths)
            self.test()
        elif isinstance(data, str):
            self.setup_from_path(data)
        else:
            assert False

    def setup_from_path(self, path):
        transitions = {}
        tape = [" "]
        tape_index = 0
        initial_state = ""
        stop_states = ["-"]

        with open(path, 'r') as fid:
            first_line = True
            for line in fid.readlines():
                line = re.sub(r"#.*", "", line)
                line = line.strip()
                if line:
                    old_state, old_symbol, new_symbol, head_dir, new_state = line.split("\t")
                    if first_line:
                        initial_state = old_state
                        first_line = False
                    if old_symbol == "_":
                        old_symbol = " "
                    if new_symbol == "_":
                        new_symbol = " "
                    if head_dir == "L":
                        head_dir = "<"
                    elif head_dir == "R":
                        head_dir = ">"
                    elif head_dir == "-":
                        pass
                    else:
                        sys.exit("Error: invalid head symbol: " + head_dir)

                    transitions[(old_state, old_symbol)] = (new_state, new_symbol, head_dir)
        definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index)
        return self.__init__(definition)

    def convert_to_two_symbol(self):
        alphabet = [symbol for _, symbol in self.transitions.keys()]
        alphabet += [symbol for _, symbol, _ in self.transitions.values()]
        alphabet = sorted(set(alphabet))
        alphabet.remove(self.blank)
        alphabet = [self.blank] + alphabet  # make sure that the blank has the index 0 (encoded 000...0)
        inverse_alphabet = {symbol: i for i, symbol in enumerate(alphabet)}
        alphabet_size = len(alphabet)
        bit_depth = int(math.ceil(math.log(alphabet_size)/math.log(2)))

        self.is_binarized_tm = True
        self.binarized_bit_depth = bit_depth
        self.binarized_symbol_lookup = alphabet

        new_transitions = {}
        new_stop_states = []
        # encode reading
        origin_source_states = sorted(set(state for state, _ in self.transitions.keys()))
        for oss in origin_source_states:
            current_source_id = 0
            current_target_id = 1
            read_transition_count = 2**(bit_depth+1)-2
            for i in range(read_transition_count//2):  # divide by 2 since we handle the 0 and 1 case in one iteration
                new_transitions[(cat_ids(oss, current_source_id), "0")] = (cat_ids(oss, current_target_id), "0", ">")
                current_target_id += 1
                new_transitions[(cat_ids(oss, current_source_id), "1")] = (cat_ids(oss, current_target_id), "1", ">")
                current_target_id += 1
                current_source_id += 1
            # encode write, move and state change for each read result
            for i in range(alphabet_size):
                if (oss, alphabet[i]) in self.transitions:
                    origin_target_state, origin_target_symbol, origin_target_dir = self.transitions[(oss, alphabet[i])]
                    origin_target_symbol_id = inverse_alphabet[origin_target_symbol]
                    origin_target_symbol_id_binary = _to_binary(origin_target_symbol_id, bit_depth)
                    # encode backtrack after reading
                    symbol_encoding = 2 ** bit_depth - 2 + i + 1  # offset +1 from the initial state
                    current_source_id = symbol_encoding
                    for j in range(bit_depth):
                        new_transitions[(cat_ids(oss, current_source_id), "0")] = (cat_ids(oss, current_target_id), "0", "<")
                        new_transitions[(cat_ids(oss, current_source_id), "1")] = (cat_ids(oss, current_target_id), "1", "<")
                        current_source_id = current_target_id
                        current_target_id += 1
                    # encode writing
                    for j in range(bit_depth):
                        write_symbol = origin_target_symbol_id_binary[j]
                        new_transitions[(cat_ids(oss, current_source_id), "0")] = (cat_ids(oss, current_target_id), write_symbol, ">")
                        new_transitions[(cat_ids(oss, current_source_id), "1")] = (cat_ids(oss, current_target_id), write_symbol, ">")
                        current_source_id = current_target_id
                        current_target_id += 1
                    # encode backtrack after writing
                    for j in range(bit_depth):
                        new_transitions[(cat_ids(oss, current_source_id), "0")] = (cat_ids(oss, current_target_id), "0", "<")
                        new_transitions[(cat_ids(oss, current_source_id), "1")] = (cat_ids(oss, current_target_id), "1", "<")
                        current_source_id = current_target_id
                        current_target_id += 1
                    # encode head movement
                    direction = origin_target_dir
                    for j in range(bit_depth-1):  # end one early to allow special transition of final state
                        new_transitions[(cat_ids(oss, current_source_id), "0")] = (cat_ids(oss, current_target_id), "0", direction)
                        new_transitions[(cat_ids(oss, current_source_id), "1")] = (cat_ids(oss, current_target_id), "1", direction)
                        current_source_id = current_target_id
                        current_target_id += 1
                    # encode state change
                    ots = origin_target_state
                    new_target_state = cat_ids(ots, 0)
                    if ots in self.stop_states:
                        new_stop_states.append(new_target_state)
                    new_transitions[(cat_ids(oss, current_source_id), "0")] = (new_target_state, "0", direction)
                    new_transitions[(cat_ids(oss, current_source_id), "1")] = (new_target_state, "1", direction)

        new_tape = ""
        for symbol in self.tape:
            new_tape += _to_binary(inverse_alphabet[symbol], bit_depth)
        new_tape = list(new_tape)

        self.transitions = new_transitions
        self.stop_states = new_stop_states
        self.tape_index = 0
        self.tape = new_tape
        self.initial_state = cat_ids(self.initial_state, 0)
        self.current_state = self.initial_state
        self.blank = "0"

    def test(self):
        assert 0 <= self.tape_index < len(self.tape)
        for (_, _), (_, _, head_dir) in self.transitions.items():
            assert head_dir in ["<", "-", ">"]

    def set_tape_string(self, string):
        self.tape_index = string.find("^")
        self.tape = list(string.replace("^", ""))

    def step(self):
        if self.current_state in self.stop_states:
            return True

        in_symbol = self.tape[self.tape_index]
        if not (self.current_state, in_symbol) in self.transitions:
            sys.exit("Invalid input: (state={state}, symbol={symbol})".format(state=self.current_state,
                                                                              symbol=in_symbol))
        out_state, out_symbol, head_dir = self.transitions[(self.current_state, in_symbol)]
        self.current_state = out_state
        self.tape[self.tape_index] = out_symbol

        if head_dir == "<":
            self.tape_index -= 1
        elif head_dir == ">":
            self.tape_index += 1
        else:
            assert head_dir == "-"

        if self.tape_index == -1:
            self.tape = [self.blank] + self.tape
            self.tape_index = 0
        elif self.tape_index == len(self.tape):
            self.tape += [self.blank]

        assert 0 <= self.tape_index < len(self.tape)
        self.steps += 1

        return False

    def print(self, linebreak=False):
        if not linebreak:
            print("\r", end="")
        for i, symbol in enumerate(self.tape):
            symbol += " "*(self.max_symbol_length-len(symbol))
            if i == self.tape_index:
                print("[{symbol}]".format(symbol=symbol), end="")
            else:
                print(" {symbol} ".format(symbol=symbol), end="")
        if linebreak:
            print("   state: {state}, steps: {steps}".format(state=self.current_state, steps=self.steps), flush=True)
        else:
            print("   state: {state}, steps: {steps}".format(state=self.current_state, steps=self.steps), flush=True,
                  end="" * 100)
        # time.sleep(0.1)

    def decode_binarized_tape(self):
        assert self.is_binarized_tm
        output = []
        tape_string = "".join(self.tape)
        while len(tape_string) >= self.binarized_bit_depth:
            word = tape_string[0:self.binarized_bit_depth]
            tape_string = tape_string[self.binarized_bit_depth:]
            word_id = int(word, 2)
            output.append(self.binarized_symbol_lookup[word_id])
        return output

    def run(self, linebreak=False):
        while True:
            self.print(linebreak)
            stopped = self.step()
            if stopped:
                break
        print("\nDone.")
