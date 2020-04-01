# Magic: The Gathering Turing Machine

A compiler that converts any [Turing machine](https://en.wikipedia.org/wiki/Turing_machine) into a Magic: The Gathering Turing machine (*MTG-TM*). This allows to run programs within the game of *Magic: The Gathering*.

Based on the awesome paper [*Magic: The Gathering is Turing Complete*](https://arxiv.org/abs/1904.09828) by Alex Churchill, Stella Biderman and Austin Herrick.

Here is an overview video about the conversion algorithm: https://www.youtube.com/watch?v=YzXoFldEux. As you will see, unfortunately the resulting machines are prohibitively slow even for rather simple problems.

The conversion from Turing machine to MTG:TM is done in four steps:
- convert the Turing machine to a binary Turing machine (that only uses the symbols 0 and 1)
- convert the binary Turing machine to a [2-tag](https://en.wikipedia.org/wiki/Tag_system) system
- convert the 2-tag system to a string that can be emulated by a [universal Turing machine](https://en.wikipedia.org/wiki/Universal_Turing_machine), specifically a *UTM(2,18)*
- recreate the UTM(2,18) and its tape string within a game of *Magic: The Gathering*

## Installation

The code is compatible with Python 3.6+ and does not need any additional packages.

## Instructions

I would recommend running the unit tests first to check that everything works. From the repository root, call
```
python -m unittest
```

From there, you can explore the different conversion options. Since the simulation of a MTG-TM constructed from an arbitrary Turing machine can run a very long time, it may be advisable to start with a simpler conversion. The code allows to start at any point in the conversion chain, so you could construct a 2-tag system by hand which should simulate in a few seconds. Unfortunately it is not trivial to build meaningful 2-tag systems manually. 

Another option is to write a binary Turing machines by hand, since auto-converted ones can take months or even years to finish the simulation, so you can speed up the process significantly by building a binary Turing machine on your own. It will still be slow, but may just be feasible. Although easier to write than 2-tag systems, binary Turing machines are still pretty tricky.

In the following you will find a few pointers about how to construct each type of program by hand. You can find examples for all these program types in the file [instances.py](mtg_turing_machine/classes/instances.py). It is generally advisable to check the unit tests on usage details.

### Turing Machine

The non-binary Turing machine is defined as follows:

- a transition function (dictionary)
  - format: `(old_state, read_symbol): new_state, write_symbol, head_direction`
  - the head direction is denoted by a "<" and ">" for left and right, respectively. 
  - you can also use "-" for keeping the head in place, but that will not be supported in all conversions.
- a tape (string) consisting only of symbols that occur in the transition function. 
  - You can use a list of strings instead if you want your symbols to have more than one character.
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
turing_machine = TuringMachine(definition)
```

Run the simulation and retrieve the results like this:

```python
turing_machine.run()
tape = turing_machine.get_stripped_tape()
```

The resulting tape will be stripped of blank symbols at the beginning and end.

### Binary Turing Machine

The binary Turing machine is a regular Turing machine that only consists of the symbols 0 and 1.

You can convert a regular Turing machine to a binary one like this: 

```python
turing_machine.convert_to_two_symbol()
```

If the input machine was already binary, the conversion will be skipped automatically. During the conversion, the original machine's symbol set is converted to a binary representation, so after stopping, the machine has to convert it back to the original symbol set. This can be achieved like this, but only if the Turing machine has been automatically converted to binary:

```python
turing_machine.run()
tape = turing_machine.get_stripped_tape(decode_binarized=True)
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

A 2-tag system processes a working string by chopping off the first two letters, looking up the first of the two letters in the production rules table and attaching the string it finds to the end of the working string. Surprisingly, 2-tag systems are as powerful as Turing machines, but much harder to write by hand.

A two tag system is defined like this:

- the production rules (dictionary) in the form `read_symbol: list_of_write_symbols`
- the initial word (string), can also be a list of strings
- the halt symbol. The 2-tag system stops when it reads this symbol. It also stops when the working string is shorter than 2 symbols

```python
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
You run the 2-tag system like this:

```python
two_tag.run()
result = two_tag.current_word
```

Instead of passing a dictionary to the TwoTagSystem class, you can alternatively pass a TuringDefinition object that describes a **binary** Turing machine. If you do that, the 2-tag system will be constructed based on the TuringDefinition. In that case, you don't need do set an initial word, as that will be constructed from the Turing machine's tape. If you want to use an arbitrary Turing machine instead of a binary one, you need to convert it to a binary Turing machine first, as described above.

When building a 2-tag system from a Turing machine, the alphabet will get severely modified to fit to the 2-tag system's architecture. Convert the result back to the binary Turing machine representation like this:

```python
two_tag.run()
tape = two_tag.get_word_as_tm_tape()
```

If the binary Turing machine was constructed automatically, you may want to reconstruct the original Turing machine's tape. The whole setup would look something like this:

```python
turing_machine.convert_to_two_symbol()
two_tag = TwoTagSystem(turing_machine.definition)
two_tag.run()
tape = two_tag.get_word_as_tm_tape()

# Write the tape to the original turing_machine and let it decode the string to the original alphabet.
# Check whether the original turing machine was already binary and skip the conversion if necessary.
if turing_machine.is_binarized_tm:
    turing_machine.set_tape_string(tape)
    tape = turing_machine.get_stripped_tape(decode_binarized=True)
```

### Universal Turing Machine

The universal Turing machine used in this project is the *UTM(2,18)* defined by [Yurii Rogozhin](mtg-turing-machine\documentation\literature\1-s2.0-S0304397596000771-main.pdf). It is a regular Turing machine with a predefined transition function and alphabet. A Turing machine you want to run on the UTM must be encoded to the UTM's tape in a way that the UTM can emulate. Writing a UTM's program by hand is very hard, but you can convert a 2-tag system to a UTM(2,18) like this:

```python
utm = UniversalTuringMachine()
utm.set_tape_string_from_two_tag(two_tag)
utm.run()
two_tag_string utm.decode_tape_as_two_tag_word()
```

Or, if you want to run the whole conversion chain, start with an arbitrary Turing machine, convert it to binary, then to a 2-tag system and finally to a UTM. After the finished run, the result needs to be converted back to the original symbol set. Beware though, the whole conversion chain lets the complexity grow by orders of magnitude, so don't expect the simulation to finish anytime soon.

```python
turing_machine.convert_to_two_symbol()
turing_machine.set_tape_string(string)

two_tag = TwoTagSystem(turing_machine)

utm = UniversalTuringMachine()
utm.set_tape_string_from_two_tag(two_tag)
utm.run()

two_tag_state = utm.decode_tape_as_two_tag_word()
two_tag.set_initial_word(two_tag_state, two_tag.halting_symbol)
tape = two_tag.get_word_as_tm_tape()

if turing_machine.is_binarized_tm:
    turing_machine.set_tape_string(tape)
    tape = turing_machine.get_stripped_tape(decode_binarized=True)
```

### Magic: The Gathering Turing Machine

The final step in the conversion is to run the simulation within the world of Magic: The Gathering. Since re-creating the full rule set of M:TG is no small feat, this project only simulates the parts that are relevant to the Turing machine. Wherever a simplification has been made, the code is heavily documented to describe the rationale behind the application of the corresponding M:TG rules. Setting up the game from scratch is not part of the simulation. Please refer to the [paper](mtg-turing-machine\documentation\literature\1904.09828.pdf), or watch Kyle Hill's excellent [video](https://www.youtube.com/watch?v=pdmODVYPDLA) explaining how it's done.

For our purposes, we need to convert a UTM to a MTG-TM and run it. The whole chain looks like this, but you can jump in at any point if you have constructed a different representation by hand:

```python
turing_machine.convert_to_two_symbol()
turing_machine.set_tape_string(string)

two_tag = TwoTagSystem(turing_machine)

utm = UniversalTuringMachine()
utm.set_tape_string_from_two_tag(two_tag)

mtg_utm = MagicTheGatheringTuringMachine(utm)
mtg_utm.run()
utm = mtg_utm.get_utm()

two_tag_state = utm.decode_tape_as_two_tag_word()
two_tag.set_initial_word(two_tag_state, two_tag.halting_symbol)
tape = two_tag.get_word_as_tm_tape()

if turing_machine.is_binarized_tm:
    turing_machine.set_tape_string(tape)
    tape = turing_machine.get_stripped_tape(decode_binarized=True)
```

In case you manage to build a tiny program that you think you can set up with real cards, you may want to print the MTG-TM setup by calling  `mtg_utm.print()`. The result will show you all the cards both players have in play (again check out [Kyle's video](https://www.youtube.com/watch?v=pdmODVYPDLA) on forcing the initial setup). 

During the setup phase, some cards were edited by cards like [Glamerdye](https://gatherer.wizards.com/pages/card/details.aspx?multiverseid=153439). The changes are printed in square brackets, so don't be surprised that the cards have a different text than you're used to. Also, the cards' color differ from their official versions because a lot of cards have been given all colors except blue. I generally found that the Churchill et al. really went out of their way to make the machine airtight in terms of M:TG rules, so whenever you see a loophole, it's likely that I omitted some information to conserve space. If you see any rule problems, please open a ticket, we can discuss it there.

The Turing tape is represented by tokens and will be printed using only the first letter of the corresponding creature type (A = Aetherborn, B = Basilisk, etc) to conserve space. Also, the order of the tape will be defined by the tokens' power and toughness, where the tokens immediately left of the Turing head have 3/3 and increase by 1/1 as we move away from the head to the left and right. Again, to conserve space, this information will be omitted, instead the tokens will be printed in their correct order, with the head position marked by square brackets. A possible starting setup may look like this:

```
Player: Bob
-----------
Hand:
    empty

Library:
    empty

Control cards:
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Aetherborn] dies, create a 2/2 [white] [Sliver] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Basilisk] dies, create a 2/2 [green] [Elf] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Cephalid] dies, create a 2/2 [white] [Sliver] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Demon] dies, create a 2/2 [green] [Aetherborn] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Elf] dies, create a 2/2 [white] [Demon] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Faerie] dies, create a 2/2 [green] [Harpy] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Giant] dies, create a 2/2 [green] [Juggernaut] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Harpy] dies, create a 2/2 [white] [Faerie] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Illusion] dies, create a 2/2 [green] [Faerie] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Juggernaut] dies, create a 2/2 [white] [Illusion] creature token.
    Xathrid Necromancer:                    Whenever Xathrid Necromancer or another [Kavu] creature you control dies, create a tapped 2/2 [white] [Leviathan] creature token.
    Xathrid Necromancer:                    Whenever Xathrid Necromancer or another [Leviathan] creature you control dies, create a tapped 2/2 [white] [Illusion] creature token.
    Xathrid Necromancer:                    Whenever Xathrid Necromancer or another [Myr] creature you control dies, create a tapped 2/2 [white] [Basilisk] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Noggle] dies, create a 2/2 [green] [Orc] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Orc] dies, create a 2/2 [white] [Pegasus] creature token.
    Xathrid Necromancer:                    Whenever Xathrid Necromancer or another [Pegasus] creature you control dies, create a tapped 2/2 [green] [Rhino] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Rhino] dies, create a 2/2 [blue] [Assassin] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Sliver] dies, create a 2/2 [green] [Cephalid] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Aetherborn] dies, create a 2/2 [green] [Cephalid] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Basilisk] dies, create a 2/2 [green] [Cephalid] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Cephalid] dies, create a 2/2 [white] [Basilisk] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Demon] dies, create a 2/2 [green] [Elf] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Elf] dies, create a 2/2 [white] [Aetherborn] creature token.
    Xathrid Necromancer (phased out):       Whenever Xathrid Necromancer or another [Faerie] creature you control dies, create a tapped 2/2 [green] [Kavu] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Giant] dies, create a 2/2 [green] [Harpy] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Harpy] dies, create a 2/2 [white] [Giant] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Illusion] dies, create a 2/2 [green] [Juggernaut] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Juggernaut] dies, create a 2/2 [white] [Giant] creature token.
    Xathrid Necromancer (phased out):       Whenever Xathrid Necromancer or another [Kavu] creature you control dies, create a tapped 2/2 [green] [Faerie] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Leviathan] dies, create a 2/2 [green] [Juggernaut] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Myr] dies, create a 2/2 [green] [Orc] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Noggle] dies, create a 2/2 [green] [Orc] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Orc] dies, create a 2/2 [white] [Noggle] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Pegasus] dies, create a 2/2 [green] [Sliver] creature token.
    Xathrid Necromancer (phased out):       Whenever Xathrid Necromancer or another [Rhino] creature you control dies, create a tapped 2/2 [white] [Sliver] creature token.
    Rotlung Reanimator (phased out):        Whenever Rotlung Reanimator or another [Sliver] dies, create a 2/2 [white] [Myr] creature token.
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Lhurgoyf] dies, create a 2/2 [green] [Lhurgoyf] creature token
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Rat] dies, create a 2/2 [white] [Rat] creature token

Remaining cards:
    Blazing Archon:                        Flying. Creatures can't attack you.
    Wild Evocation:                        At the beginning of each player's upkeep, that player reveals a card at random from their hand.If it's a land card, the player puts it onto the battlefield. Otherwise, the player casts it without paying its mana cost if able.
    Recycle:                               Skip your draw step. Whenever you play a card, draw a card. Your maximum hand size is two.
    Privileged Position:                   Other permanents you control have hexproof.
    Vigor:                                 Trample. If damage would be dealt to another creature you control, prevent that damage. Put a +1/+1 counter on that creature for each 1 damage prevented this way. When Vigor is put into a graveyard from anywhere, shuffle it into its owner's library.


Tape tokens ([] marks the head position):
------------
cycle 0, state q1: <RRFFAAAAAFFAAAFFAAAAAF[F]AAAMAAAMAAAMAAAMAAAMAAAMAAAMAAAMAAAAAAAM>

Player: Alice
-------------
Hand:
    Infest:                                 All creatures get -2/-2 until end of turn.

Library:
    Soul Snuffers:                         When Soul Snuffers enters the battlefield, put a -1/-1 counter on each creature.
    Coalition Victory:                     You win the game if you control a land of each basic land type and a creature of each color
    Cleansing Beam:                        Cleansing Beam deals 2 damage to target creature and each other creature that shares a color with it.

Control cards:
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Lhurgoyf] dies, create a 2/2 [black] [Cephalid] creature token
    Rotlung Reanimator:                     Whenever Rotlung Reanimator or another [Rat] dies, create a 2/2 [black] [Cephalid] creature token

Remaining cards:
    Wheel of Sun and Moon:                 If a card would be put into enchanted player's graveyard from anywhere, instead that card is revealed and put on the bottom of that player's library.
    Ancient Tomb:                          Tap: Add two colorless mana to your mana pool. Ancient Tomb deals 2 damage to you.
    Island:                                Land
    Prismatic Omen:                        Lands you control are every basic land type in addition to their other types.
    Steely Resolve:                        As Steely Resolve enters the battlefield, choose a creature type. Creatures of the chosen type have shroud. [Chosen Creature Type: Assembly Worker]
    Dread of Night:                        [Black] creatures get -1/-1.
    Choke:                                 Islands don't untap during their controllers' untap steps.
    Blazing Archon:                        Flying. Creatures can't attack you.
    Dread of Night:                        [Black] creatures get -1/-1.
    Fungus Sliver:                         All [Incarnation] creatures have "Whenever this creature is dealt damage, put a +1/+1 counter on it."
    Shared Triumph:                        As Shared Triumph enters the battlefield, choose a creature type. Creatures of the chosen type get +1/+1. [Choice: Lhurgoyf]
    Shared Triumph:                        As Shared Triumph enters the battlefield, choose a creature type. Creatures of the chosen type get +1/+1. [Choice: Rat]
    Vigor:                                 Trample. If damage would be dealt to another creature you control, prevent that damage. Put a +1/+1 counter on that creature for each 1 damage prevented this way. When Vigor is put into a graveyard from anywhere, shuffle it into its owner's library.
    Mesmeric Orb:                          Whenever a permanent becomes untapped, that permanent's controller puts the top card of their library into their graveyard.
```


# Sources

This project is based on three papers that you can find in the repository:
- [Magic: The Gathering is Turing Complete (Alex Churchill, Stella Biderman and Austin Herrick, 2019)](mtg-turing-machine\documentation\literature\1904.09828.pdf)
- [Small universal Turing machines (Yurii Rogozhin, 1996)](mtg-turing-machine\documentation\literature\1-s2.0-S0304397596000771-main.pdf)
- [Universality of Tag Systems With P = 2 (John Cocke and Marvin Minsky,1964)](mtg-turing-machine\documentation\literature\1p15-cocke.pdf)
