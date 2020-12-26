import random
import itertools
from card import Card

def shuffle_deck():
	"""Generate a shuffled (randomized) deck of 52 unique cards."""
	deck = []
	suits = ["Hearts","Diamonds","Clubs","Spades"]
	values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
	all_cards =  list(itertools.product(suits,values)) #generate all possible card combinations
	random.shuffle(all_cards) #randomize the card combinations
	
	# Generate the randomized deck of cards
	for i in range(len(all_cards)):
		new_card = Card(all_cards[i][0],all_cards[i][1])

		deck.append(new_card)

	return deck #return the randomized deck of cards

def start_new_hand():
	"""Initialize a new hand of Rummy 500."""
	deck = shuffle_deck() #get a new deck
	hand_size = 10 #10 cards dealt to each player
	player1_hand = [] #empty player 1 hand
	player2_hand = [] #empty player 2 hand
	discard_line = [] #empty discard line (on the tabletop)

	# Deal cards to player hands from the deck
	for i in range(hand_size):
		player1_hand.append(deck.pop(0))
		player2_hand.append(deck.pop(0))

	# Flip the top card of the deck onto the table top to start the discard line
	discard_line.append(deck.pop(0))

	return deck,discard_line,player1_hand,player2_hand

def has_triplet(player_hand):
	"""Check if the player has one or many triplets in their hand."""
	value_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0] #ace through king
	possible_values = ["a","2","3","4","5","6","7","8","9","10","j","q","k"]

	# Count the number of cards of each value in the player's hand.
	for card in player_hand:
		for val in range(len(possible_values)):
			if card.get_value() == possible_values[val]:
				value_counts[val] += 1

	# Generate a dictionary stating whether a triplet of each value exists in the hand.
	triplets = {key:(True if val==3 else False) for (key,val) in zip(possible_values,value_counts)}

	return triplets #{card value:True/False given triplet or not}

def has_quartet(player_hand):
	"""Check if the player has one or many quartets in their hand."""
	pass

def has_straight(player_hand):
	"""Check if the player has one or many straights in their hand."""
	pass