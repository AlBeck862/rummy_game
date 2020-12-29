import random
import itertools
from card import Card
from deck import Deck

def start_new_hand():
	"""Initialize a new hand of Rummy 500."""
	deck = Deck() #get a new deck
	hand_size = 10 #10 cards dealt to each player
	player1_hand = [] #empty player 1 hand
	player2_hand = [] #empty player 2 hand
	discard_line = [] #empty discard line (on the tabletop)

	# Deal cards to player hands from the deck
	for i in range(hand_size):
		player1_hand.append(deck.draw())
		player2_hand.append(deck.draw())

	# Flip the top card of the deck onto the table top to start the discard line
	discard_line.append(deck.draw())

	return deck,discard_line,player1_hand,player2_hand

def count_similar_values(player_hand):
	"""Count the number of cards of each value in a player's hand."""	
	value_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0] #ace through king
	possible_values = ["a","2","3","4","5","6","7","8","9","10","j","q","k"]

	# Count the number of cards of each value in the player's hand.
	for card in player_hand:
		for val in range(len(possible_values)):
			if card.get_value() == possible_values[val]:
				value_counts[val] += 1

	return zip(possible_values,value_counts)

def has_triplet(player_hand):
	"""
	Check if the player has one or many triplets in their hand.
	Generates a dictionary stating whether a triplet of each value exists in the hand.
	"""
	zipped_count = count_similar_values(player_hand)

	triplets = {key:(True if val==3 else False) for (key,val) in zipped_count}

	return triplets #{card value:True/False given triplet or not}

def has_quartet(player_hand):
	"""
	Check if the player has one or many quartets in their hand.
	Generates a dictionary stating whether a quartet of each value exists in the hand.
	"""
	zipped_count = count_similar_values(player_hand)

	quartets = {key:(True if val==4 else False) for (key,val) in zipped_count}

	return quartets #{card value:True/False given triplet or not}

def sort_for_straights(suit_list):
	"""Sorts a suited list according to card values."""
	numerical_list = [False] * 14 #list of 14 None-type spaces, ace-low through ace-high
	
	# Establish the order of the cards
	for card in suit_list:
		try:
			num_value = int(card.get_value())
		except:
			if card.get_value() == "jack":
				num_value = 11
			elif card.get_value() == "queen":
				num_value = 12
			elif card.get_value() == "king":
				num_value = 13
			elif card.get_value() == "ace":
				num_value = 14
			else:
				print("Error: straight sorting failed.")

		numerical_list[num_value-1] = True
		numerical_list[0] = numerical_list[13] #force the ace count to be the same in both ace locations

	# Return a boolean list representing card presence in the given suit, ordered from ace-low to ace-high
	return numerical_list

def has_straight(player_hand):
	"""Check if the player has one or many straights in their hand."""
	
	# Create one list for each suit in the player's hand
	all_hearts = []
	all_diamonds = []
	all_clubs = []
	all_spades = []
	for card in player_hand:
		if card.is_suit("hearts"):
			all_hearts.append(card)
		if card.is_suit("diamonds"):
			all_diamonds.append(card)
		if card.is_suit("clubs"):
			all_clubs.append(card)
		if card.is_suit("spades"):
			all_spades.append(card)

	# Get the order of cards for each suit
	hearts = sort_for_straights(all_hearts)
	hearts.append(False) #append False to prevent a list-index error below

	diamonds = sort_for_straights(all_diamonds)
	diamonds.append(False) #append False to prevent a list-index error below

	clubs = sort_for_straights(all_clubs)
	clubs.append(False) #append False to prevent a list-index error below

	spades = sort_for_straights(all_spades)
	spades.append(False) #append False to prevent a list-index error below

	# Place all suit lists into a single multi-dimensional list
	all_suits = [hearts,diamonds,clubs,spades]

	# Package straight cards and lengths together
	straights = [False] * 20 #this is more than enough slots to cover for the number of possible straights in a hand
	straight_num = 0
	suit_count = 0
	for suit in all_suits:
		suit_count += 1
		for i in range(len(suit)):
			# Edge case for the first index (cannot check the previous index)
			if i == 0:
				if suit[0]:
					start_index = 0
			# Detect the start of a potential straight
			elif suit[i] and not suit[i-1]:
				start_index = i
			# Detect the end of a potential straight
			elif suit[i] and not suit[i+1]:
				end_index = i
				if (end_index - start_index) >= 2:
					straights[straight_num] = (suit_count,start_index,end_index)
					straight_num += 1
			else:
				pass

	# Return the suit and the indeces of the cards bounding each straight
	return straights