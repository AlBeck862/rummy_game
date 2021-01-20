import pygame
import os

# Set size of a card, used for image scaling
CARD_SIZE = (125,191)

class Card:
	# All possible cards. Loaded ace-king, heart-diamond-club-spade. Each card is scaled appropriately.
	all_cards = [pygame.transform.scale(pygame.image.load("cards/" + str(x) + ".png"),CARD_SIZE) for x in range(52)] #class variable to avoid reloading every image for every new card object
	possible_values = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King"]
	possible_suits = ["Hearts","Diamonds","Clubs","Spades"]

	def __init__(self,suit,value):
		"""Every card has a suit and a value."""
		self.suit=suit #string
		self.value=value #string
		self.numerical_value=self._assign_numerical_value() #int, 1 through 13 representing Ace through King
		self.points=self._assign_points() #int, point value of the card
		self.image=self._assign_image() #PyGame image

	def __repr__(self):
		"""What is returned when checking the contents of a card."""
		return self.value + " of " + self.suit

	def is_suit(self,suit_query):
		"""Checks the card's suit against a given suit."""
		if self.suit.lower() == suit_query.lower():
			return True
		else:
			return False

	def is_value(self,value_query):
		"""Checks the card's value against a given value."""
		if self.value.lower() == value_query.lower():
			return True
		else:
			return False

	def get_suit(self):
		"""Returns the card's suit."""
		return self.suit.lower()

	def get_value(self):
		"""Returns the card's value."""
		return self.value.lower()

	def _assign_numerical_value(self):
		"""Assign the correct numerical value to the card."""
		for i in range(len(self.possible_values)):
			if self.possible_values[i] == self.value:
				return i + 1

	def _assign_points(self):
		"""Assign the correct points value to the card."""
		if self.value == self.possible_values[0]: #aces are worth 15 points
			return 15
		elif self.value in self.possible_values[1:8]: #all numerically valued cards up to nine are worth 5 points
			return 5
		else: #tens and face cards are worth 10 points
			return 10

	def _assign_image(self):
		"""Assign the correct image to the card."""
		# Variable to allow breaking out of the outside loop below
		break_again = False
		
		# Determine the correct card image to assign to a particular card object given the card's suit and value
		card_selection = 0
		for i in range(len(self.possible_values)):
			for j in range(len(self.possible_suits)):
				if self.possible_values[i] == self.value and self.possible_suits[j] == self.suit:
					break_again = True
					break
				card_selection += 1
			if break_again:
				break

		return self.all_cards[card_selection] #return the correct card image (a PyGame surface)
		