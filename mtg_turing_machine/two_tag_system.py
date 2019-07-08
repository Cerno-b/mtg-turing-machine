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
