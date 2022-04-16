import random
import timeit
import json
from os import path

# setting up pathways needed
current_folder = path.dirname(__file__)
data_test_loc = path.join(current_folder, "data test 1.json")


class Card:
    def __init__(self, value, suit):
        # setting up cards with a value and suit, jacks represented by an 11, queens by a 12, and kings by a 13
        self.value = value
        self.suit = suit

        # allows for quicker comparisons, and is used to define what order the hand is sorted into
        if self.suit == "diamonds":
            self.suit_int = 0
        if self.suit == "hearts":
            self.suit_int = 1
        if self.suit == "clubs":
            self.suit_int = 2
        if self.suit == "spades":
            self.suit_int = 3

        # face cards are worth 10 points, all other cards are worth their face value
        if 10 < self.value:
            self.points = 10
        else:
            self.points = self.value

    def print(self):
        print(f"{self.value}, {self.suit}")


class Deck:
    def __init__(self, decklist=None):
        """defines the deck and then shuffles deck randomly"""
        self.deck = []
        if decklist:
            for i in decklist:
                self.deck.append(Card(i[1], i[0]))
        else:
            for s in ["diamonds", "hearts", "clubs", "spades"]:
                for v in range(1, 14):
                    if v == 13:
                        pass
                    else:
                        self.deck.append(Card(v, s))
        random.shuffle(self.deck)

    def randomize_deck(self):
        random.shuffle(self.deck)

    def new_hand(self, hand_size):
        """draws hand from deck equal to hand size parameter"""
        hand = Hand()
        for i in range(hand_size):
            new_card = self.deck[0]
            self.deck.remove(new_card)
            hand.cards.append(new_card)
        return hand

    def print(self):
        for i in self.deck:
            i.print()


class Hand():
    def __init__(self):
        self.cards = []

    def set_hand(self, card_list):
        """this exists to test particular hands, and uses a list var in this format:
        [[suit, value], [suit, value], ... ]"""
        self.cards = []
        for i in card_list:
            self.cards.append(Card(i[0], i[1]))

    def print(self):
        for i in self.cards:
            i.print()


def hand_sort(sort_list):
    """this function a modified bubble sort that has been changed to not only sort by value, but by suit as well,
    in this order: diamonds, hearts, clubs, spades. It also sorts the cards into their respective suits, and
    sorts them in their individual suits, and returns a sorted list of the whole hand and a list of the suits
    sorted"""

    diamonds = []
    hearts = []
    clubs = []
    spades = []

    # sorting all the cards from sort_list into their respective lists based on their suit
    for card in sort_list:
        if card.suit_int == 0:
            diamonds.append(card)
        if card.suit_int == 1:
            hearts.append(card)
        if card.suit_int == 2:
            clubs.append(card)
        if card.suit_int == 3:
            spades.append(card)

    # defines the unsorted suit list
    suits_list = [diamonds, hearts, clubs, spades]

    has_swapped = True

    while has_swapped:
        has_swapped = False
        # for each card in the full hand, we repeat this procedure
        # j is the index of the card that is being focused on
        for j in range(len(sort_list) - 1):
            # if the current card has a higher value than the card next to it, we swap it
            if sort_list[j].value > sort_list[j + 1].value:
                # Swap
                sort_list[j], sort_list[j + 1] = sort_list[j + 1], sort_list[j]
                # tells the computer to continue repeating this process
                has_swapped = True

            # if card value is the same, swap based on suit in diamonds, hearts, clubs, spades order
            elif sort_list[j].value == sort_list[j + 1].value:
                # assigned a suit int value so they are comparable
                if sort_list[j].suit_int > sort_list[j + 1].suit_int:
                    # swap
                    sort_list[j], sort_list[j + 1] = sort_list[j + 1], sort_list[j]
                    has_swapped = True

    # now we sort the suit list created earlier, by going through each of the suits and sorting them individually
    for i in suits_list:
        has_swapped = True

        while has_swapped:
            has_swapped = False

            # for each card in the current suit, repeat this procedure, j represents the index of the current card
            for j in range(len(i) - 1):
                # if the current card has a higher value than the card to its right, we swap them

                if i[j].value > i[j + 1].value:
                    # Swap
                    i[j], i[j + 1] = i[j + 1], i[j]
                    has_swapped = True
                # no need to sort by suits, as they are already sorted into their respective suits

    return sort_list, suits_list


def check_paired(card1, card2):
    """This function is used to compare two cards and decide whether or not they are paired, and what type of pairing
    they are"""
    # card1 is always to the left of card2
    # if their values are the same, they are considered paired
    if card1.value == card2.value:
        # 1 means that they are paired in a set
        return True, 1
    # if their suits are the same, and card2 is one higher than card1, they are considered paired
    elif card1.suit_int == card2.suit_int:
        if card2.value - card1.value == 1:
            # 2 means that they are paired in a run
            return True, 2
        else:
            # 0 means that they are not paired, but this is a placeholder
            return False, 0
    # anything else, they are not considered paired
    else:
        return False, 0


def pair_hands(hand):
    """This function is used to take a hand and divide it into two lists: one list that defines all the unpaired
    cards, and one that defines all paired cards. First, the function will run through a process that prioritizes runs
    over sets, by first going through all the suits in the suit list and finding all of the runs and adding them to
    the paired cards list, and then going through the rest of the unpaired cards in the normal list and finding all sets.
    The function then does the reverse, prioritizing the """
    num_hand, suit_hand = hand_sort(hand)
    paired_cards = []
    unpaired_cards = []
    runs_num_hand = num_hand.copy()
    runs_suit_hand = suit_hand.copy()
    runs_paired = []
    runs_unpaired = []
    sets_num_hand = num_hand.copy()
    sets_suit_hand = suit_hand.copy()
    sets_paired = []
    sets_unpaired = []

    # we start by first prioritizing the runs, then sets, then we do the opposite, then compare scores, and whichever
    # has a lower score is returned

    # we start by finding the runs in the hand
    for i in range(len(runs_suit_hand)):
        pos_pairs = []
        if len(runs_suit_hand[i]) < 3:
            pass
        else:
            for j in range(len(runs_suit_hand[i])):
                try:
                    card = runs_suit_hand[i][j]
                    check_card = runs_suit_hand[i][j + 1]
                    paired, set_type = check_paired(card, check_card)
                    if paired and set_type == 2:
                        if len(pos_pairs) < 1:
                            pos_pairs.append(card)
                        pos_pairs.append(check_card)
                    else:
                        if len(pos_pairs) >= 3:
                            for c in pos_pairs:
                                runs_paired.append(c)
                                runs_num_hand.remove(c)
                        pos_pairs = []

                except IndexError:
                    pass

            if len(pos_pairs) >= 3:
                for c in pos_pairs:
                    runs_paired.append(c)
                    runs_num_hand.remove(c)
            pos_pairs = []

    # then we find sets of cards

    pos_pairs = []
    if len(runs_num_hand) < 3:
        pass
    else:
        for i in range(len(runs_num_hand)):
            try:
                card = runs_num_hand[i]
                check_card = runs_num_hand[i + 1]
                paired, set_type = check_paired(card, check_card)
                if paired and set_type == 1:
                    if len(pos_pairs) < 1:
                        pos_pairs.append(card)
                    pos_pairs.append(check_card)
                else:
                    if len(pos_pairs) >= 3:
                        for c in pos_pairs:
                            runs_paired.append(c)
                            runs_num_hand.remove(c)
                    pos_pairs = []
            except IndexError:
                if len(pos_pairs) >= 3:
                    for c in pos_pairs:
                        runs_paired.append(c)
                        runs_num_hand.remove(c)
                pos_pairs = []

    # finally we add all unpaired cards to their respective list
    for v in runs_num_hand:
        runs_unpaired.append(v)

    # now we create the other list, where it prioritizes sets over runs
    pos_pairs = []
    for i in range(len(sets_num_hand)):
        try:
            card = sets_num_hand[i]
            check_card = sets_num_hand[i + 1]
            paired, set_type = check_paired(card, check_card)
            if paired and set_type == 1:
                if len(pos_pairs) < 1:
                    pos_pairs.append(card)
                pos_pairs.append(check_card)
            else:
                if len(pos_pairs) >= 3:
                    for c in pos_pairs:
                        sets_paired.append(c)
                        sets_num_hand.remove(c)
                        sets_suit_hand[c.suit_int].remove(c)

                pos_pairs = []
        except IndexError:
            if len(pos_pairs) >= 3:
                for c in pos_pairs:
                    sets_paired.append(c)
                    sets_num_hand.remove(c)
                    sets_suit_hand[c.suit_int].remove(c)
            pos_pairs = []

    pos_pairs = []

    for i in range(len(sets_suit_hand)):
        pos_pairs = []
        if len(sets_suit_hand[i]) < 3:
            pass
        else:
            for j in range(len(sets_suit_hand[i])):
                try:
                    card = sets_suit_hand[i][j]
                    check_card = sets_suit_hand[i][j + 1]
                    paired, set_type = check_paired(card, check_card)
                    if paired and set_type == 2:
                        if len(pos_pairs) < 1:
                            pos_pairs.append(card)
                        pos_pairs.append(check_card)
                    else:
                        if len(pos_pairs) >= 3:
                            for c in pos_pairs:
                                sets_paired.append(c)
                                sets_num_hand.remove(c)
                        pos_pairs = []

                except IndexError:
                    pass

            if len(pos_pairs) >= 3:
                for c in pos_pairs:
                    sets_paired.append(c)
                    sets_num_hand.remove(c)
            pos_pairs = []

    for v in sets_num_hand:
        sets_unpaired.append(v)

    runs_score = 0
    for i in runs_unpaired:
        runs_score += i.points

    sets_score = 0
    for i in sets_unpaired:
        sets_score += i.points

    if sets_score > runs_score:
        paired_cards = runs_paired
        unpaired_cards = runs_unpaired
    elif runs_score >= sets_score:
        paired_cards = sets_paired
        unpaired_cards = sets_unpaired

    return paired_cards, unpaired_cards, suit_hand


data = []
ogdecklist = [["diamonds", 1], ["diamonds", 2], ["diamonds", 3], ["diamonds", 4], ["diamonds", 5], ["diamonds", 6],
              ["diamonds", 7], ["diamonds", 8], ["diamonds", 9], ["diamonds", 10], ["diamonds", 11], ["diamonds", 12],
              ["diamonds", 13], ["spades", 1], ["spades", 2], ["spades", 3], ["spades", 4], ["spades", 5],
              ["spades", 6],
              ["spades", 7], ["spades", 8], ["spades", 9], ["spades", 10], ["spades", 11], ["spades", 12],
              ["spades", 13],
              ["clubs", 1], ["clubs", 2], ["clubs", 3], ["clubs", 4], ["clubs", 5], ["clubs", 6], ["clubs", 7],
              ["clubs", 8], ["clubs", 9], ["clubs", 10], ["clubs", 11], ["clubs", 12], ["clubs", 13], ["hearts", 1],
              ["hearts", 2], ["hearts", 3], ["hearts", 4], ["hearts", 5], ["hearts", 6], ["hearts", 7], ["hearts", 8],
              ["hearts", 9], ["hearts", 10], ["hearts", 11], ["hearts", 12], ["hearts", 13]]
decklist = [["diamonds", 1], ["diamonds", 2], ["diamonds", 3], ["diamonds", 4], ["diamonds", 5], ["diamonds", 6],
              ["diamonds", 7], ["diamonds", 8], ["diamonds", 9], ["diamonds", 10], ["diamonds", 11], ["diamonds", 12],
              ["diamonds", 13], ["spades", 1], ["spades", 2], ["spades", 3], ["spades", 4], ["spades", 5],
              ["spades", 6],
              ["spades", 7], ["spades", 8], ["spades", 9], ["spades", 10], ["spades", 11], ["spades", 12],
              ["spades", 13],
              ["clubs", 1], ["clubs", 2], ["clubs", 3], ["clubs", 4], ["clubs", 5], ["clubs", 6], ["clubs", 7],
              ["clubs", 8], ["clubs", 9], ["clubs", 10], ["clubs", 11], ["clubs", 12], ["clubs", 13], ["hearts", 1],
              ["hearts", 2], ["hearts", 3], ["hearts", 4], ["hearts", 5], ["hearts", 6], ["hearts", 7], ["hearts", 8],
              ["hearts", 9], ["hearts", 10], ["hearts", 11], ["hearts", 12], ["hearts", 13]]

for i in range(1000000):
    deck = Deck(decklist)
    hand = deck.new_hand(10)
    paired_cards, unpaired_cards, suit_hand = pair_hands(hand.cards)
    score = 0
    for i in unpaired_cards:
        score += i.points
    data.append(score)
'''
deck = Deck()
hand = deck.new_hand(10)
paired_cards, unpaired_cards, suit_hand = pair_hands(hand.cards)
score = 0
print("SUIT LISTS:")
print("Diamonds")
for i in suit_hand[0]:
    i.print()
print("Hearts")
for i in suit_hand[1]:
    i.print()
print("Clubs")
for i in suit_hand[2]:
    i.print()
print("Spades")
for i in suit_hand[3]:
    i.print()
print("UNPAIRED CARDS:")
for i in unpaired_cards:
    i.print()
print("PAIRED CARDS:")
for i in paired_cards:
    i.print()
score = 0
for i in unpaired_cards:
    score += i.points
print(f"SCORE: {score}")'''

with open(data_test_loc, 'w') as f:
    json.dump(data, f)
f.close()
