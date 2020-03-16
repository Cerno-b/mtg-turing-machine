from .turing_machine import TuringDefinition


class TwoTagSystem:
    """Two tag system main class
    Attributes:
        production_rules:       Production rules (dict), corresponds to the transition function of a Turing machine
        current_word:           The current word (list of symbols), corresponds to the tape of a Turing machine
        halting_symbol:         Symbol indicating when the two tag system should halt.
        steps:                  The number of steps the two tag system has taken so far
        from_turing_machine:    Flag indicating that the two tag system has been converted from a Turing machine
        """

    def __init__(self, definition):
        """Initialize
        Arguments:
            definition: Definition of the two tag system. Either a Turing Machine Definition or production rules
                - Turing machine as binary TuringDefinition (binary Turing machine only consists of the symbols 0 and 1)
                - Production rules as a dictionary of the form:
                    {symbol: list of symbols}
            """
        assert isinstance(definition, TuringDefinition) or isinstance(definition, dict)
        if isinstance(definition, TuringDefinition):
            self.init_from_turing_machine(definition)
        else:
            self.production_rules = definition
            self.current_word = [""]
            self.halting_symbol = ""
            self.steps = 0
            self.from_turing_machine = False

    def init_from_turing_machine(self, tm_definition):
        """Initialize the two tag system from a binary Turing machine"""
        assert isinstance(tm_definition, TuringDefinition)
        assert tm_definition.blank == '0'
        alphabet = self.get_alphabet(tm_definition.transitions)
        assert alphabet == {'0', '1'} or alphabet == {"0"} or alphabet == {"1"}

        self.production_rules, self.current_word = self.convert_tm_to_two_tag_system(tm_definition)

        self.halting_symbol = "#"
        self.steps = 0
        self.from_turing_machine = True

    @staticmethod
    def get_alphabet(transitions):
        """Extract the alphabet from a transition function"""
        alphabet = [symbol for (_, symbol) in transitions.keys()]
        alphabet = set(alphabet)
        return alphabet

    @staticmethod
    def convert_tm_to_two_tag_system(tm_definition):
        """Convert a binary Turing machine to a two tag system.
        For details refer to the Cocke/Minsky paper in the 'literature' directory."""

        # Todo: adapt and test to make it work with arbitrary TM head positions.
        assert tm_definition.tape_index == 0

        # first, convert the Turing machine into a tm-like construct that allows reading and writing simultaneously

        adapted_transitions = []  # list of transitions adapted to the tm-like construct

        for transition in tm_definition.transitions.items():
            (source_state, read_symbol), (target_state, write_symbol, direction) = transition
            adapted_state = source_state + "_" + read_symbol

            # the tm-like construct will have separate states for having read a 0 or a 1
            if target_state in tm_definition.stop_states:
                adapted_state_change_0 = target_state
                adapted_state_change_1 = target_state
            else:
                adapted_state_change_0 = target_state + "_0"
                adapted_state_change_1 = target_state + "_1"

            adapted_transition = (adapted_state, write_symbol, direction,
                                  adapted_state_change_0, adapted_state_change_1)
            adapted_transitions.append(adapted_transition)

        # Express the tm tape (which only has 0s and 1s) as two binary numbers, m and n (left and right of the head)
        tape_m = 0
        tape_n = 0
        for i, symbol in enumerate(tm_definition.tape):
            tape_n += int(symbol) * 2 ** i

        # A special unique start state (uss) needs to be prepended since the Turing machine's original start state
        # was split into two states and we must begin with a single start state
        uss = "q_init_0"
        tm_initial_state = tm_definition.initial_state
        uss_transition = (uss, "0", ">", tm_initial_state + "_0", tm_initial_state + "_1")
        adapted_transitions.append(uss_transition)

        # Convert the start tape's two binary numbers into a two tag system's start word of the form
        # [A x a x a x... a x B x b x b x...b x] where each a x and b x occurs m and n times, respectively.
        # The upper case A x and B x only occur once and act as separators between the left and right hand side
        # Each adapted state 's' will receive their own A and B variants, named a_'s' and b_'s'.
        # In this instance, 's' is the unique start state uss. The remaining a_'s' and b_'s' will be defined later.
        start_word = ["A_" + uss, "x"] + ["a_" + uss, "x"] * tape_m + ["B_" + uss, "x"] + ["b_" + uss, "x"] * tape_n

        production_rules = {}

        # convert the tm's adapted transitions to two tag system production rules
        for adapted_transition in adapted_transitions:
            prod_rules = TwoTagSystem.transition_to_production_rules(adapted_transition, tm_definition.stop_states)

            # add the production rules for a single transition to the dictionary of all production rules
            for key, value in prod_rules.items():
                assert key not in production_rules
                production_rules[key] = value

        return production_rules, start_word

    @staticmethod
    def transition_to_production_rules(adapted_transition, tm_stop_states):
        """Convert a single adapted Turing machine transition into
        a set of multiple two tag system production rules
        Arguments:
            adapted_transition: The transition to be converted (5-tuple, see function convert_tm_to_two_tag_system())
            tm_stop_states:     The Turing machine's stop states (list)"""

        tm_state, tm_write_symbol, tm_direction, tm_state_change_0, tm_state_change_1 = adapted_transition

        # rename the stop states to the stopping symbol "#"
        if tm_state_change_0 in tm_stop_states:
            tm_state_change_0 = "#"
        if tm_state_change_1 in tm_stop_states:
            tm_state_change_1 = "#"

        assert tm_write_symbol in ("0", "1")  # make sure the Turing machine is actually binary
        assert tm_direction in ("<", ">")  # only left and right head movement is supported

        # set up the production rules for right and left head movement according to the Cocke and Minsky paper
        # refer to the paper in the "literature" directory for details
        # The strings "$", "!0" and "!1" are placeholders and will be replaced by
        # the corresponding adapted Turing machine state names.
        if tm_direction == ">":
            production_rules = {
                "A$": ["C$", "x"] if tm_write_symbol == "0" else ["C$", "x", "c$", "x"],
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
        elif tm_direction == "<":
            production_rules = {
                # switch A and B (is now called Z)
                "A$": ["Z$", "x"],
                "a$": ["z$", "x"],
                # Z (formerly A) now takes the role of B
                "Z$": ["S$"],
                "z$": ["s$"],
                # B takes the role of (formerly) A
                "B$": ["C$", "x"] if tm_write_symbol == "0" else ["C$", "x", "c$", "x"],
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

        # iterate over the production rules and make some final adaptations
        final_production_rules = {}
        for source_symbol, target_symbols in production_rules.items():
            source_symbol = source_symbol.replace("$", "_" + str(tm_state))  # replace placeholder by tm state names

            # iterate over the targets (right-hand side) of the production rules and make some final adaptations
            final_targets = []
            for target in target_symbols:
                # set the halting symbol to the target to make the two tag system stop
                if (target == "A!0" and tm_state_change_0 == "#") or (target == "A!1" and tm_state_change_1 == "#"):
                    target = "#"
                else:  # if not stopping, replace placeholders by tm state names
                    target = target.replace("$", "_" + str(tm_state))
                    target = target.replace("!0", "_" + str(tm_state_change_0))
                    target = target.replace("!1", "_" + str(tm_state_change_1))
                final_targets.append(target)
            final_production_rules[source_symbol] = final_targets

        return final_production_rules

    def set_initial_word(self, initial_word, halting_symbol):
        """Set the initial word and halting symbol. This will reset the steps counter."""
        self.steps = 0
        self.current_word = list(initial_word)
        self.halting_symbol = halting_symbol

    def step(self):
        """Compute a single step of the two tag system"""
        # cut off the first two symbols and place the result of the production rule based on the first symbol to the
        # end of the word
        first_symbol = self.current_word[0]
        self.current_word = self.current_word[2:] + self.production_rules[first_symbol]
        self.steps += 1

    def print_definition(self):
        """Print a summary of the current two tag system definition"""
        alphabet = set()
        for key, value in self.production_rules.items():
            alphabet.add(key)
            alphabet = alphabet.union(set(value))

        print("Production Rules:")
        for key, value in self.production_rules.items():
            print("  {key}->{value}".format(key=key, value=value))
        print("Number of production rules:", len(self.production_rules))
        print("Alphabet: {}".format(sorted(alphabet)))
        print("Alphabet size: {}".format(len(alphabet)))
        print("Initial word:", self.current_word)
        print("Initial word length:", len(self.current_word))
        print()

    def print_summary(self):
        """Print a summary of the current two tag system definition with a header"""
        print("Two-Tag System")
        print("--------------")
        self.print_definition()

    def print(self):
        """Print the current state of the two tag system"""
        first_symbol = self.current_word[0]
        if first_symbol == self.halting_symbol:
            print("\rstep:", self.steps, "- word:", self.get_brief_word())
            print("Halting Symbol reached.")
        else:
            print("\rstep:", self.steps,
                  "- rule:", first_symbol, "->", self.production_rules[first_symbol],
                  "- word:", self.get_brief_word())

    def get_word_as_tm_tape(self):
        """Return the two tag system's current word in the form of the original binary TM's tape"""

        assert self.from_turing_machine
        # make sure the two tag system has finished a cycle that marks the beginning of a TM step
        assert self.current_word[0] == "#" or self.current_word[0].startswith("A")
        assert self.current_word[1] == "x"

        # the word should now look like this:
        # - a single "A x"
        # - one or more "a x"
        # - a single "B x"
        # - one or more "b x"
        # A x and B x act as separators

        word = self.current_word[2:]  # cut off the initial "A x"
        m = 0
        n = 0

        # count all "a x" until "B x" is reached
        while not word[0].startswith("B"):
            assert word[0].startswith("a") and word[1] == "x"
            m += 1
            assert len(word) % 2 == 0
            word = word[2:]

        assert word[0].startswith("B") and word[1] == "x"
        word = word[2:]  # cut off the "B x"

        # count all "b x" until the end
        while word:
            assert word[0].startswith("b") and word[1] == "x"
            n += 1
            assert len(word) % 2 == 0
            word = word[2:]

        # convert numbers to binary strings, with the right string reversed
        left = bin(m)[2:] if m > 0 else ""
        right = bin(n)[2:] if n > 0 else ""
        right = "".join((reversed(right)))
        return left + "^" + right  # mark the head position with a ^

    def get_brief_word(self):
        """The two tag system's word will get very long if the tts was derived from a Turing machine.
        Instead of outputting all 'a x' and 'b x' repetitions, repeated occurrences of symbol pairs will be
        represented by the pair, followed by its count, e.g. '[a x]^5' for 5 occurrences of the 'a x' pair."""
        word_copy = self.current_word
        current_symbol_pair = []
        count = 0

        brief_word = ""
        while len(word_copy) >= 2:

            # cut off a symbol pair
            symbol_pair = word_copy[0:2]
            word_copy = word_copy[2:]

            if current_symbol_pair == symbol_pair:  # if it fits the currently counted pair, increment
                count += 1
            else:  # otherwise switch to the new pair and append the old one to the brief word
                if current_symbol_pair:
                    brief_word += "({symbol})^{count}, ".format(count=count, symbol=" ".join(current_symbol_pair))
                current_symbol_pair = symbol_pair
                count = 1
        brief_word += "({symbol})^{count}, ".format(count=count, symbol=" ".join(current_symbol_pair))

        # if a single symbol is left (odd number of symbols in the word), append it
        if len(word_copy) > 0:
            brief_word += "({symbol})^1, ".format(symbol=" ".join(word_copy))
        return brief_word

    def run(self, brief=False, silent=False):
        """Run the two tag system until it reaches a halting symbol and stops.
        Arguments:
            brief:  Print updates in brief format
            silent: Suppress any output except the final result"""
        first_symbol = self.current_word[0]
        if not silent:
            if brief:
                print("Number of transitions:", len(self.production_rules))
                print("Initial state:", self.get_brief_word())
            else:
                self.print_definition()
                print(first_symbol, "->", self.production_rules[first_symbol])
        # repeat until halting symbol reached or current word becomes shorter than 2 symbols
        while self.current_word[0] != self.halting_symbol and len(self.current_word) >= 2:
            self.step()
            first_symbol = self.current_word[0]
            if not silent:
                # in case of a tts based on a tm, only give status updates after one tts cycle ends
                if brief and self.from_turing_machine:
                    if first_symbol.startswith("A"):
                        self.print()
                else:  # in all other cases (brief == False or tts not based on tm), always give status updates
                    self.print()

        # in case of tts based on a tm, convert the final word back to a tm tape
        if self.from_turing_machine:
            print()
            print("Final Result:")
            print(self.get_word_as_tm_tape())
