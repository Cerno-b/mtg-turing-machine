from turing_machine import TuringMachine, TuringDefinition


def get_alphabet(transitions):
    alphabet = [symbol for (_, symbol) in transitions.keys()]
    alphabet = set(alphabet)
    return alphabet


def convert_tm_to_instantaneous_tm(turing_machine):
    assert turing_machine.tape_index == 0
    initial = turing_machine.initial_state
    inst_initial = initial + "_inst_0"
    transitions = [
        (inst_initial, "0", ">", initial + "_0", initial + "_1")
    ]
    for (src_state, read), (tgt_state, write, move) in turing_machine.transitions.items():
        inst_state = src_state + "_" + read
        inst_write = write
        inst_move = move
        if tgt_state in turing_machine.stop_states:
            inst_change_0 = tgt_state
            inst_change_1 = tgt_state
        else:
            inst_change_0 = tgt_state + "_0"
            inst_change_1 = tgt_state + "_1"
        transitions.append((inst_state, inst_write, inst_move, inst_change_0, inst_change_1))

    state_dict = {}
    for s in turing_machine.stop_states:
        state_dict[s] = -1
    counter = 0
    new_transitions = []
    for inst_state, inst_write, inst_move, tgt_state_0, tgt_state_1 in transitions:
        if inst_state not in state_dict:
            state_dict[inst_state] = counter
            counter += 1
        if tgt_state_0 not in state_dict:
            state_dict[tgt_state_0] = counter
            counter += 1
        if tgt_state_1 not in state_dict:
            state_dict[tgt_state_1] = counter
            counter += 1
        new_state_id = state_dict[inst_state]
        new_tgt_state_0_id = state_dict[tgt_state_0]
        new_tgt_state_1_id = state_dict[tgt_state_1]
        new_transitions.append((new_state_id, inst_write, inst_move, new_tgt_state_0_id, new_tgt_state_1_id))
    transitions = new_transitions

    tape_q = state_dict[inst_initial]
    tape_m = 0
    tape_n = 0
    for i, cell in enumerate(turing_machine.tape):
        tape_n += int(cell) * 2**i
    inst_tape = (tape_q, tape_m, tape_n)
    return transitions, inst_tape


def set_direction(string, direction):
    if direction == "<":
        if "A" in string or "a" in string:
            string = string.replace("A", "B")
            string = string.replace("a", "b")
        elif "B" in string or "b" in string:
            string = string.replace("B", "A")
            string = string.replace("b", "a")
    return string


def encode_transition_as_2tag(transition):
    state_id, inst_write, inst_move, inst_change_0_id, inst_change_1_id = transition
    if inst_change_0_id < 0:
        inst_change_0_id = "#"  # set stop symbol
    if inst_change_1_id < 0:
        inst_change_1_id = "#"
    assert inst_write in ("0", "1")
    assert inst_move in ("<", ">")

    if inst_move == ">":
        enc_transitions = {
            "A$": ["C$", "x$"] if inst_write == "0" else ["C$", "x$", "c$", "x$"],
            "a$": ["c$", "x$", "c$", "x$"],
            "B$": ["S$"],
            "b$": ["s$"],
            "C$": ["D$_1",  "D$_0"],
            "c$": ["d$_1",  "d$_0"],
            "S$": ["T$_1",  "T$_0"],
            "s$": ["t$_1",  "t$_0"],
            "D$_1": ["A!1", "x!1"],
            "d$_1": ["a!1", "x!1"],
            "T$_1": ["B!1", "x!1"],
            "t$_1": ["b!1", "x!1"],
            "D$_0": ["x!0", "A!0", "x!0"],
            "d$_0": ["a!0", "x!0"],
            "T$_0": ["B!0", "x!0"],
            "t$_0": ["b!0", "x!0"]
        }
    elif inst_move == "<":
        enc_transitions = {
            # switch A and B (is now called Z)
            "A$": ["Z$", "x$"],
            "a$": ["z$", "x$"],
            # Z (formerly A) now takes the role of B
            "Z$": ["S$"],
            "z$": ["s$"],
            # B takes the role of (formerly) A
            "B$": ["C$", "x$"] if inst_write == "0" else ["C$", "x$", "c$", "x$"],
            "b$": ["c$", "x$", "c$", "x$"],
            "C$": ["D$_1", "D$_0"],
            "c$": ["d$_1", "d$_0"],
            "S$": ["T$_1", "T$_0"],
            "s$": ["t$_1", "t$_0"],

            "D$_1": ["Y$_1", "x$"],
            "d$_1": ["y$_1", "x$"],
            "T$_1": ["A!1", "x!1"],
            "t$_1": ["a!1", "x!1"],
            "D$_0": ["x!0", "Y$_0", "x$"],
            "d$_0": ["y$_0", "x$"],
            "T$_0": ["A!0", "x!0"],
            "t$_0": ["a!0", "x!0"],

            "Y$_0": ["B!0", "x!0"],
            "y$_0": ["b!0", "x!0"],
            "Y$_1": ["B!1", "x!1"],
            "y$_1": ["b!1", "x!1"]
        }
    else:
        assert False

    new_enc_transitions = {}
    for source, targets in enc_transitions.items():
        # source = set_direction(source, inst_move)
        source = source.replace("$", "_" + str(state_id))
        new_targets = []
        for target in targets:
            if ("!0" in target and inst_change_0_id == "#") or ("!1" in target and inst_change_1_id == "#"):
                target = "#"
            else:
                # target = set_direction(target, inst_move)
                target = target.replace("$", "_" + str(state_id))
                target = target.replace("!0", "_" + str(inst_change_0_id))
                target = target.replace("!1", "_" + str(inst_change_1_id))
            new_targets.append(target)
        new_enc_transitions[source] = new_targets

    return new_enc_transitions


def encode_instantaneous_tm_as_2tag(transitions, tape):
    tape_q, tape_m, tape_n = tape
    enc_tape_str = "Ax" + "ax"*tape_m + "Bx" + "bx"*tape_n
    enc_tape = []
    for symbol in enc_tape_str:
        enc_tape.append(symbol + "_0")

    enc_transitions = {}

    for transition in transitions:
        new_transitions = encode_transition_as_2tag(transition)
        for key, value in new_transitions.items():
            assert key not in enc_transitions
            enc_transitions[key] = value

    return enc_transitions, enc_tape


def encode_tm_to_2tag(turing_machine):
    assert isinstance(turing_machine, TuringMachine)
    assert turing_machine.blank == '0'
    assert get_alphabet(turing_machine.transitions) == {'0', '1'}
    transitions, tape = convert_tm_to_instantaneous_tm(turing_machine)
    transitions, tape = encode_instantaneous_tm_as_2tag(transitions, tape)
    return transitions, tape


class TwoTagSystem:
    def __init__(self, data):
        if isinstance(data, TuringMachine):
            self.transitions, self.state = encode_tm_to_2tag(data)
            self.halt_symbol = "#"
            self.step_number = 0
        else:
            self.transitions = data
            self.state = ""
            self.halt_symbol = ""
            self.step_number = 0
        self.prev = None

    def set_input_string(self, state, halt_symbol):
        self.step_number = 0
        self.state = state
        self.halt_symbol = halt_symbol

    def step(self):
        first = self.state[0]
        self.state = self.state[2:] + self.transitions[first]
        self.step_number += 1

    def print(self):
        first = self.state[0]
        if self.prev != first:
            print("step {step}: {state}".format(step=self.step_number, state=self.state))
            print(first, " -> ", self.transitions[first])
            self.prev = first

    def run(self):
        print("Initial state:", self.state)
        first = self.state[0]
        print(first, " -> ", self.transitions[first])
        while True:
            self.step()
            if self.state[0] == self.halt_symbol:
                break
            self.print()
