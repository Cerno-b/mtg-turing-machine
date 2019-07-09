import sys
import re
import time


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
            print("   state: {state}, steps: {steps}".format(state=self.current_state, steps=self.steps), flush=True,
                  end="" * 100)
        # time.sleep(0.1)

    def run(self, linebreak=False):
        while True:
            self.print(linebreak)
            stopped = self.step()
            if stopped:
                break
        print("\nDone.")
