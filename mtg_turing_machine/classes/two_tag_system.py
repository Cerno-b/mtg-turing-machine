from .turing_machine import TuringMachine


class TwoTagSystem:
    """Two tag system main class
    Attributes:
        transitions:            State transitions as dictionary in the form
                                    {symbol: list of symbols}
        state:                  The current state (list of symbols)
        halt_symbol:            Symbol indicating when the two tag system should halt.
        steps:                  The number of steps the two tag system has taken so far
        from_turing_machine:    Flag indicating that the two tag system has been converted from a Turing machine
        prev:                   Todo: check if still needed
        """
    def __init__(self, transitions):
        if isinstance(transitions, TuringMachine):
            self.transitions, self.state = self.encode_tm_to_2tag(transitions)
            self.halt_symbol = "#"
            self.steps = 0
            self.from_turing_machine = True
        else:
            self.transitions = transitions
            self.state = [""]
            self.halt_symbol = ""
            self.steps = 0
            self.from_turing_machine = False
        self.prev = None

    @staticmethod
    def get_alphabet(transitions):
        """Extract the alphabet from a transition function"""
        alphabet = [symbol for (_, symbol) in transitions.keys()]
        alphabet = set(alphabet)
        return alphabet

    @staticmethod
    def convert_tm_to_instantaneous_tm(turing_machine):
        """Convert a binary Turing machine to a form that allows executing reading and writing in a single step.
        This duplicates the number of states.
        For details refer to the Cocke/Minsky paper in the literature directory."""
        assert turing_machine.definition.tape_index == 0
        output_transitions = []
        output_stop_states = []

        for transition in turing_machine.definition.transitions.items():
            (source_state, read_symbol), (target_state, write_symbol, direction) = transition
            output_state = source_state + "_" + read_symbol
            output_write_symbol = write_symbol
            output_direction = direction

            # the output form will have separate states for having read a 0 or a 1
            if target_state in turing_machine.definition.stop_states:
                output_state_change_0 = target_state
                output_state_change_1 = target_state
                output_stop_states.append(target_state)
            else:
                output_state_change_0 = target_state + "_0"
                output_state_change_1 = target_state + "_1"

            transition = (output_state, output_write_symbol, output_direction,
                          output_state_change_0, output_state_change_1)
            output_transitions.append(transition)

        # Todo: adapt and test to make it work with arbitrary TM head positions.
        assert turing_machine.definition.tape_index == 0

        # express the tape (which only consists of 0 and 1) as two binary numbers, m and n (left and right of the head)
        tape_m = 0
        tape_n = 0
        for i, symbol in enumerate(turing_machine.definition.tape):
            tape_n += int(symbol) * 2 ** i
        output_tape = (tape_m, tape_n)
        return output_transitions, output_tape, output_stop_states

    @staticmethod
    def encode_transition_as_2tag(transition, stop_states):
        state_id, inst_write, inst_move, inst_change_0_id, inst_change_1_id = transition
        if inst_change_0_id in stop_states:
            inst_change_0_id = "#"  # set stop symbol
        if inst_change_1_id in stop_states:
            inst_change_1_id = "#"
        assert inst_write in ("0", "1")
        assert inst_move in ("<", ">")

        if inst_move == ">":
            enc_transitions = {
                "A$": ["C$", "x"] if inst_write == "0" else ["C$", "x", "c$", "x"],
                "a$": ["c$", "x", "c$", "x"],
                "B$": ["S$"],
                "b$": ["s$"],
                "C$": ["D$_1", "D$_0"],
                "c$": ["d$_1", "d$_0"],
                "S$": ["T$_1", "T$_0"],
                "s$": ["t$_1", "t$_0"],
                "D$_1": ["A!1", "x"],
                "d$_1": ["a!1", "x"],
                "T$_1": ["B!1", "x"],
                "t$_1": ["b!1", "x"],
                "D$_0": ["x", "A!0", "x"],
                "d$_0": ["a!0", "x"],
                "T$_0": ["B!0", "x"],
                "t$_0": ["b!0", "x"],
            }
        elif inst_move == "<":
            enc_transitions = {
                # switch A and B (is now called Z)
                "A$": ["Z$", "x"],
                "a$": ["z$", "x"],
                # Z (formerly A) now takes the role of B
                "Z$": ["S$"],
                "z$": ["s$"],
                # B takes the role of (formerly) A
                "B$": ["C$", "x"] if inst_write == "0" else ["C$", "x", "c$", "x"],
                "b$": ["c$", "x", "c$", "x"],
                "C$": ["D$_1", "D$_0"],
                "c$": ["d$_1", "d$_0"],
                "S$": ["T$_1", "T$_0"],
                "s$": ["t$_1", "t$_0"],

                "D$_1": ["Y$_1", "x"],
                "d$_1": ["y$_1", "x"],
                "T$_1": ["A!1", "x"],
                "t$_1": ["a!1", "x"],
                "D$_0": ["x", "Y$_0", "x"],
                "d$_0": ["y$_0", "x"],
                "T$_0": ["A!0", "x"],
                "t$_0": ["a!0", "x"],

                "Y$_0": ["B!0", "x"],
                "y$_0": ["b!0", "x"],
                "Y$_1": ["B!1", "x"],
                "y$_1": ["b!1", "x"]
            }
        else:
            assert False

        new_enc_transitions = {}
        for source, targets in enc_transitions.items():
            source = source.replace("$", "_" + str(state_id))
            new_targets = []
            for target in targets:
                if ("A!0" == target and inst_change_0_id == "#") or ("A!1" in target and inst_change_1_id == "#"):
                    target = "#"
                else:
                    target = target.replace("$", "_" + str(state_id))
                    target = target.replace("!0", "_" + str(inst_change_0_id))
                    target = target.replace("!1", "_" + str(inst_change_1_id))
                new_targets.append(target)
            new_enc_transitions[source] = new_targets

        return new_enc_transitions

    @staticmethod
    def encode_instantaneous_tm_as_2tag(transitions, tape, start_state, stop_states):
        tape_m, tape_n = tape
        ss = "q_init_0"
        transitions.append((ss, "0", ">", start_state + "_0", start_state + "_1"))
        # if tape_n % 2 == 0:
        #     ss = start_state + "_0"
        # elif tape_n % 2 == 1:
        #     ss = start_state + "_1"
        # else:
        #    assert False
        enc_tape = ["A_" + ss, "x"] + ["a_" + ss, "x"] * tape_m + ["B_" + ss, "x"] + ["b_" + ss, "x"] * tape_n

        enc_transitions = {}

        for transition in transitions:
            new_transitions = TwoTagSystem.encode_transition_as_2tag(transition, stop_states)
            for key, value in new_transitions.items():
                assert key not in enc_transitions
                enc_transitions[key] = value

        return enc_transitions, enc_tape

    @staticmethod
    def encode_tm_to_2tag(turing_machine):
        assert isinstance(turing_machine, TuringMachine)
        assert turing_machine.definition.blank == '0'
        assert TwoTagSystem.get_alphabet(turing_machine.definition.transitions) == {'0', '1'} \
            or TwoTagSystem.get_alphabet(turing_machine.definition.transitions) == {"0"} \
            or TwoTagSystem.get_alphabet(turing_machine.definition.transitions) == {"1"}
        transitions, tape, stop_states = TwoTagSystem.convert_tm_to_instantaneous_tm(turing_machine)
        transitions, tape = TwoTagSystem.encode_instantaneous_tm_as_2tag(transitions, tape,
                                                                         turing_machine.definition.initial_state,
                                                                         stop_states)
        return transitions, tape

    def set_input_string(self, state, halt_symbol):
        self.steps = 0
        self.state = list(state)
        self.halt_symbol = halt_symbol

    def step(self):
        first = self.state[0]
        self.state = self.state[2:] + self.transitions[first]
        self.steps += 1

    def print_definition(self):
        alphabet = set()
        for key, value in self.transitions.items():
            alphabet.add(key)
            alphabet = alphabet.union(set(value))
        print("Transitions:")
        for key, value in self.transitions.items():
            print("  {key}->{value}".format(key=key, value=value))
        print("Number of transitions:", len(self.transitions))
        print("Alphabet: {}".format(sorted(alphabet)))
        print("Alphabet size: {}".format(len(alphabet)))
        print("Initial state:", self.state)
        print("Initial state size:", len(self.state))
        print()

    def print(self):
        first = self.state[0]
        if first == self.halt_symbol:
            print("\rstep:", self.steps, "- state:", self.get_brief_state())
            print("Halt Symbol reached.")
        else:
            print("\rstep:", self.steps, "- trans:", first, "->", self.transitions[first], "- state:",
                  self.get_brief_state())
        self.prev = first

    def print_summary(self):
        print("Two-Tag System")
        print("--------------")
        self.print_definition()

    def get_tm_tape(self):
        assert self.from_turing_machine
        assert self.state[0] == "#" or self.state[0].startswith("A")
        assert self.state[1] == "x"

        state = self.state[2:]
        m = 0
        n = 0
        while not state[0].startswith("B"):
            assert state[0].startswith("a") and state[1] == "x"
            m += 1
            state = state[2:]
        assert state[0].startswith("B") and state[1] == "x"
        state = state[2:]
        while state:
            assert state[0].startswith("b") and state[1] == "x"
            n += 1
            if len(state) > 2:
                state = state[2:]
            else:
                assert len(state) == 2
                state = []
        left = bin(m)[2:] if m > 0 else ""
        right = bin(n)[2:] if n > 0 else ""
        right = "".join((reversed(right)))
        return left + "^" + right

    def get_brief_state(self):
        state_copy = self.state
        current_symbol = []
        count = 0
        brief = ""
        while len(state_copy) >= 2:
            symbol = state_copy[0:2]
            state_copy = state_copy[2:]
            if current_symbol == symbol:
                count += 1
            else:
                if current_symbol:
                    brief += "({symbol})^{count}, ".format(count=count, symbol=" ".join(current_symbol))
                current_symbol = symbol
                count = 1
        brief += "({symbol})^{count}, ".format(count=count, symbol=" ".join(current_symbol))
        if len(state_copy) > 0:
            brief += "({symbol})^1, ".format(symbol=" ".join(state_copy))
        return brief

    def run(self, brief=False, silent=False):
        first = self.state[0]
        if not silent:
            if brief:
                print("Number of transitions:", len(self.transitions))
                print("Initial state:", self.get_brief_state())
            else:
                self.print_definition()
                print(first, "->", self.transitions[first])
        while self.state[0] != self.halt_symbol:
            if len(self.state) < 2:
                break
            self.step()
            first = self.state[0]
            if not silent:
                if brief:
                    if first.startswith("A"):
                        self.print()
                else:
                    self.print()

        if self.from_turing_machine:
            print()
            print("Final Result:")
            m = self.state.count("a_#")
            n = self.state.count("b_#")
            m_str = str(bin(m))[2:] if m > 0 else ""
            n_str = str(bin(n))[2:] if n > 0 else ""
            print(m_str + "^" + n_str)
