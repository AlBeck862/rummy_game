class Player:
	def __init__(self,name):
		self.hand =
		self.discard = []
		self.score = 0
		self.name = name

	def draw_from_deck(self,deck,num_cards=1):
		"""Draw a specified number of cards from the deck. Defaults to 1 card."""
		pass

	def draw_from_discard_line(self,discard_line,num_cards=1):
		"""Draw a specified number of cards from the discard line. Defaults to the top card."""
		pass