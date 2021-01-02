from deck import Deck

class Player:
	def __init__(self,name):
		self.hand = [] #cards in hand
		self.discard = [] #cards on tabletop
		self.score = 0 #current score in the game
		self.name = name

	def draw_from_deck(self,deck,num_cards=1):
		"""
		Draw a specified number of cards from the deck. Defaults to 1 card.
		Returns the updated deck.
		"""
		for i in range(num_cards):
			self.hand.append(deck.draw())

		return deck

	def draw_from_discard_line(self,discard_line,num_cards=1):
		"""Draw a specified number of cards from the discard line. Defaults to the top card."""
		pass

	def list_hand(self):
		"""Print the cards in the player's hand to the console."""
		print(self.hand)