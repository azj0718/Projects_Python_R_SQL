#BLACKJACK GAME THAT MATCHES ONE UP TO SIX- PLAYERS AGAINST THE DEALER!
#Austin Jin

import random
import time
from termcolor import colored, COLORS
#Before executing the program, please make sure that the termcolor module is added to your Anaconda libraries by typing in the following command in your command line: pip install termcolor

ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
suits = ("♢", "♧", "♡", "♤")
s_color = ['white']
p_color = list(k for k in COLORS.keys() if k not in s_color)
maximum_players = len(p_color)

class Card(object):
    """Consists of an individual card that combines one element from both ranks and suits"""

    def __init__(self, rank, suit):
        assert rank in ranks
        self.rank = rank
        assert suit in suits
        self.suit = suit

    def __repr__(self):
        return "{:>2}{}".format(self.rank, self.suit)

    def score(self):
        """Yields the value of the card based on the rules of BlackJack"""
        if self.ace():
            score = 11
        else:
            try:
                score = int(self.rank)
            except ValueError:
                score = 10
        return score

    def ace(self):
        """Performs a check on whether the card is an Ace"""
        return self.rank == "A"

class Deck(object):
    """Represents deck of 52 cards to be dealt to the player and dealer"""

    def __init__(self):
        self.__deck_new()

    def __deck_new(self):
        """This function produces a new deck that consists of 52 cards"""
        self.cards = list(Card(r, s) for r in ranks for s in suits)

    def shuffle(self):
        """This function shuffles the deck of 52 card in a random fashion"""
        random.shuffle(self.cards)

    def deal(self):
        """This function deals out cards starting from the final cards of the deck and creates a new shuffled deck if the deck is empty"""
        if not self.cards:
            self.__deck_new()
            self.shuffle()
        return self.cards.pop()

class Hand(object):
    """Represents the cards held by the player or the dealer"""

    def __init__(self, stake=0):
        self.cards = []
        self.stake = stake
        self.active = True

    def __repr__(self):
        return "  ".join(str(card) for card in self.cards)

    def initial(self):
        """This function yields the initial card of the hand"""
        assert self.cards
        return self.cards[0]

    def final(self):
        """This function yields the final card of the hand"""
        assert self.cards
        return self.cards[-1]

    def card_addition(self, card):
        """This function adds an instance of the card to the hand"""
        self.cards.append(card)

    def score(self):
        """This function calculates the value of the hand and whether there is an Ace"""
        aces = sum(1 for c in self.cards if c.ace())
        score = sum(c.score() for c in self.cards)
        while aces > 0 and score > 21:
            score -= 10
            aces -= 1
        return score

    def blackjack(self):
        """This function checks to see if the hand is BlackJack"""
        return len(self.cards) == 2 and self.score() == 21

    def if_twentyone(self):
        """This function checks to see if the hand has a value of 21"""
        return self.score() == 21

    def over_twentyone(self):
        """This function checks to see if the hand has a value of more than 21 which would be a bust."""
        return self.score() > 21

    def hand_pair(self):
        """This function checks to see if the hand has a pair of the two same cards"""
        return len(self.cards) == 2 and self.initial().rank == self.final().rank

    def hand_split(self):
        """This function checks to see if the hand can be split into two hands"""
        assert self.hand_pair()
        card = self.cards.pop()
        hand = Hand(self.stake)
        hand.card_addition(card)
        return hand

class Player(object):
    """This class represents the dealer and the player(s) of the game"""

    def __init__(self, name, chips, color='red'):
        assert color in p_color
        assert chips > 0
        self.name = name
        self.chips = chips
        self.color = color
        self.hands = []
        self.insurance = 0
        self.conclusion = {'ties': 0, 'wins': 0, 'losses': 0}

    def if_doubledown(self, hand):
        """This function checks if the player(s) is allowed to double-down"""
        return (self.remaining_chips(hand.stake) and
                (len(hand.cards) == 2 or hand.score() in (9, 10, 11)))

    def hand_active(self):
        """This function generates the hand if the player(s) is still active"""
        for hand in self.hands:
            if hand.active:
                yield hand

    def any_active_hands(self):
        """This function checks to see if the player(s) has any remaining, active hands"""
        return list(h for h in self.hands if h.active)

    def split_hands(self, hand):
        """This function checks if the player(s) is allowed to split their hand"""
        return self.remaining_chips(hand.stake) and hand.hand_pair()

    def remaining_chips(self, amount=0):
        """This function checks to see if there are remaining chips left"""
        assert amount >= 0
        if amount == 0:
            return self.chips > 0
        return self.chips >= amount

    def secure(self, bet):
        """This function secures the chips that were bet"""
        assert bet > 0
        self.chips += bet
        self.conclusion['ties'] += 1

    def victory(self, bet, chance=1):
        """This function returns score results for the player's wins"""
        assert bet > 0
        assert chance >= 1
        self.chips += int(bet * (chance + 1))
        self.conclusion['wins'] += 1

    def reduce(self):
        """This function returns score results for the player's losses"""
        self.conclusion['losses'] += 1

    def bet(self, bet):
        """This function reduces the amount of chips if the player has placed a bet"""
        assert bet > 0
        assert self.remaining_chips(bet)
        self.chips -= bet
        return bet

class Game(object):
    """This class provides guidance for the various steps throughout the game"""

    def __init__(self, names, chips):
        self.colors = list(p_color)
        self.playing = False
        self.insurance = False
        self.dealer = None
        self.deck = Deck()
        self.deck.shuffle()
        self.players = list(Player(name, chips, self.__random_color()) for name in names)
        self.max_name_len = max(max(len(name) for name in names), len("Dealer"))

    def __random_color(self):
        """This is a function to retrieve a color from the set of colors in the module termcolors"""
        assert self.colors
        colors = self.colors
        color = random.choice(colors)
        colors.remove(color)
        return color

    def __deal_card(self, name, hand, color="white", declare=True):
        """This function appends a card from the end of the deck to the hand"""
        card = self.deck.deal()
        hand.card_addition(card)
        if declare:
            time.sleep(1)
            cue = "Deals {} which adds up to a value of {:>2}: {}".format(card, hand.score(), hand)
            print(self.text_formatting(name, cue, color))

    def __get_bet(self, player, query, minimum, multiple):
        """This function requires the player to place a bet which is checked through the constraints"""
        print()
        print(self.text_formatting(player.name, query.lower(), player.color))
        cue = "{} available, {} minimum, multiples of {} only".format(
            player.chips, minimum, multiple)
        print(self.text_formatting(player.name, cue, player.color))
        bet = -1
        while bet < minimum or bet > player.chips or bet % multiple != 0:
            bet = input(self.text_formatting(
                player.name, "Please enter an amount ({}): ".format(minimum), player.color))
                #Please keep in mind that you may only enter in amounts of 10
            if bet == '':
                bet = minimum
            else:
                try:
                    bet = int(bet)
                except ValueError:
                    pass
        return bet

    def text_formatting(self, name, text, color="white"):
        """This function provides a color to the player name output prefixed"""
        name = name.rjust(self.max_name_len)
        return colored("{} > {}".format(name, text), color)

    def remainingchips_players(self, min=0):
        """This function yields the players who have remaining chips"""
        return list(p for p in self.players if p.remaining_chips(min))

    def players_active(self):
        """This function yields the players who have remaining, active hands"""
        for player in self.players:
            if player.any_active_hands():
                yield player

    def any_active_hands(self):
        """This function yields the players who have remaining active hands"""
        return list(p for p in self.players if p.any_active_hands())

    def organize(self):
        """This function sets up the game by receiving the player's bets and dealing out two cards each for the dealer and player(s)"""
        hands = []
        self.playing = True
        min_bet = 10
        random.shuffle(self.players)
        players = self.remainingchips_players(min_bet)
        if not players:
            return
        for player in players:
            player.insurance = 0
            bet = self.__get_bet(player, "Enter the number of bets you would like to make: ", min_bet, 2)
            hand = Hand(bet)
            hands.append(hand)
            player.bet(bet)
            player.hands = [hand]
        dealer = Hand(0)
        for _ in range(2):
            for hand in hands:
                self.__deal_card(_, hand, declare=False)
            self.__deal_card(_, dealer, declare=False)
        print()
        for player in players:
            hand = player.hands[0]
            cue = "The following cards were dealt and has a total value of {:>2}: {}".format(hand.score(), hand)
            print(self.text_formatting(player.name, cue, player.color))
        print(self.text_formatting("Dealer", "Face up card is: {}".format(dealer.initial())))
        self.dealer = dealer

    def take_insurance(self):
        """This function allows the player(s) to take insurance if feasible"""
        if self.dealer.initial().ace():
            players = self.remainingchips_players()
            for player in players:
                bet = self.__get_bet(player, "Would you like to take insurance?", 0, 2)
                if bet > 0:
                    player.insurance = player.bet(bet)
                else:
                    player.insurance = 0

    def dealer_scored_blackjack(self):
        """This function checks to see if the dealer scored blackjack and sorts out the placed bets based on the result"""
        dealer = self.dealer
        players = self.players_active()
        if dealer.blackjack():
            self.playing = False
            print()
            print(self.text_formatting("The dealer", "has scored blackjack : {}".format(dealer)))
            for player in players:
                for hand in player.hand_active():
                    if player.insurance:
                        print(self.text_formatting(
                            player.name, "Congratulations! You won your insurance bet!", player.color))
                        player.victory(player.insurance, chance=2)
                    self.determine_outcome(dealer, player, hand)
        elif dealer.initial().ace():
            print()
            print(self.text_formatting("The dealer", "has not scored blackjack."))
            for player in players:
                if player.insurance:
                    print(self.text_formatting(
                        player.name, "Oh no..! You lost your insurance bet!", player.color))
                    player.reduce()

    def player_scored_blackjack(self):
        """This function checks to see if the player scored blackjack and sorts out the placed bets based on the result"""
        players = self.players_active()
        dealer = self.dealer
        for player in players:
            for hand in player.hand_active():
                if hand.blackjack():
                    print(self.text_formatting(player.name, "Congratulations! You scored blackjack!", player.color))
                    self.determine_outcome(dealer, player, hand)

    def determine_outcome(self, dealer, player, hand):
        """This function settles out the result when comparing the player's hand to the dealer's hand"""
        hand.active = False
        if hand.score() > dealer.score() or dealer.over_twentyone():
            conclusion = "Congratulations! :) You have defeated the dealer!"
            if hand.blackjack():
                chance = 1.5
            else:
                chance = 1
            player.victory(hand.stake, chance)
        elif hand.score() == dealer.score():
            conclusion = ":| You have ended up in a tie with the dealer!"
            player.secure(hand.stake)
        else:
            conclusion = "Oh no..! :( You have been defeated by the dealer!"
            player.reduce()
        print(self.text_formatting(player.name, conclusion, player.color))

    def perform_splithand(self, player, hand):
        """This function performs a hand split on the player if feasible"""
        if hand.hand_pair() and player.remaining_chips(hand.stake):
            cue = "Please type in Y for 'Yes' and N for 'No' if you would like to split your pair (Y/N): "
            cue = self.text_formatting(player.name, cue, player.color)
            answer = match_input(cue, ("Y", "N"), "Y")
            if answer == "Y":
                new_hand = hand.hand_split()
                player.bet(hand.stake)
                self.__deal_card(player.name, hand, player.color)
                self.__deal_card(player.name, new_hand, player.color)
                player.hands.append(new_hand)
                self.yield_playerhand(player.name, hand, player.color)

    def append_card(self, player, hand):
        """This function appends a card from the end of the deck to the player's hand and returns a result if feasible"""
        self.__deal_card(player.name, hand, player.color)

    def over_twentyone(self, player, hand):
        """This function performs some protocols if the player is busted"""
        print(self.text_formatting(player.name, "Darn it! You are busted!", player.color))
        player.reduce()
        hand.active = False

    def if_doubledown(self, player, hand):
        """This function allows the player to double-down based on the stakes at hand"""
        player.bet(hand.stake)
        hand.stake += hand.stake
        self.__deal_card(player.name, hand, player.color)
        if hand.over_twentyone():
            self.over_twentyone(player, hand)

    def play_dealersturn(self):
        """This function manages the dealer's turns and provides a result of the game"""
        dealer = self.dealer
        print()
        cue = "Deals {} which adds up to a value of {:>2}: {}".format(
            dealer.final(),
            dealer.score(),
            dealer)
        print(self.text_formatting("Dealer", cue))
        while dealer.score() < 17:
            self.__deal_card("Dealer", dealer)
        if dealer.over_twentyone():
            print(self.text_formatting("The dealer", "has been busted!"))
        for player in self.players_active():
            for hand in player.hand_active():
                self.determine_outcome(dealer, player, hand)

    def conclusion(self):
        """This function yields out the results of the player"""
        print()
        players = sorted(self.players,
                         reverse=True,
                         key=lambda x: (x.chips,
                                        x.conclusion['wins']*3 + x.conclusion['ties'],
                                        -x.conclusion['losses']))
        for player in players:
            conclusion = ",  ".join("{}: {:>2}".format(r, i) for r, i in player.conclusion.items())
            cue = "# of Chips: {:>3},  {}".format(player.chips, conclusion)
            print(self.text_formatting(player.name, cue, player.color))

    def yield_playerhand(self, name, hand, color="white"):
        """This function yields the player's current hand"""
        print()
        cue = "Value of hand is {:>2}: {}".format(hand.score(), hand)
        print(self.text_formatting(name, cue, color))

    def play_remaininghands(self):
        """This function plays out the remaining, active hands until completion"""
        if self.playing:
            for player in self.players_active():
                for hand in player.hand_active():
                    self.play_restofhand(player, hand)
            if self.any_active_hands():
                self.play_dealersturn()

    def play_restofhand(self, player, hand):
        """This function plays out the hand until completion"""
        self.yield_playerhand(player.name, hand, player.color)
        if player.split_hands(hand):
            self.perform_splithand(player, hand)

        while hand.active:
            if hand.if_twentyone():
                print(self.text_formatting(player.name, "Nice! :) You have scored 21!", player.color))
                break
            if hand.over_twentyone():
                self.over_twentyone(player, hand)
                break
            if player.if_doubledown(hand):
                query = "Please choose your next move (D for double-down / S for stand / H for hit): "
                answers = ('H', 'S', 'D')
            else:
                query = "Please choose your next move (S for stand / H for hit): "
                answers = ('H', 'S')

            cue = self.text_formatting(player.name, query, player.color)
            answer = match_input(cue, answers, default='H')
            if answer == 'H':
                if self.append_card(player, hand):
                    break
            elif answer == 'S':
                break
            elif answer == 'D':
                self.if_doubledown(player, hand)
                break
            else:
                # should never get here!
                raise ValueError

def screen_new():
    """This function clears the screen for greater visibility. ANSI escape code for clearing screen from cursor to the end of the screen."""
    print("\033[H\033[J")

def commence_cue():
    """This function clears the screen prior to kicking off a fresh round"""
    print()
    input("Press enter key to continue or Ctrl+C to exit: ")
    screen_new()

def match_input(query, accepted, default):
    """This function gets input that matches the accepted answers"""
    while True:
        answer = input(query).upper()
        if answer == '':
            answer = default
        if answer in accepted:
            break
    return answer

def begin_program():
    """This function is brought up at the beginning of the game for the name of the player(s) and the amount of chips"""
    while True:
        cue = "Provide up to less than {} player names or press enter to continue as single-player (If more than one player, seperate each name by a space): "
        names = input(cue.format(maximum_players))
        if names == '':
            names = ["Player"]
        else:
            names = names.split(' ')
        if len(names) > maximum_players:
            print("Maximum of {} players only please!".format(maximum_players))
        else:
            break

    print()
    chips = input("Enter starting number of chips (Default is 100): ")
    if chips == '':
        chips = 100
    else:
        chips = int(chips)
    return Game(names, chips)

def main():
    """This function executes the main screen of the game in a loop"""
    screen_new()
    print("""
          ---------------------
          Welcome to Blackjack!
          ---------------------
History: Blackjack, formerly known as Black Jack and Vingt-Un, is the American member of a global family of banking games known as Twenty-One, whose relatives include the British game of Pontoon and the European game, Vingt-et-Un.

Instructions: The program will start by collecting names of the player(s) and asking for a chip balance. Then the computer dealer will deal out an initial set of cards and for each hand, the player(s) will have to either offer split, double down, hit or stand as appropriate. If the player is busted or the dealer either busts or stands, then the game will finish and move to the next round. The program will keep track of the score by showing results per round and asking to settle bets until the chip balance reaches zero. Good luck and have fun!
    """)

    #Objective of the game is acquire cards with a face value that is as close as possible to 21 without going over
    #The player may either play with others or against the computer dealer. If there are other players to be included in the game, the program will collect name(s) of those players and start by asking for a chip balance
    #Once the player name(s), chip balance, and amount of chips to bet are provided, the dealer will deal the initial set of cards
    #Then, the player(s) will have the option of splitting, doubling down, hitting, or standing per hand
    #The dealer will continue playing until busted or until the player stands
    #When each session is completed, the results of the game will show and allow the player(s) to settle bets per match until their chip balance ends up in 0
    #The program will keep track of the scores throughout the duration of all games and print out a scoreboard at the exit of the program with the amount of chips remaining per player along with the number of wins, ties, and losses

    # The following try, except, and finally clauses are to kick off the program by collecting the player(s) names and chip balance

    try:
        print()
        game = begin_program()

        while True:
            commence_cue()
            if not game.remainingchips_players(10):
                print("Game over! The player(s) don't have any remaining chips!")
                break
            game.organize()
            game.player_scored_blackjack()
            game.dealer_scored_blackjack()
            game.play_remaininghands()
            game.take_insurance()

    except KeyboardInterrupt:
        print()
    finally:
        if game:
            game.conclusion()
        print()
        print("Hope you had fun and thanks for playing BlackJack!")
        print()

if __name__ == '__main__':
    main()

#The overall program is less than 500 lines if comments are excluded