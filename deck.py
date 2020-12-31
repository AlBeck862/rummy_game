import random
import itertools
from card import Card

class Deck:
	def __init__(self):
		"""Every deck contains the standard 52 cards in randomized order"""
		self.contents = self._generate_deck()

	def __repr__(self):
		"""What is returned when checking the contents (and order) of a deck."""
		return self.contents

	def draw(self):
		"""Replaces .pop(0) functionality used for lists: always draws from the top (start) of the deck."""
		return self.contents.pop(0)

	def _generate_deck(self):
		"""Generate a shuffled (randomized) deck of 52 unique cards."""
		deck = []
		suits = ["Hearts","Diamonds","Clubs","Spades"]
		values = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
		all_cards =  list(itertools.product(suits,values)) #generate all possible card combinations
		random.shuffle(all_cards) #randomize the card combinations
		
		# Generate the randomized deck of cards
		for i in range(len(all_cards)):
			new_card = Card(all_cards[i][0],all_cards[i][1])
			deck.append(new_card)

		return deck

	def check_if_empty(self):
		"""Returns true if the deck is empty, otherwise, return false."""
		if len(self.contents) == 0: #empty deck
			return True
		else: #deck still contains cards
			return False