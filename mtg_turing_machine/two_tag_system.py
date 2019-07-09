from turing_machine import TuringMachine, TuringDefinition


def get_alphabet(transitions):
    alphabet = [symbol for (_, symbol) in transitions.keys()]
    alphabet = set(alphabet)
    return alphabet


def convert_tm_to_instantaneous_tm(turing_machine):
    assert turing_machine.tape_index == 0
    initial = turing_machine.initial_state
    inst_initial = initial + "_inst_0"
    transitions = {
        inst_initial: ("0", ">", ("0", initial + "_0"), ("1", initial + "_1"))
    }
    for (src_state, read), (tgt_state, write, move) in turing_machine.transitions.items():
        inst_state = src_state + "_" + read
        inst_write = write
        inst_move = move
        if tgt_state in turing_machine.stop_states:
            inst_change_0 = tgt_state
            inst_change_1 = tgt_state
        else:
            inst_change_0 = ("0", tgt_state + "_0")
            inst_change_1 = ("1", tgt_state + "_1")
        transitions[inst_state] = (inst_write, inst_move, inst_change_0, inst_change_1)
    tape_q = inst_initial
    tape_m = 0
    tape_n = 0
    for i, cell in enumerate(turing_machine.tape):
        tape_n += int(cell) * 2**i
    inst_tape = (tape_q, tape_m, tape_n)
    return transitions, inst_tape


def encode_transition_as_2tag(inst_state, target):
    inst_write, inst_move, inst_change_0, inst_change_1 = target
    enc_transitions = {
        "a": "cxcx",
        "B": "S",
        "b": "s",
        "C": "D1D0",
        "c": "d1d0",
        "S": "T1T0",
        "s": "t1t0",
        "D1": "A1x1",
        "d1": "a1x1",
        "T1": "B1x1",
        "t1": "b1x1",
        "D0": "x0A0x0",
        "d0": "a0x0",
        "T0": "B0x0",
        "t0": "b0"
    }

    if inst_write == "0":
        enc_transitions["A"] = "Cx"
    elif inst_write == "1":
        enc_transitions["A"] = "Cxcx"
    else:
        assert False

    def encode_instantaneous_tm_as_2tag(transitions, tape):
    tape_q, tape_m, tape_n = tape
    enc_tape = "Ax" + "ax"*tape_m + "Bx" + "bx"*tape_n
    enc_transitions = {

    }

    transitions = []
    state = ()
    # single transition: Q_i -> (S_i, D_i, Q_i0, Q_i1)
    # state: (Q_i, M, N)
    # A x (a x)^M B x (b x)^N
    return transitions, state


def encode_tm_to_2tag(turing_machine):
    assert isinstance(turing_machine, TuringMachine)
    assert turing_machine.blank == '0'
    assert get_alphabet(turing_machine.transitions) == {'0', '1'}
    state = convert_to_instantaneous(turing_machine)




class TwoTagSystem:
    def __init__(self, transitions):
        self.transitions = transitions
        self.state = ""
        self.halt_symbol = ""
        self.step_number = 0

    def set_input_string(self, state, halt_symbol):
        self.step_number = 0
        self.state = state
        self.halt_symbol = halt_symbol

    def step(self):
        first = self.state[0]
        self.state = self.state[2:] + self.transitions[first]
        self.step_number += 1

    def print(self):
        print("step {step}: {state}".format(step=self.step_number, state=self.state))

    def run(self):
        print("Initial state:", self.state)
        while not self.state.startswith(self.halt_symbol):
            self.step()
            self.print()
