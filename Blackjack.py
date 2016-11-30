# Mini-project #6 - Blackjack

import simpleguitk as simplegui
import random

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
player_score = 0
dealer_score = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

DECKb = []
last_card = True

# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
        canvas.draw_text("Blackjack", [150, 75], 46, "orange")
        canvas.draw_text("Dealer Hand", [150, 125], 18, "black")
        canvas.draw_text("Player Hand", [150, 275], 18, "black")

        if in_play == True:
            canvas.draw_text("Hit or Stand?", [350, 275], 18, "black")
        else:
            canvas.draw_text("New Deal?", [350, 275], 18, "black")

        canvas.draw_text("Player Score: " + str(player_score), [400, 60], 18, "black")
        canvas.draw_text("Dealer Score: " + str(dealer_score), [400, 80], 18, "black")

        canvas.draw_text("Hand is " + str(My_hand.get_value()), [150, 293], 18, "orange")
        canvas.draw_text("Hand is " + str(Dealer_hand.get_value()), [150, 143], 18, "orange")
        
        
        canvas.draw_text(outcome, [150, 500], 36, "orange")

# define hand class
class Hand:
    def __init__(self):
        self.hand = []    # create Hand object

    def __str__(self):
        hand_string = ""
        for i in self.hand:
            hand_string += str(i) + " "
        return "Hand contains " + hand_string  # return a string representation of a hand

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)    

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video
       
        hand = ""
        for i in self.hand:
            hand += str(i) + " "
       
        hand_value = 0
        
        for char in hand:    
            for rank in VALUES:
                if rank in char:
                    hand_value += VALUES[rank]
       
        if any('A' in card for card in hand):
            if hand_value + 10 <= 21:
                return hand_value + 10
            else:
                return hand_value
        else:
            return hand_value

    def draw(self, canvas, pos):
        for card in self.hand:
            draw_card = Card(card[0], card[1])
            draw_card.draw(canvas, pos)
            pos[0] += CARD_SIZE[0] + 10
        
# define deck class 
class Deck:
    def __init__(self):
        global DECKb
        """
        DECKb is created so that deck is not reshuffled
        afer every new game. The entire Deck must be played 
        until a new Deck is used and reshuffled.
        """
        if last_card == True:
            self.deck_cards = []
            for suit in SUITS:
                for rank in RANKS:
                    self.deck_cards.append(suit + rank)
            DECKb = self.deck_cards
        else:
            self.deck_cards = DECKb

    def shuffle(self):
        # shuffle the deck 
        random.shuffle(self.deck_cards)    # use random.shuffle()

    def deal_card(self):
        """
        Returns the last card of the deck 
        (appending to either dealer hand or player hand) 
        and removing it from the deck.
        """
        return self.deck_cards.pop()

    def deck_cards_list(self):
        return self.deck_cards

    def __str__(self):
        s = ""
        for i in self.deck_cards:
            s += str(i) + " "
        return "Deck contains " + s  

def deal():
    global outcome, in_play, My_hand, Shared_deck_cards, Dealer_hand, dealer_score, last_card
        
    in_play = True

    My_hand = Hand()
    Dealer_hand = Hand()
    Shared_deck_cards = Deck()

    if last_card == True:
        Shared_deck_cards.shuffle()

    My_hand.add_card(Shared_deck_cards.deal_card())
    My_hand.add_card(Shared_deck_cards.deal_card())

    if len(Shared_deck_cards.deck_cards_list()) > 0:
        last_card = False

    print "My hand is " + str(My_hand.get_value())

    Dealer_hand.add_card(Shared_deck_cards.deal_card())
    Dealer_hand.add_card(Shared_deck_cards.deal_card())

    print "Dealer hand is " + str(Dealer_hand.get_value())
    
    if Dealer_hand.get_value() == 21:
        outcome = "Dealer Wins!"
        dealer_score += 1
        in_play = False
        deal()
    outcome = ""
    
def hit():
    global in_play, dealer_score, player_score, outcome
    # if the hand is in play, hit the player
    if in_play == True and My_hand.get_value() <= 21:
        My_hand.add_card(Shared_deck_cards.deal_card())
        # The following print statements are for debugging purposes
        print
        print My_hand
        print "Your hand " + str(My_hand.get_value())
        if My_hand.get_value() > 21:
            outcome = "You have busted!"
            in_play = False
            dealer_score += 1
        """      
        elif My_hand.get_value() == 21:
            outcome = "You Win!"
            in_play = False
            player_score += 1
        """
        """
        else:
            outcome = "You Win!"
            in_play = False
            player_score += 1
        """
    else:   
        return

       
def stand():
    global in_play, dealer_score, player_score, outcome
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    if in_play == True:
        while Dealer_hand.get_value() <= 17:
            Dealer_hand.add_card(Shared_deck_cards.deal_card())   
        else:
            print "Dealer hand is " + str(Dealer_hand.get_value())
            
    if My_hand.get_value() == 21 and Dealer_hand.get_value() > 21:
        outcome = "You Win!"
        
    elif Dealer_hand.get_value() > 21:
        outcome = "Dealer has busted! You win!"
        player_score += 1
        
    elif Dealer_hand.get_value() >= My_hand.get_value():
        outcome = "Dealer Wins!"
        dealer_score += 1
        
    else:
        outcome = "You Win!"
        player_score += 1

    in_play = False

# draw handler    
def draw(canvas): 
    My_hand.draw(canvas, [150, 300])
    Dealer_hand.draw(canvas, [150, 150])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)


# get things rolling
deal()
frame.start()
