import copy

from collections import deque

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
    "c2": "S",
    "-": "-"
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
    ">": "Rat",  # right end of tape marker
    "-": "Assassin"  # trigger win condition to stop the UTM
}

GREEN = "green"
WHITE = "white"
BLACK = "black"
BLUE = "blue"

XATHRID_NECROMANCER = "Xathrid Necromancer"
ROTLUNG_REANIMATOR = "Rotlung Reanimator"
INFEST = "Infest"
CLEANSING_BEAM = "Cleansing Beam"
COALITION_VICTORY = "Coalition Victory"
SOUL_SNUFFERS = "Soul Snuffers"
CLOAK_OF_INVISIBILITY = "Cloak of Invisibility"


class Queue(deque):
    """Wrapper for the normal deque that allows access like queue, but retains the benefit
    of having an iterable queue"""
    def put(self, element):
        self.appendleft(element)

    def get(self):
        return self.pop()


class Player:
    def __init__(self):
        self.library = Queue()
        self.hand = None  # Alice can only have one card at a time. Bob can't have any cards
        self.table_tape = set()
        self.table_control = set()
        self.table_rest = set()
        self.win = False

    def print(self):
        print("Hand:")
        if self.hand:
            print("    " + self.hand.name)
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
        print()


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
    def __init__(self, name, *, text, tapped=False, phased_in=True):
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

        self.state = 0  # keep track of state for printing
        self.cycles = 0

    def get_tape_sorted(self):
        tape = list(self.bob.table_tape)
        tape.append(list(self.alice.table_tape)[0])

        left_tokens = [t for t in tape if t.color == GREEN]
        special_token = [t for t in tape if t.color == BLUE]  # at the end, the blue Assassin marks the head position
        right_tokens = [t for t in tape if t.color == WHITE]

        sorted_left_tokens = sorted(left_tokens, key=lambda t: t.power_toughness, reverse=True)
        sorted_right_tokens = sorted(right_tokens, key=lambda t: t.power_toughness)
        return sorted_left_tokens + special_token + sorted_right_tokens

    def print_tape(self):
        sorted_tape = self.get_tape_sorted()
        print(f"cycle {self.cycles}, q{self.state + 1}: ", end="")
        for token in sorted_tape:
            if token.power_toughness == 2:
                print(f"[{token.creature_type}]", end="")
            else:
                print(token.creature_type, end="")
        print()

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
        assert len(token_tape) + 1 - 2 == len(tape)  # +1 (head treated separately), -2 (the end of tape markers)

        head_token = Token(head_tape, WHITE, 2)  # 2/2 token is under the head, color does not matter at this point
        token_tape.add(head_token)

        # At this point, the order of the tape symbols is represented by the token's power and toughness, so it is not
        # necessary to keep the token tape in order.

        # give Alice one of the head neighbors (take it away from Bob)
        alice_token = None
        for alice_token in token_tape:
            if alice_token.power_toughness == 3 and alice_token.creature_type not in ["<", ">"]:
                token_tape.remove(alice_token)
                break
        assert alice_token

        name = "Illusory Gains"
        text = "Enchant creature. You control enchanted creature. Whenever a creature enters the battlefield under an opponent's control, attach Illusory Gains to that creature."
        enchantment = Card(name, text=text)
        alice_token.attach_card(enchantment)

        self.alice.table_tape.add(alice_token)
        self.bob.table_tape = token_tape

    def decode_tape(self):
        inverse_token_lookup = {v: k for k, v in TOKEN_LOOKUP.items()}
        tape_sorted = self.get_tape_sorted()
        decoded_tape = []
        for token in tape_sorted:
            # this could be nicer if we could protect the blue Assassin from Cleansing Beam,
            # so that it would have the proper 2/2 that marks the head position.
            if token.power_toughness == 4 and token.color == BLUE:
                decoded_tape.append("^")
            if token.creature_type not in ["<", ">"]:
                decoded_tape.append(inverse_token_lookup[token.creature_type])

        self._utm.overwrite_tape_string(decoded_tape)
        return decoded_tape

    def set_up_controllers(self, utm):
        """Set up the controller cards that encode the UTM(2,18) program"""
        transition = utm.get_transition()

        control_cards = []
        for key, value in transition.items():
            source_state, read_symbol = key
            target_state, write_symbol, head_dir = value

            assert source_state in ["q1", "q2"]
            assert target_state in ["q1", "q2", "-"]
            assert head_dir in ["<", ">", "-"]

            trigger_type = TOKEN_LOOKUP[read_symbol]
            target_type = TOKEN_LOOKUP[write_symbol]
            name = ROTLUNG_REANIMATOR if target_state == source_state else XATHRID_NECROMANCER
            phased_in = True if source_state == "q1" else False
            if target_state == "-":
                color = BLUE
                name = ROTLUNG_REANIMATOR
            else:
                color = WHITE if head_dir == "<" else GREEN

            trigger_type_string = TOKEN_NAME_LOOKUP[trigger_type]
            target_type_string = TOKEN_NAME_LOOKUP[target_type]
            if name == ROTLUNG_REANIMATOR:
                text = f"Whenever Rotlung Reanimator or another [{trigger_type_string}] dies, create a 2/2 [{color}] [{target_type_string}] creature token."
                gen_token = Token(write_symbol, color, 2, tapped=False)
            elif name == XATHRID_NECROMANCER:
                text = f"Whenever Xathrid Necromancer or another [{trigger_type_string}] creature you control dies, create a tapped 2/2 [{color}] [{target_type_string}] creature token."
                gen_token = Token(write_symbol, color, 2, tapped=True)
            else:
                assert False

            controller_card = Card(name, text=text, phased_in=phased_in)
            controller_card.traits["trigger"] = trigger_type
            controller_card.traits["gen_token"] = gen_token

            name = CLOAK_OF_INVISIBILITY
            text = "Enchanted creature has phasing and can't be blocked except by Walls."
            attachment = Card(name, text=text)
            controller_card.attach_card(attachment)

            control_cards.append(controller_card)

        # add two special controllers for Bob that create more tokens once the end of the tape is reached.
        # the cards do not phase like the rest
        special_controllers_bob = [
            ("<", "<", GREEN),
            (">", ">", WHITE)
            ]

        for trigger_type, target_type, color in special_controllers_bob:
            trigger_type_string = TOKEN_NAME_LOOKUP[trigger_type]
            target_type_string = TOKEN_NAME_LOOKUP[target_type]
            text = f"Whenever Rotlung Reanimator or another [{trigger_type_string}] dies, create a 2/2 [{color}] [{target_type_string}] creature token"
            controller_card = Card(ROTLUNG_REANIMATOR, text=text)
            controller_card.traits["trigger"] = trigger_type
            controller_card.traits["gen_token"] = Token(target_type, color, 2, tapped=False)
            control_cards.append(controller_card)

        self.bob.table_control = control_cards

        # add two special controllers for Alice that help adding more tokens once the end of the tape is reached
        special_controllers_alice = [
            ("<", "C", BLACK),
            (">", "C", BLACK)
        ]

        control_cards = []
        for trigger_type, target_type, color in special_controllers_alice:
            trigger_type_string = TOKEN_NAME_LOOKUP[trigger_type]
            target_type_string = TOKEN_NAME_LOOKUP[target_type]
            text = f"Whenever Rotlung Reanimator or another [{trigger_type_string}] dies, create a 2/2 [{color}] [{target_type_string}] creature token"
            controller_card = Card(ROTLUNG_REANIMATOR, text=text)
            controller_card.traits["trigger"] = trigger_type
            controller_card.traits["gen_token"] = Token(target_type, color, 2, tapped=False)
            control_cards.append(controller_card)

        self.alice.table_control = control_cards

    def set_up_remaining_cards(self):
        """Set up the remaining table cards that control the game flow."""
        alice_cards = [
            ("Wheel of Sun and Moon", "If a card would be put into enchanted player's graveyard from anywhere, instead that card is revealed and put on the bottom of that player's library."),
            ("Steely Resolve", "As Steely Resolve enters the battlefield, choose a creature type. Creatures of the chosen type have shroud. [Chosen Creature Type: Assembly Worker]"),
            ("Dread of Night", "[Black] creatures get -1/-1."),
            ("Dread of Night", "[Black] creatures get -1/-1."),
            ("Fungus Sliver", 'All [Incarnation] creatures have "Whenever this creature is dealt damage, put a +1/+1 counter on it."'),
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
            self.alice.table_rest.add(card)

        card = Card("Island", text="Land", tapped=True)
        self.alice.table_rest.add(card)

        bob_cards = [
            ("Wild Evocation", "At the beginning of each player's upkeep, that player reveals a card at random from their hand."
                               "If it's a land card, the player puts it onto the battlefield. Otherwise, the player casts it without paying its mana cost if able."),
            ("Recycle", "Skip your draw step. Whenever you play a card, draw a card. Your maximum hand size is two."),
            ("Privileged Position", "Other permanents you control have hexproof."),
            ("Vigor", "Trample. If damage would be dealt to another creature you control, prevent that damage. Put a +1/+1 counter on that creature for each 1 damage prevented this way. "
                      "When Vigor is put into a graveyard from anywhere, shuffle it into its owner's library."),
            ("Blazing Archon", "Flying. Creatures can't attack you.")
        ]

        for name, text in bob_cards:
            card = Card(name, text=text)
            self.bob.table_rest.add(card)

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

    def trigger_controllers(self, token):
        """This function triggers a Rotlung Reanimator or Xathrid Necromancer based on the token that just died.
        When an end-of-tape marker dies, this function has to be called twice (see comments below). This is done
        via a recursive call. The recursion depth cannot exceed 1 though."""
        for head_control_card in self.bob.table_control:
            if head_control_card.phased_in and head_control_card.traits["trigger"] == token.creature_type:
                new_token = copy.copy(head_control_card.traits["gen_token"])  # new token belongs to Bob

                # Shared Triumph increases power and toughness for end-of-tape tokens.
                # This has to be done because below, a new 2/2 head token will be generated
                # for which the end token is the 3/3 neighbor.
                if new_token.creature_type in ["<", ">"]:
                    new_token.power_toughness += 1

                # move Illusory Gains to new token
                alice_head = list(self.alice.table_tape)[0]
                illusory_gains = alice_head.detach_card()  # this now belongs to Bob
                new_token.attach_card(illusory_gains)  # this now belongs to Alice
                assert illusory_gains.name == "Illusory Gains"

                self.alice.table_tape.remove(alice_head)
                self.alice.table_tape.add(new_token)
                self.bob.table_tape.add(alice_head)

                # in case an end-of tape token (Lhurgoyf "<" or Rat ">") was created, Alice's Rotlung Reanimator
                # triggers and creates a 2/2 Cephalid token, which marks the blank symbol, so a new blank tape
                # field is added here. Due to Dread of Night, the Cephalid immediately dies, which now triggers
                # the proper control card to do the actual write operation
                if new_token.creature_type in ["<", ">"]:
                    for alice_control_card in self.alice.table_control:
                        if alice_control_card.traits["trigger"] == new_token.creature_type:
                            new_token = copy.copy(alice_control_card.traits["gen_token"])  # Cephalid, will die immediately
                            self.trigger_controllers(new_token)

    def step_infest(self):
        """Infest will give all creatures -2/-2, destroying Bob's 2/2 token which then triggers
        a single Rotlung Reanimator or Xathrid Necromancer, which in turn will create a new 2/2 token based on the
        UTM rule set. Illusory gains will give the new token to Alice, while returning the token
        previously held by Alice back to Bob"""
        for token in copy.copy(self.bob.table_tape):
            if token.power_toughness == 2:
                self.bob.table_tape.remove(token)
                self.trigger_controllers(token)

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
        """The machine halts when Alice wins the game. Coalition Victory immediately does so if Alice has lands
        of every color and creatures of every color. The first condition is always true due to Prismatic Omen.
        The second condition is almost true, since all her creatures have been given all colors except blue
        via Prismatic Lace during the set up step. The missing blue creature is generated by the Turing machine if
        a Rhino "c1<" is read in state q1. The corresponding Rotlung Reanimator creates a blue Assassin, which will
        trigger the win condition of Coalition Victory in this step."""
        if list(self.alice.table_tape)[0].color == BLUE:
            self.alice.win = True

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
        of the library. But a detailed look at the rules clarifies that the order is actually different:

        - During the untap step, Mesmeric Orb triggers. The rules state that any abilities triggered during the
        untap step are delayed until the upkeep step.
        - During the upkeep step, Wild Evocation triggers. It goes to the stack at the same time as Mesmeric Orb.
        - Since Alice has priority, her Mesmeric Orb goes to the stack first, then Wild Evocation.
        - This causes Wild Evocation to resolve first, which sends Cleansing Beam to the bottom of the library.
        - Next, Mesmeric Orb resolves and sends Coalition Victory to the bottom of the library.
        """
        head_token = list(self.alice.table_tape)[0]
        if head_token.tapped:
            head_token.tapped = False
            return True
        return False

    def step(self, verbose):
        # ------------
        # Alice's turn
        # ------------

        # == BEGINNING PHASE ==

        # -- untap step --
        card_untapped = self.untap_alice()

        # -- upkeep step --
        # Wild Evocation forces Alice to play her only card in hand
        # Wheel of Sun and Moon forces her to put the card at the bottom of her library instead of her graveyard
        assert self.alice.hand is not None

        if self.alice.hand.name == INFEST:
            if verbose:
                self.print_tape()
            self.step_infest()
        elif self.alice.hand.name == CLEANSING_BEAM:
            self.step_cleansing_beam()
        elif self.alice.hand.name == COALITION_VICTORY:
            self.step_coalition_victory()
        elif self.alice.hand.name == SOUL_SNUFFERS:
            self.step_soul_snuffers()
            self.cycles += 1
        else:
            assert False

        self.alice.library.put(self.alice.hand)
        self.alice.hand = None

        # Trigger Mesmeric Orb. Read the comments in the untap_alice() function on why this is delayed to here.
        if card_untapped:
            top_library_card = self.alice.library.get()
            assert top_library_card.name == COALITION_VICTORY
            self.alice.library.put(top_library_card)
            self.state = (self.state + 1) % 2

        if self.alice.win:
            return

        # -- draw step --
        assert self.alice.hand is None
        self.alice.hand = self.alice.library.get()

        # == MAIN_PHASE 1 == (nothing to do: no mana)
        # == COMBAT_PHASE == (nothing to do: Blazing Archon)
        # == MAIN PHASE 2 == (nothing to do: no mana)
        # == ENDING PHASE == (nothing to do)

        # ----------
        # Bob's turn
        # ----------

        # == BEGINNING PHASE ==

        # -- untap step --
        # Phase in the other set of cards.
        # The control cards are used every fourth turn so phasing them out every second turn has no effect.
        # If a state change occurs, the 4-turn cycle is reduced to 3 turns, which will cause the other set
        # of control cards to appear in the turn when they are used.
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

    def run(self, verbose=False):
        while not self.alice.win:
            self.step(verbose)

    def get_utm(self):
        self.decode_tape()
        return self._utm
