import queue

from .universal_turing_machine import UniversalTuringMachine

# Map the UTM(2,18) symbols to single letter representations of creature types
TOKEN_LOOKUP = {
    "1": "A",
    "1>": "B",
    "1<": "C",
    "11>": "D",
    "11<": "E",
    "b": "F",
    "b>": "G",
    "b<": "H",
    "b1>": "I",
    "b1<": "J",
    "b2": "K",
    "b3": "L",
    "c": "M",
    "c>": "N",
    "c<": "O",
    "c1>": "P",
    "c1<": "R",
    "c2": "S"
}

# Map the single letter representations to the full creature type
TOKEN_NAME_LOOKUP = {
    "A": "Aetherborn",
    "B": "Basilisk",
    "C": "Cephalid",
    "D": "Demon",
    "E": "Elf",
    "F": "Faerie",
    "G": "Giant",
    "H": "Harpy",
    "I": "Illusion",
    "J": "Juggernaut",
    "K": "Kavu",
    "L": "Leviathan",
    "M": "Myr",
    "N": "Noggle",
    "O": "Orc",
    "P": "Pegasus",
    "R": "Rhino",
    "S": "Sliver"
}

GREEN = "g"
WHITE = "w"

XATHRID_NECROMANCER = "Xathrid Necromancer"
ROTLUNG_REANIMATOR = "Rotlung Reanimator"


class Player:
    def __init__(self):
        self.library = queue.Queue()
        self.hand = []
        self.table_tape = []
        self.table_control = []
        self.table_rest = []

    def print(self):
        print("Hand:")
        if self.hand:
            for card in self.hand:
                print("    " + card.name)
        else:
            print("    empty")
        print()
        print("Library:")
        if self.library:
            for card in self.library:
                print("    " + card.name)
        else:
            print("    empty")
        print()
        print("Control cards:")
        for card in self.table_control:
            if card.phased_in:
                print("    " + card.name)
            else:
                print("    " + card.name + " (phased out)")
        print()
        print("Remaining cards:")
        for card in self.table_rest:
            print("    " + card.name)


class Token:
    def __init__(self, creature_type, color, power_toughness):
        if creature_type in TOKEN_LOOKUP:
            self.creature_type = TOKEN_LOOKUP[creature_type]
        else:
            self.creature_type = creature_type
        self.color = color
        self.power_toughness = power_toughness
        self.attached_cards = []

    def attach_card(self, card):
        self.attached_cards.append(card)

class Card:
    def __init__(self, name, *, text, tapped=False, phased_in=False):
        assert text
        assert name
        self.name = name
        self.tapped = tapped
        self.text = text
        self.phased_in = phased_in
        self.attached_cards = []

    def attach_card(self, card):
        self.attached_cards.append(card)

class MagicTheGatheringTuringMachine:
    """The Magic: The Gathering Turing Machine. The current version does not run any simulations, so
    it is only used to convert a UTM(2,18) to its corresponding card representation."""

    def __init__(self, utm):
        """Arguments:
            utm: A UTM(2,18)"""
        assert isinstance(utm, UniversalTuringMachine)

        self.alice = Player()
        self.bob = Player()

        self.set_up_tape(utm)
        self.set_up_controllers(utm)
        self.set_up_remaining_cards()
        self.set_up_libraries()

    def print_tape(self):
        for token in self.bob.table_tape:
            print(token.creature_type, end="")
            # slip in Alice's head token
            if token.power_toughness == 3 and token.color == GREEN:
                alice_token = self.alice.table_tape[0]
                print(f"[{alice_token}]", end="")


    def print(self):
        print("Player: Bob")
        print("-----------")
        self.bob.print()
        print()
        print("Tape tokens ([] marks the head position):")
        print("------------")
        self.print_tape()
        print()
        print("Player: Alice")
        print("-------------")
        self.alice.print()

    def set_up_tape(self, utm):
        """Set up the creature tokens that make up the Turing Machine's tape"""
        tape = utm.get_tape()
        index = utm.get_tape_index()
        left_tape = tape[0:index]
        head_tape = tape[index]
        right_tape = tape[index+1:]
        left_tape.reverse()

        token_tape = []
        for i, symbol in enumerate(left_tape):
            # represent a token by (creature_type, color, power/toughness)
            token = Token(symbol, GREEN, i + 3)  # 2/2 token is under the head, so the left neighbor has 3/3
            token_tape.append(token)
        token_tape.reverse()

        for i, symbol in enumerate(right_tape):
            # represent a token by (creature_type, color, power/toughness)
            token = Token(symbol, WHITE, i + 3)  # 2/2 token is under the head, so the right neighbor has 3/3
            token_tape.append(token)
        assert len(token_tape) + 1 == len(tape)

        head_token = Token(head_tape, WHITE, 2)  # 2/2 token is under the head

        # At this point, the order of the tape symbols is represented by the token's power and toughness, so it is not
        # necessary to keep the token tape in order.

        # Todo: make sure to give Alice or Bob the appropriate tokens: Should Alice get the one to the left of the head?

        name = "Illusory Gains"
        text = "Enchant creature. You control enchanted creature. Whenever a creature enters the battlefield under an opponent's control, attach Illusory Gains to that creature."
        enchantment = Card(name, text=text)
        head_token.attach_card(enchantment)

        self.alice.table_tape = [head_token]
        self.bob.table_tape = token_tape

    def decode_tape(self):
        pass

    def set_up_controllers(self, utm):
        """Set up the controller cards that encode the UTM(2,18) program"""
        transition = utm.get_transition()
        control_cards = []
        for key, value in transition.items():
            source_state, read_symbol = key
            target_state, write_symbol, head_dir = value

            assert source_state in ["q1", "q2"]
            assert target_state in ["q1", "q2"]
            assert head_dir in ["L", "R"]

            trigger_type = TOKEN_LOOKUP[read_symbol]
            target_type = TOKEN_LOOKUP[write_symbol]
            name = ROTLUNG_REANIMATOR if target_state == "q1" else XATHRID_NECROMANCER
            phased_in = True if source_state == "q1" else False
            if target_state == "-":
                color = "blue"
            else:
                color = "white" if head_dir == "L" else "green"

            if name == ROTLUNG_REANIMATOR:
                text = f"Whenever Rotlung Reanimator or another [{trigger_type}] dies, create a 2/2 [{color}] [{target_type}] creature token"
            elif name == XATHRID_NECROMANCER:
                text = f"Whenever Xathrid Necromancer or another [{trigger_type}] creature you control dies, create a tapped 2/2 [{color}] [{target_type}] creature token."
            else:
                assert False

            controller_card = Card(name, text=text, phased_in=phased_in)

            name = "Cloak of Invisibility"
            text = "Enchanted creature has phasing and can't be blocked except by Walls."
            attachment = Card(name, text=text)
            controller_card.attach_card(attachment)

            control_cards.append(controller_card)

        self.bob.table_control = control_cards

    def set_up_remaining_cards(self):
        """Set up the remaining table cards that control the game flow."""
        alice_cards = [
            ("Wheel of Sun and Moon", "If a card would be put into enchanted player's graveyard from anywhere, instead that card is revealed and put on the bottom of that player's library."),
            ("Steely Resolve", "As Steely Resolve enters the battlefield, choose a creature type. Creatures of the chosen type have shroud. [Chosen Creature Type: Assembly Worker]"),
            ("Dread of Night", "[Black] creatures get -1/-1."),
            ("Dread of Night", "[Black] creatures get -1/-1."),
            ("Fungus Sliver", 'All [Incarnation] creatures have "Whenever this creature is dealt damage, put a +1/+1 counter on it."'),
            ("Rotlung Reanimator", "Whenever Rotlung Reanimator or another [Lhurgoyf] dies, create a 2/2 black [Cephalid] creature token."),
            ("Rotlung Reanimator", "Whenever Rotlung Reanimator or another [Rat] dies, create a 2/2 black [Cephalid] creature token."),
            ("Shared Triumph", "As Shared Triumph enters the battlefield, choose a creature type. Creatures of the chosen type get +1/+1. [Choice: Lhurgoyf]"),
            ("Shared Triumph", "As Shared Triumph enters the battlefield, choose a creature type. Creatures of the chosen type get +1/+1. [Choice: Rat]"),
            ("Vigor", "Trample. If damage would be dealt to another creature you control, prevent that damage. Put a +1/+1 counter on that creature for each 1 damage prevented this way. "
                      "When Vigor is put into a graveyard from anywhere, shuffle it into its owner's library."),
            ("Mesmeric Orb", "Whenever a permanent becomes untapped, that permanent's controller puts the top card of their library into their graveyard."),
            ("Ancient Tomb", "Tap: Add two colorless mana to your mana pool. Ancient Tomb deals 2 damage to you."),
            ("Prismatic Omen", "Lands you control are every basic land type in addition to their other types."),
            ("Choke", "Islands don't untap during their controllers' untap steps."),
            ("Blazing Archon", "Flying. Creatures can't attack you.")
        ]

        for name, text in alice_cards:
            card = Card(name, text=text)
            self.alice.table_rest.append(card)

        bob_cards = [
            ("Rotlung Reanimator", "Whenever Rotlung Reanimator or another [Lhurgoyf] dies, create a 2/2 [green] [Lhurgoyf] creature token."),
            ("Rotlung Reanimator", "Whenever Rotlung Reanimator or another [Rat] dies, create a 2/2 [white] [Rat] creature token."),
            ("Wild Evocation", "At the beginning of each player's upkeep, that player reveals a card at random from their hand. "
                               "If it's a land card, the player puts it onto the battlefield. Otherwise, the player casts it without paying its mana cost if able."),
            ("Recycle", "Skip your draw step. Whenever you play a card, draw a card. Your maximum hand size is two."),
            ("Privileged Position", "Other permanents you control have hexproof."),
            ("Vigor", "Trample. If damage would be dealt to another creature you control, prevent that damage. Put a +1/+1 counter on that creature for each 1 damage prevented this way. "
                      "When Vigor is put into a graveyard from anywhere, shuffle it into its owner's library."),
            ("Blazing Archon", "Flying. Creatures can't attack you.")
        ]

        for name, text in bob_cards:
            card = Card(name, text=text)
            self.bob.table_rest.append(card)

    def set_up_libraries(self):
        """Set up the players libraries. Since only Alice has cards in play, Bob's library is empty."""
        alice_library = [
            ("Infest", "All creatures get -2/-2 until end of turn."),
            ("Cleansing Beam", "Cleansing Beam deals 2 damage to target creature and each other creature that shares a color with it."),
            ("Coalition Victory", "You win the game if you control a land of each basic land type and a creature of each color"),
            ("Soul Snuffers", "When Soul Snuffers enters the battlefield, put a -1/-1 counter on each creature.")
        ]

        for name, text in alice_library:
            card = Card(name, text=text)
            self.alice.library.put(card)