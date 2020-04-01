# Magic: The Gathering Turing Machine

A compiler that converts any [Turing machine](https://en.wikipedia.org/wiki/Turing_machine) into a Magic: The Gathering Turing machine (MTG-TM), which allows to run programs within the game of Magic: The Gathering.

Based on the brilliant paper [Magic: The Gathering is Turing Complete](https://arxiv.org/abs/1904.09828) by Alex Churchill, Stella Biderman and Austin Herrick.

This video gives an overview about the conversion algorithm: https://www.youtube.com/watch?v=YzXoFldEux. As you will see, the resulting machines are prohibitively slow even for rather simple problems.

The conversion is done in four steps:
- convert the Turing machine to a binary Turing machine (that only uses the symbols 0 and 1)
- convert the binary Turing machine to a [2-tag](https://en.wikipedia.org/wiki/Tag_system) system
- convert the 2-tag system to a string that can be emulated by a [universal Turing machine](https://en.wikipedia.org/wiki/Universal_Turing_machine), specifically a UTM(2,18)
- recreate the UTM(2,18) and its tape string within a game of Magic: The Gathering

## Installation

The code is compatible with Python 3.6+ and does not need any additional packages.

## Instructions

I would recommend running the unit tests first to check that everything works. From the repository root, call
```
python -m unittest
```

From there, you can explore the different conversion options. Since the simulation of a MTG-TM that has been constructed from an arbitrary Turing machine can run a very long time, it may be advisable to start with a simpler conversion. The code allows to start at any point in the conversion, so you could construct a 2-tag system by hand which should simulate in a few seconds. Since non-binary Turing machines can take months or even years to simulate, you can speed up the process significantly by building a binary Turing machine by hand. It will still be slow, but may just be feasible.

In the following you will find a few pointers about how to construct each type of program by hand. You can find examples for all these program types in the file [instances.py](mtg_turing_machine/classes/instances.py)

### Turing Machine

The non-binary Turing machine is defined as follows:

- a transition function (dictionary)
  - format: `(old_state, read_symbol): new_state, write_symbol, head_direction`
  - the head direction is denoted by a "<" and ">" for left and right, respectively. 
  - you can also use "-" for keeping the head in place, but that will not be supported in all conversions.
- a tape (string) consisting only of symbols that occur in the transition function. 
  - You can use a list of strings instead if you want your symbols to have more than one character. They will still be treated as single symbols
- the tape index that marks the starting position of the Turing head.
- the blank symbol
- a list of stop states. The machine halts as soon as one of these states is reached

```python
    transitions = {
        ("q0", "1"): ("q0", "1", ">"),
        ("q0", "x"): ("q1", "x", ">"),
        ("q1", "_"): ("qend", "_", "<"),
        ("q1", "1"): ("q2", "x", "<"),
        ("q2", "x"): ("q0", "1", ">")
    }
    tape = "111x11"
    tape_index = 0
    initial_state = "q0"
    blank = "_"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    tm = TuringMachine(definition)
```
### Binary Turing Machine

The binary Turing machine is a regular Turing machine that only consists of the symbols 0 and 1.

You can convert a regular Turing machine to a binary one like this: 
```
# assume turing_machine has been constructed like described above.
turing_machine.convert_to_two_symbol()
```

Alternatively, you can construct a binary Turing machine manually, by limiting yourself to an alphabet of 0 and 1. This is very likely more runtime-efficient than the automatical conversion, but more complex machines are tricky to convert by hand.

```python
    transitions = {
        ("q0", "1"): ("q0", "1", ">"),
        ("q0", "0"): ("q1", "0", ">"),
        ("q1", "0"): ("qend", "0", "<"),
        ("q1", "1"): ("q2", "0", "<"),
        ("q2", "0"): ("q3", "1", ">"),
        ("q3", "0"): ("q1", "0", ">"),
    }
    tape = "111011"
    tape_index = 0
    initial_state = "q0"
    blank = "0"
    stop_states = ["qend"]
    definition = TuringDefinition(transitions, initial_state, stop_states, tape, tape_index, blank=blank)
    tm =  TuringMachine(definition)
```

### 2-Tag System

A 2-tag system processes a string by chopping off the first two letters, looking up the first of the two letters in the production rules table and attaches the string it finds to the end of the original string. Surprisingly, 2-tag systems are as powerful as Turing machines, but much harder to write by hand.

A two tag system is defined like this:

- the production rules (dictionary) in the form `read_symbol: write_symbol`
- the initial word (string), can also be a list of characters
- the halt symbol. The 2-tag system stops when it reads this symbol. It also stops when the working string is too short to read two symbols

Instead of passing a dictionary to the TwoTagSystem class, you can alternatively pass a TuringDefinition object that describes a **binary** Turing machine. If you do, the 2-tag system will be constructed based on the TuringDefinition. In that case, you don't neet do set an initial word, as that will be constructed from the Turing machine's tape. In order to use an arbitrary Turing machine, you need to convert it to a binary Turing machine first.

```
    production_rules = {
        "a": ["b", "c"],
        "b": ["a"],
        "c": ["a", "a", "a"],
    }
    halt_symbol = "#"
    initial_word = "aaa"

    two_tag = TwoTagSystem(production_rules)
    two_tag.set_initial_word(initial_word, halt_symbol)
```
