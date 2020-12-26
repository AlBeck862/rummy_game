class Card:
	def __init__(self,suit,value):
		"""Every card has a suit and a value."""
		self.suit=suit
		self.value=value

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