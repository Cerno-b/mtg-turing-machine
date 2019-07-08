import sys
import re
import time

from encode_2tag import encode_2tag_to_utm


class TuringMachine:
    def __init__(self, transitions, initial_state, stop_states, tape=None, tape_index=0):
        self.transitions = transitions
        if tape is None:
            self.tape = [" "]
        else:
            self.tape = list(tape)
        self.tape_index = tape_index
        self.current_state = initial_state
        self.stop_states = stop_states
        self.blank = " "
        self.steps = 0

        self.test()
        
    def test(self):
        assert 0 <= self.tape_index < len(self.tape)
        for (_, _), (_, _, head_dir) in self.transitions.items():
            assert head_dir in ["<", "-", ">"]

    def set_tape_string(self, string):
        self.tape_index = string.find("^")
        self.tape = list(string.replace("^", ""))

    def execute(self):
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
        if linebreak:
            print("\r", end="")
        for i, symbol in enumerate(self.tape):
            if i == self.tape_index:
                print("[", end="")
            else:
                print(" ", end="")
            print(symbol, end="")
            if i == self.tape_index:
                print("]", end="")
            else:
                print(" ", end="")
        if linebreak:
            print("   state: {state}, steps: {steps}".format(state=self.current_state, steps=self.steps), flush=True)
        else:
            print("   state: {state}, steps: {steps}".format(state=self.current_state, steps=self.steps), flush=True, end="" * 100)
        # time.sleep(0.1)

    def run(self, linebreak=False):
        while True:
            self.print(linebreak)
            stopped = self.execute()
            if stopped:
                break
        print("\nDone.")


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

    return TuringMachine(transitions, initial_state, stop_states, tape, tape_index)


def load_tm_from_file(path):
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
    return TuringMachine(transitions, initial_state, stop_states, tape, tape_index)


def load_tm_utm():
    return load_tm_from_file("rogozhin_enc.txt")


def main():
    turing_machine = load_tm_utm()
    # turing_machine.set_tape_string("ttbb1111111bb11b111111b1111111bb^1c1c")
    # turing_machine.set_tape_string("ttbb1bb^1c1c1c1c1c1c1c1c1c1c111c")

    alphabet = ["X", "#"]
    transitions = {
        "X": "X"}

    input_str = "XXXXXXXXXX#"

    tape = encode_2tag_to_utm(alphabet, transitions, input_str)
    turing_machine.set_tape_string(tape)

    turing_machine.run(True)


if __name__ == '__main__':
    main()
