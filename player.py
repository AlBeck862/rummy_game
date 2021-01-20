from deck import Deck

class Player:
	def __init__(self,name):
		self.hand = [] #cards in hand
		self.tabletop = [] #cards on tabletop
		self.stage = [] #region of cards primed to be discarded
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

	def draw_from_discard_line(self,discard_line,discard_line_index):
		"""
		Draw a specified number of cards from the discard line.
		Returns an updated discard line.
		"""
		num_cards = len(discard_line) - discard_line_index #calculate the number of cards to draw from the end of the discard line

		for i in range(num_cards):
			self.hand.append(discard_line.pop())

		return discard_line

	def stage_for_discard(self,hand_index):
		"""Move a card from the player's hand to that player's stage."""
		self.stage.append(self.hand.pop(hand_index))

	def unstage(self,hand_index):
		"""Move a card from the player's stage to that player's hand."""
		self.hand.append(self.stage.pop(hand_index))

	def list_hand(self):
		"""Print the cards in the player's hand to the console."""
		print(self.hand)

	def check_for_match(self,num_cards):
		"""Check for a match (3 or 4 cards) in the player's stage."""
		# Store staged card values
		value = [card.get_value() for card in self.stage]

		# Check if all values are identical and if there is the specified number of cards
		if (len(value) == num_cards) and (all(x == value[0] for x in value)):
			return True
		else:
			return False

	def check_for_straight(self):
		"""Check for a straight in the player's stage."""
		# Initialize lists of the stage's cards' numerical values and suits
		num_value = [card.numerical_value for card in self.stage]
		suit = [card.get_suit() for card in self.stage]

		print(num_value)
		print(suit)

		# Check if the numerical values in the stage are sequential and if the all card suits in the stage are identical.
		# Also check that the stage contains at least three cards.
		if len(num_value) < 3: #necessary to avoid errors
			return False
		elif (sorted(num_value) == list(range(min(num_value),max(num_value)+1))) and all(x == suit[0] for x in suit):
			return True
		elif 1 in num_value: #handle ace-high cases
			num_value.remove(1)
			num_value.append(14)
			if (sorted(num_value) == list(range(min(num_value),max(num_value)+1))) and all(x == suit[0] for x in suit):
				return True
			else:
				return False
		else:
			return False

	# CURRENTLY UNUSED. COULD BE USED FOR .sort() LIST METHOD OR FOR sorted() LIST FUNCTION.
	# Idea: use to sort straights to be discarded to the tabletop
	def _sort_by_num_value(self,card):
		"""Return the numerical value of the given card for straight sorting."""
		return card.numerical_value