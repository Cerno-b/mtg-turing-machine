import queue
import copy

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
    "S": "Sliver",
    "<": "Lhurgoyf",  # left end of tape marker
    ">": "Rat"  # right end of tape marker
}

GREEN = "green"
WHITE = "white"

XATHRID_NECROMANCER = "Xathrid Necromancer"
ROTLUNG_REANIMATOR = "Rotlung Reanimator"
INFEST = "Infest"
CLEANSING_BEAM = "Cleansing Beam"
COALITION_VICTORY = "Coalition Victory"
SOUL_SNUFFERS = "Soul Snuffers"
CLOAK_OF_INVISIBILITY = "Cloak of Invisibility"


class Player:
    def __init__(self):
        self.library = queue.Queue()
        self.hand = []
        self.table_tape = set()
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
    def __init__(self, creature_type, color, power_toughness, tapped=False):
        if creature_type in TOKEN_LOOKUP:
            self.creature_type = TOKEN_LOOKUP[creature_type]
        else:
            self.creature_type = creature_type
        self.color = color
        self.power_toughness = power_toughness
        self.tapped = tapped
        self.attached_card = None

    def attach_card(self, card):
        self.attached_card = card

    def detach_card(self):
        attached_card = self.attached_card
        self.attached_card = None
        return attached_card

class Card:
    def __init__(self, name, *, text, tapped=False, phased_in=False):
        assert text
        assert name
        self.name = name
        self.tapped = tapped
        self.text = text
        self.phased_in = phased_in
        self.attached_card = None
        self.traits = {}

    def attach_card(self, card):
        self.attached_card = card

    def detach_card(self):
        attached_card = self.attached_card
        self.attached_card = None
        return attached_card

class MagicTheGatheringTuringMachine:
    """The Magic: The Gathering Turing Machine. The current version does not run any simulations, so
    it is only used to convert a UTM(2,18) to its corresponding card representation."""

    def __init__(self, utm):
        """Arguments:
            utm: A UTM(2,18)"""
        assert isinstance(utm, UniversalTuringMachine)

        self._utm = utm

        self.alice = Player()
        self.bob = Player()

        self.set_up_tape(utm)
        self.set_up_controllers(utm)
        self.set_up_remaining_cards()
        self.set_up_libraries()

        self.stopped = False

    def print_tape(self):
        sorted_tokens = sorted(self.bob.table_tape, key=lambda t: t.power_toughness)
        for token in sorted_tokens:
            print(token.creature_type, end="")
            # slip in Alice's head token
            if token.power_toughness == 3 and token.color == GREEN:
                alice_token = list(self.alice.table_tape)[0]
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
        left_tape = ["<"] + tape[0:index]  # < and > are end of tape markers
        head_tape = tape[index]
        right_tape = tape[index+1:] + [">"]
        left_tape.reverse()

        token_tape = set()
        for i, symbol in enumerate(left_tape):
            # represent a token by (creature_type, color, power/toughness)
            token = Token(symbol, GREEN, i + 3)  # 2/2 token is under the head, so the left neighbor has 3/3
            token_tape.add(token)

        for i, symbol in enumerate(right_tape):
            # represent a token by (creature_type, color, power/toughness)
            token = Token(symbol, WHITE, i + 3)  # 2/2 token is under the head, so the right neighbor has 3/3
            token_tape.add(token)
        assert len(token_tape) + 1 == len(tape)

        head_token = Token(head_tape, WHITE, 2)  # 2/2 token is under the head

        # At this point, the order of the tape symbols is represented by the token's power and toughness, so it is not
        # necessary to keep the token tape in order.

        # Todo: make sure to give Alice or Bob the appropriate tokens: Should Alice get the one to the left of the head?

        name = "Illusory Gains"
        text = "Enchant creature. You control enchanted creature. Whenever a creature enters the battlefield under an opponent's control, attach Illusory Gains to that creature."
        enchantment = Card(name, text=text)
        head_token.attach_card(enchantment)

        self.alice.table_tape.add(head_token)
        self.bob.table_tape = token_tape

    def decode_tape(self):
        # todo decode to UTM character set + index
        utm_tape = []
        index = 0
        left_tape = utm_tape[0:index]
        right_tape = utm_tape[index:]
        tape_string = left_tape + ["^"] + right_tape
        self._utm.overwrite_tape_string(tape_string)

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
                color = WHITE if head_dir == "L" else GREEN

            if name == ROTLUNG_REANIMATOR:
                text = f"Whenever Rotlung Reanimator or another [{trigger_type}] dies, create a 2/2 [{color}] [{target_type}] creature token"
                gen_token = Token(target_type, color, 2, tapped=False)
            elif name == XATHRID_NECROMANCER:
                text = f"Whenever Xathrid Necromancer or another [{trigger_type}] creature you control dies, create a tapped 2/2 [{color}] [{target_type}] creature token."
                gen_token = Token(target_type, color, 2, tapped=True)
            else:
                assert False

            controller_card = Card(name, text=text, phased_in=phased_in)
            controller_card.traits["trigger"] = read_symbol
            controller_card.traits["gen_token"] = gen_token

            name = CLOAK_OF_INVISIBILITY
            text = "Enchanted creature has phasing and can't be blocked except by Walls."
            attachment = Card(name, text=text)
            controller_card.attach_card(attachment)

            control_cards.append(controller_card)

        # add two special controllers that create more tokens once the end of the tape is reached.
        # the cards do not phase like the rest
        special_controllers = [
            ("<", "<", GREEN),
            (">", ">", WHITE)
            ]

        for read_symbol, write_symbol, color in special_controllers:
            trigger_type = TOKEN_LOOKUP[read_symbol]
            target_type = TOKEN_LOOKUP[write_symbol]
            text = f"Whenever Rotlung Reanimator or another [{trigger_type}] dies, create a 2/2 [{color}] [{target_type}] creature token"
            controller_card = Card(ROTLUNG_REANIMATOR, text=text)
            controller_card.traits["trigger"] = read_symbol
            controller_card.traits["gen_token"] =Token(target_type, color, 2, tapped=False)
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
            (ROTLUNG_REANIMATOR, "Whenever Rotlung Reanimator or another [Lhurgoyf] dies, create a 2/2 black [Cephalid] creature token."),
            (ROTLUNG_REANIMATOR, "Whenever Rotlung Reanimator or another [Rat] dies, create a 2/2 black [Cephalid] creature token."),
            ("Shared Triumph", "As Shared Triumph enters the battlefield, choose a creature type. Creatures of the chosen type get +1/+1. [Choice: Lhurgoyf]"),
            ("Shared Triumph", "As Shared Triumph enters the battlefield, choose a creature type. Creatures of the chosen type get +1/+1. [Choice: Rat]"),
            ("Vigor", "Trample. If damage would be dealt to another creature you control, prevent that damage. Put a +1/+1 counter on that creature for each 1 damage prevented this way. "
                      "When Vigor is put into a graveyard from anywhere, shuffle it into its owner's library."),
            ("Mesmeric Orb", "Whenever a permanent becomes untapped, that permanent's controller puts the top card of their library into their graveyard."),
            ("Ancient Tomb", "Tap: Add two colorless mana to your mana pool. Ancient Tomb deals 2 damage to you."),
            ("Prismatic Omen", "Lands you control are every basic land type in addition to their other types."),
            ("Choke", "Islands don't untap during their controllers' untap steps."),
            ("Blazing Archon", "Flying. Creatures can't attack you."),
        ]

        for name, text in alice_cards:
            card = Card(name, text=text)
            self.alice.table_rest.append(card)

        card = Card("Island", text="Land", tapped=True)
        self.alice.table_rest.append(card)

        bob_cards = [
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

        self.alice.hand = Card(INFEST, text="All creatures get -2/-2 until end of turn.")

    def set_up_libraries(self):
        """Set up the players libraries. Since only Alice has cards in play, Bob's library is empty."""
        alice_library = [
            # INFEST is in Alice's hand when the machine starts
            (CLEANSING_BEAM, "Cleansing Beam deals 2 damage to target creature and each other creature that shares a color with it."),
            (COALITION_VICTORY, "You win the game if you control a land of each basic land type and a creature of each color"),
            (SOUL_SNUFFERS, "When Soul Snuffers enters the battlefield, put a -1/-1 counter on each creature.")
        ]

        for name, text in alice_library:
            card = Card(name, text=text)
            self.alice.library.put(card)

    def step_infest(self):
        """Infest will give all creatures -2/-2, destroying Bob's 2/2 token which then triggers
        a single Rotlung Reanimator or Xathrid Necromancer, which in turn will create a new 2/2 token based on the
        UTM rule set. Illusory gains will give the new token to Alice, while returning the token
        previously held by Alice back to Bob"""
        for token in self.bob.table_tape:
            if token.power_toughness == 2:
                self.bob.table_tape.remove(token)
                for card in self.bob.table_control:
                    if card.traits["trigger"] == token.creature_type:
                        new_token = copy.copy(card.traits["gen_token"])  # new token belongs to Bob

                        # move Illusory Gains to new token
                        alice_head = list(self.alice.table_tape)[0]
                        illusory_gains = alice_head.detach()  # this now belongs to Bob
                        new_token.attach(illusory_gains)  # this now belongs to Alice
                        assert illusory_gains.name == "Illusory Gains"

                        self.alice.table_tape.remove(alice_head)
                        self.alice.table_tape.add(new_token)
                        self.bob.table_tape.add(alice_head)


    def step_cleansing_beam(self):
        """Cleansing Beam deals 2 damage to target creature and each other creature of the same color.
        Bob's cards are protected by Privileged Positions and most of Alice's cards are edited to be Assembly Workers
        which are protected by Steely Resolve. The only remaining possible target card is Alice's head token, which
        is either white or green depending on the previous turn (Infest). If the token is white, Cleansing Beam
        deals 2 damage to all white creatures, which is converted to two +1/+1 counters by Vigor instead.
        So now all white tokens have +2/+2. Later all tokens will receive -1/-1.
        This will lead to all white tokens having received +1/+1 and all green tokens having received -1/-1,
        which corresponds to a single Turing head movement to the left.
        Vice-versa for green tokens and movement to the right."""
        head_token = list(self.alice.table_tape)[0]
        for token in self.bob.table_tape:
            if token.color == head_token.color:
                token.power_toughness += 2
        head_token.power_toughness += 2

    def step_coalition_victory(self):
        pass

    def step_soul_snuffers(self):
        """Soul Snuffers performs the second part of the head movement (read the step_infest() comment).
        It gives all creatures -1/-1, so all tokens that received +2+/+2 previously, now have +1/+1. In order to
        prevent non-token creatures from being destroyed, they receive all colors from Prismatic Lace during the
        setup (not simulated here). This allows them to receive +2/+2 from cleansing beam as well, which offsets
        the -1/-1 received here. This does not work for Vigor, though.
        That card however is protected by the edited Fungus Sliver.
        This simulation will only adapt the tokens' counters for simplicity."""
        head_token = list(self.alice.table_tape)[0]
        head_token.power_toughness -= 1
        for token in self.bob.table_tape:
            token.power_toughness -= 1

    def untap_alice(self):
        """In case the Infest step has triggered a Xathrid Necromancer, Alice's head token is now tapped.
        It untaps during her next untap step, which causes Mesmeric Orb to trigger and put the next card from the top
        of her library to the graveyard, which is redirected to the bottom of her library by Wheel of Sun and Moon.
        This card must be Coalition Victory. This causes the turn order to shift by one, which leads to the other set
        of phased cards to become active. Alice has no lands to untap in this step due to Choke.

        It gets a bit more complicated though. The untap step comes before the upkeep step, which would cause
        Coalition Victory to go to the bottom of the library before Cleansing Beam. This would mess up the order
        of the library. Due to a detail in the rules, it still works out. Here is how:

        - During the untap step, Mesmeric Orb triggers. The rules state that any abilities triggered during the
        untap step are delayed until the upkeep step.
        - During the upkeep step, Wild Evocation triggers. It goes to the stack at the same time as Mesmeric Orb.
        - Since Alice has priority, her Mesmeric Orb goes to the stack first, then Wild Evocation.
        - This causes Wild Evocation to resolve first, which sends Cleansing Beam to the bottom of the library
        first, followed by Coalition Victory.

        To keep things simple, this function should be called during the upkeep step after Wild Evocation triggered.
        This simulates the behavior described above.
        """
        head_token = list(self.alice.table_tape)[0]
        if head_token.tapped:
            head_token.tapped = False
            top_library_card = self.alice.library.get()
            assert top_library_card.name == COALITION_VICTORY
            self.alice.library.put(COALITION_VICTORY)

    def step(self):
        # ------------
        # Alice's turn
        # ------------

        # == BEGINNING PHASE ==

        # -- untap step --

        # -- upkeep step --
        # Wild Evocation forces Alice to play her only card in hand
        # Wheel of Sun and Moon forces her to put the card at the bottom of her library instead of her graveyard
        assert(len(self.alice.hand) == 1)
        hand_card = self.alice.hand[0]
        self.alice.library.put(hand_card)
        self.alice.hand = []

        if hand_card.name == INFEST:
            self.step_infest()
        elif hand_card.name == CLEANSING_BEAM:
            self.step_cleansing_beam()
        elif hand_card.name == COALITION_VICTORY:
            self.step_coalition_victory()
        elif hand_card.name == SOUL_SNUFFERS:
            self.step_soul_snuffers()
        else:
            assert False

        # Here is where it gets a bit complicated: Read the comment in the untap_alice function on why the function
        # is called here and not during the untap step.
        self.untap_alice()

        # -- draw step --
        assert len(self.alice.hand) == 0
        self.alice.hand.append(self.alice.library.get())

        # == MAIN_PHASE 1 == (nothing to do: no mana)
        # == COMBAT_PHASE == (nothing to do: Blazing Archon)
        # == MAIN PHASE 2 == (nothing to do: no mana)
        # == ENDING PHASE == (nothing to do)

        # ----------
        # Bob's turn
        # ----------

        # == BEGINNING PHASE ==

        # -- untap step --
        for card in self.bob.table_control:
            if card.attached_card is not None:
                assert card.attached_card.name == CLOAK_OF_INVISIBILITY
                card.phased_in = not card.phased_in

        # -- upkeep step -- (nothing to do)

        # -- draw step -- (nothing to do: Recycle)

        # == MAIN_PHASE 1 == (nothing to do: hand is empty)
        # == COMBAT_PHASE == (nothing to do: Blazing Archon)
        # == MAIN PHASE 2 == (nothing to do: hand is empty)
        # == ENDING PHASE == (nothing to do)

    def run(self):
        while not self.stopped:
            self.step()

    def get_utm(self):
        self.decode_tape()
        return self._utm