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
		value = [0] * len(self.stage)
		for card_num,card in enumerate(self.stage):
			value[card_num] = card.get_value()

		print(value)

		if (len(value) == num_cards) and (all(x == value[0] for x in value)):
			return True
		else:
			return False

	def check_for_straight(self):
		"""Check for a straight in the player's stage."""
		pass

	### UNTESTED METHODS BELOW THIS LINE ###

	def _count_similar_values(self):
		"""Count the number of cards of each value in a player's hand."""	
		value_counts = [0,0,0,0,0,0,0,0,0,0,0,0,0] #ace through king
		possible_values = ["a","2","3","4","5","6","7","8","9","10","j","q","k"]

		# Count the number of cards of each value in the player's hand.
		for card in self.hand:
			for val in range(len(possible_values)):
				if card.get_value() == possible_values[val]:
					value_counts[val] += 1

		return zip(possible_values,value_counts)

	def has_triplet(self):
		"""
		Check if the player has one or many triplets in their hand.
		Generates a dictionary stating whether a triplet of each value exists in the hand.
		"""
		zipped_count = self._count_similar_values()

		triplets = {key:(True if val==3 else False) for (key,val) in zipped_count}

		return triplets #{card value:True/False given triplet or not}

	def has_quartet(self):
		"""
		Check if the player has one or many quartets in their hand.
		Generates a dictionary stating whether a quartet of each value exists in the hand.
		"""
		zipped_count = self._count_similar_values()

		quartets = {key:(True if val==4 else False) for (key,val) in zipped_count}

		return quartets #{card value:True/False given triplet or not}

	def _sort_for_straights(suit_list):
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

	def has_straight(self):
		"""Check if the player has one or many straights in their hand."""
		
		# Create one list for each suit in the player's hand
		all_hearts = []
		all_diamonds = []
		all_clubs = []
		all_spades = []
		for card in self.hand:
			if card.is_suit("hearts"):
				all_hearts.append(card)
			if card.is_suit("diamonds"):
				all_diamonds.append(card)
			if card.is_suit("clubs"):
				all_clubs.append(card)
			if card.is_suit("spades"):
				all_spades.append(card)

		# Get the order of cards for each suit
		hearts = self._sort_for_straights(all_hearts)
		hearts.append(False) #append False to prevent a list-index error below

		diamonds = self._sort_for_straights(all_diamonds)
		diamonds.append(False) #append False to prevent a list-index error below

		clubs = self._sort_for_straights(all_clubs)
		clubs.append(False) #append False to prevent a list-index error below

		spades = self._sort_for_straights(all_spades)
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