import pygame
import time
from deck import Deck
from player import Player
from button import *

class Game:
	# Colours
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	DARK_GREEN = (0,180,0)
	GREEN = (0,255,0)
	LESS_GREEN = (0,200,0)
	
	# Misc. variables
	FPS = 30 #fps at which the game runs
	DECK_LOC = (50,410) #x,y position of the back of the deck
	CARD_SIZE = (125,191) #set size of a card, used for image scaling
	LINE_PX_OFFSET = 25 #offset between cards in a line
	
	# Width and height of the window
	WIDTH = 1600
	HEIGHT = 1010

	# Starting coordinates of the discard line
	DISCARD_X = 200
	DISCARD_Y = 410

	# Starting coordinates of Player 1's hand
	PLAYER_1_X = 50
	PLAYER_1_Y = 210

	# Starting coordinates of Player 2's hand
	PLAYER_2_X = 50
	PLAYER_2_Y = 610

	# Starting coordinates of Player 1's stage
	PLAYER_1_STAGE_X = 50
	PLAYER_1_STAGE_Y = 10

	# Starting coordinates of Player 2's stage
	PLAYER_2_STAGE_X = 50
	PLAYER_2_STAGE_Y = 810

	# Width, height, and position of the discard button
	DISCARD_BUTTON_WIDTH = 250
	DISCARD_BUTTON_HEIGHT = 50
	DISCARD_BUTTON_X = 1300
	DISCARD_BUTTON_Y = DISCARD_Y + (CARD_SIZE[1]/2) - (DISCARD_BUTTON_HEIGHT/2) #align the button with the discard line (and deck)

	# Width, height, and position of the undo button (when drawing from the discard line)
	UNDO_BUTTON_WIDTH = 130
	UNDO_BUTTON_HEIGHT = 50
	UNDO_BUTTON_X = 1200
	UNDO_BUTTON_Y = 950

	def __init__(self,p1="Player 1",p2="Player 2"):
		"""
		p1: string, player 1's name, defaults to "Player 1"
		p2: string, player 2's name, defaults to "Player 2"
		"""

		# Initialize PyGame
		pygame.init()
		
		# Game window initialization
		self.window = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
		pygame.display.set_caption("Rummy 500")
		
		self.bg = self.DARK_GREEN #the screen's background color
		self.player1 = Player(p1) #create Player 1
		self.player2 = Player(p2) #create Player 2
		self.deck = None #the deck is initialized via the play() method below
		self.hand_size = 10 #number of cards dealt to each player
		self.discard_line = [] #an empty discard line, populated by the internal _new_round() method
		self.card_back = pygame.image.load("card_backs/red_back.png") #the back of a card to represent the deck of cards on the screen
		self.state = 1 #the state of the game (Player 1: 1, Player 2: 2, Pause: 3), starts as Player 1

	def play(self):
		"""Main function that runs the game."""

		# Initialize the clock
		clock = pygame.time.Clock()

		# Start the first round of the game
		self._new_round()

		self.show_undo_button = False
		self.undo_button_clicked = False

		# TEST CODE, REMOVE ASAP *********************************
		self.player_drawn = False

		# Game loop
		while True:

			# Run the game at the set framerate
			clock.tick(self.FPS)

			# Quit the game if the window is closed
			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					pygame.quit()
					quit()


			# End the round if either (player hand and stage is empty) or (the deck is empty)
			if (len(self.player1.hand) == 0 and len(self.player1.stage) == 0) or (len(self.player2.hand) == 0 and len(self.player2.stage) == 0) or self.deck.check_if_empty():
				# The round is over
				print("new round started")
				# ADD: tally points
				self._new_round()

			# INSERT PLAYER-STATE CHANGE LOGIC HERE (must be before player-specific logic)
			# INCLUDE: reset of "self.player_drawn" variable to False
			# INCLUDE: reset of "self.show_undo_button" variable to False (if it is never clicked, it will stay until the end of the turn)

			if self.state == 1: #player 1
				# Check whether the deck has been clicked (True: clicked, False: not clicked)
				self.deck_click = self._mouse_click(self.DECK_LOC[0], self.DECK_LOC[1], self.CARD_SIZE[0], self.CARD_SIZE[1])

				# Check for click on a specific discard line card
				self.discard_line_click, self.discard_line_index = self._line_click(self.discard_line,self.DISCARD_X,self.DISCARD_Y,self.CARD_SIZE[0],self.CARD_SIZE[1])
				if self.discard_line_click and not self.player_drawn:
					self.discard_line_click_card = self.discard_line[self.discard_line_index] #the card clicked in the discard line is remembered: it must be discarded to the tabletop
					self.show_undo_button = True

				# Check for click on a specific card in Player 1's hand
				self.player_hand_click, self.player_hand_index = self._line_click(self.player1.hand,self.PLAYER_1_X,self.PLAYER_1_Y,self.CARD_SIZE[0], self.CARD_SIZE[1])

				# Check for click on a specific card in Player 1's stage
				self.stage_click, self.stage_index = self._line_click(self.player1.stage,self.PLAYER_1_STAGE_X,self.PLAYER_1_STAGE_Y,self.CARD_SIZE[0], self.CARD_SIZE[1])

				# Check for valid card combinations in Player 1's stage
				if self.show_undo_button:
					self.triplet = self.player1.check_for_match(3,self.discard_line_click_card) #check for a triplet, True if a triplet is in the player's stage AND the card clicked in the discard line is used
					self.quartet = self.player1.check_for_match(4,self.discard_line_click_card) #check for a quartet, True if a quartet is in the player's stage AND the card clicked in the discard line is used
					self.straight = self.player1.check_for_straight(self.discard_line_click_card) #check for a straight, True if a straight is in the player's stage AND the card clicked in the discard line is used
				else:
					self.triplet = self.player1.check_for_match(3) #check for a triplet, True if a triplet is in the player's stage
					self.quartet = self.player1.check_for_match(4) #check for a quartet, True if a quartet is in the player's stage
					self.straight = self.player1.check_for_straight() #check for a straight, True if a straight is in the player's stage

				# Check for click on the undo button if applicable
				if self.show_undo_button:
					self.undo_button_clicked = self._mouse_click(self.UNDO_BUTTON_X,self.UNDO_BUTTON_Y,self.UNDO_BUTTON_WIDTH,self.UNDO_BUTTON_HEIGHT)

			elif self.state == 2: #player 2
				# Check whether the deck has been clicked (True: clicked, False: not clicked)
				self.deck_click = self._mouse_click(self.DECK_LOC[0], self.DECK_LOC[1], self.CARD_SIZE[0], self.CARD_SIZE[1])
				
				# Check for click on a specific discard line card
				self.discard_line_click, self.discard_line_index = self._line_click(self.discard_line,self.DISCARD_X,self.DISCARD_Y,self.CARD_SIZE[0],self.CARD_SIZE[1])
			
				# Check for click on a specific card in Player 2's hand
				self.player_hand_click, self.player_hand_index = self._line_click(self.player2.hand,self.PLAYER_2_X,self.PLAYER_2_Y,self.CARD_SIZE[0], self.CARD_SIZE[1])

				# Check for click on a specific card in Player 2's stage
				self.stage_click, self.stage_index = self._line_click(self.player2.stage,self.PLAYER_2_STAGE_X,self.PLAYER_2_STAGE_Y,self.CARD_SIZE[0], self.CARD_SIZE[1])

			elif self.state == 3: #pause menu
				pass

			# Refresh what is displayed on-screen
			self._draw_window()

############### CURRENT BUGS ###############
# Undo button: clicking "undo" while any of the cards drawn from the discard line are in the stage (and not in hand) crashes the game because .remove() is called in player.undo_discard() on a list (player hand) that does not contain the card.
############### CURRENT BUGS ###############

	def _draw_window(self):
		"""Update what is shown on-screen."""
		self.window.fill(self.bg)

		# Display the back of the deck and a count of cards remaining in the deck
		if self.deck_click:
			card_back = ImageButton(size=self.CARD_SIZE,position=self.DECK_LOC,image=self.card_back,text=str(len(self.deck.contents)),font="Arial Bold",action=self._draw_from_deck())
			card_back.exist(self.window)
			self.deck_click = False #reset deck_click after the click is acted upon
		else:
			card_back = ImageButton(size=self.CARD_SIZE,position=self.DECK_LOC,image=self.card_back,text=str(len(self.deck.contents)),font="Arial Bold")
			card_back.exist(self.window)

		# Display the discard line
		if self.discard_line_click:
			self._display_line(self.discard_line,self.DISCARD_X,self.DISCARD_Y,button=True,action=self._draw_from_discard_line())
			self.discard_line_click = False #reset discard_line_click after the click is acted upon
		else:
			self._display_line(self.discard_line,self.DISCARD_X,self.DISCARD_Y,button=True)

		# Display the undo button if applicable (if a card was drawn from the discard line, the player must play that card which may not be possible)
		# The undo button returns the cards drawn from the discard line to the discard line
		if self.show_undo_button:
			if self.undo_button_clicked:
				undo_button = TextButton((self.UNDO_BUTTON_WIDTH,self.UNDO_BUTTON_HEIGHT),(self.UNDO_BUTTON_X,self.UNDO_BUTTON_Y),colour=self.GREEN,rollover_colour=self.LESS_GREEN,text="UNDO DRAW",text_size=18,font="Arial Rounded Bold",action=self._undo_discard_draw())
				undo_button.exist(self.window)
				self.undo_button_clicked = False #reset undo_button_clicked after the click is acted upon
				self.player_drawn = False #allow the player to draw again to correct their mistake (i.e., allow them to draw from the deck instead)
			else:
				undo_button = TextButton((self.UNDO_BUTTON_WIDTH,self.UNDO_BUTTON_HEIGHT),(self.UNDO_BUTTON_X,self.UNDO_BUTTON_Y),colour=self.GREEN,rollover_colour=self.LESS_GREEN,text="UNDO DRAW",text_size=18,font="Arial Rounded Bold")
				undo_button.exist(self.window)

		# Display player 1's hand
		if self.player_hand_click:
			self._display_line(self.player1.hand,self.PLAYER_1_X,self.PLAYER_1_Y,button=True,action=self._player_card_selected())
			self.player_hand_click = False #reset player_hand_click after the click is acted upon
		else:
			self._display_line(self.player1.hand,self.PLAYER_1_X,self.PLAYER_1_Y,button=True)

		# Display player 2's hand
		if self.player_hand_click:
			self._display_line(self.player2.hand,self.PLAYER_2_X,self.PLAYER_2_Y,button=True,action=self._player_card_selected())
			self.player_hand_click = False #reset player_hand_click after the click is acted upon
		else:
			self._display_line(self.player2.hand,self.PLAYER_2_X,self.PLAYER_2_Y,button=True)

		# Display player 1's stage
		if self.stage_click:
			self._display_line(self.player1.stage,self.PLAYER_1_STAGE_X,self.PLAYER_1_STAGE_Y,button=True,action=self._unstage_card()) #action: return card to hand
			self.stage_click = False #reset stage_click after the click is acted upon
		else:
			self._display_line(self.player1.stage,self.PLAYER_1_STAGE_X,self.PLAYER_1_STAGE_Y,button=True)

		# Display player 2's stage
		if self.stage_click:
			self._display_line(self.player2.stage,self.PLAYER_2_STAGE_X,self.PLAYER_2_STAGE_Y,button=True,action=self._unstage_card())
			self.stage_click = False #reset stage_click after the click is acted upon
		else:
			self._display_line(self.player2.stage,self.PLAYER_2_STAGE_X,self.PLAYER_2_STAGE_Y,button=True)

		# Set up the appropriate discard button ***********IMPORTANT: self.show_undo_button should ONLY be reset to False if the button is CLICKED
		if self.triplet:
			discard_button = TextButton((self.DISCARD_BUTTON_WIDTH,self.DISCARD_BUTTON_HEIGHT),(self.DISCARD_BUTTON_X,self.DISCARD_BUTTON_Y),colour=self.GREEN,rollover_colour=self.LESS_GREEN,text="DISCARD TRIPLET",text_size=18,font="Arial Rounded Bold")
			self.show_undo_button = False #remove the undo button once the card is discarded to the tabletop
		elif self.quartet:
			discard_button = TextButton((self.DISCARD_BUTTON_WIDTH,self.DISCARD_BUTTON_HEIGHT),(self.DISCARD_BUTTON_X,self.DISCARD_BUTTON_Y),colour=self.GREEN,rollover_colour=self.LESS_GREEN,text="DISCARD QUARTET",text_size=18,font="Arial Rounded Bold")
			self.show_undo_button = False #remove the undo button once the card is discarded to the tabletop
		elif self.straight:
			discard_button = TextButton((self.DISCARD_BUTTON_WIDTH,self.DISCARD_BUTTON_HEIGHT),(self.DISCARD_BUTTON_X,self.DISCARD_BUTTON_Y),colour=self.GREEN,rollover_colour=self.LESS_GREEN,text="DISCARD STRAIGHT",text_size=18,font="Arial Rounded Bold")
			self.show_undo_button = False #remove the undo button once the card is discarded to the tabletop
		elif self.state == 1:
			if len(self.player1.stage) == 1 and not self.show_undo_button:
				discard_button = TextButton((self.DISCARD_BUTTON_WIDTH,self.DISCARD_BUTTON_HEIGHT),(self.DISCARD_BUTTON_X,self.DISCARD_BUTTON_Y),colour=self.GREEN,rollover_colour=self.LESS_GREEN,text="DISCARD AND END TURN",text_size=18,font="Arial Rounded Bold")
		elif self.state == 2:
			if len(self.player2.stage) == 1 and not self.show_undo_button:
				discard_button = TextButton((self.DISCARD_BUTTON_WIDTH,self.DISCARD_BUTTON_HEIGHT),(self.DISCARD_BUTTON_X,self.DISCARD_BUTTON_Y),colour=self.GREEN,rollover_colour=self.LESS_GREEN,text="DISCARD AND END TURN",text_size=18,font="Arial Rounded Bold")
		
		# Display the discard button if applicable
		try:
			discard_button.exist(self.window)
		except:
			pass

		# Display the name of the player whose turn it is currently (or pause if the game state is set to pause)
		if self.state == 1:
			current_player_name = self.player1.name
			self._create_text(current_player_name + "'s turn",20,(1450,925),(100,100))
		elif self.state == 2:
			current_player_name = self.player2.name
			self._create_text(current_player_name + "'s turn",20,(1450,925),(100,100))
		elif self.state == 3:
			self._create_text("Game Paused",20,(1450,925),(100,100))

		# Refresh the screen
		pygame.display.update()

	def _line_click(self,line,x,y,width,height):
		"""Determine which card in a card line has been selected."""
		# Set line_clicked and line_index to default values: necessary for 0-card lines to avoid skipping assignment (by skipping the loop)
		line_clicked = False
		line_index = None

		# Check for click on a specific discard line card
		for card_num in range(len(line)):
			# Set last_card to True when the last card in the discard line is reached
			if card_num == len(line) - 1:
				last_card = True
			else:
				last_card = False

			# Adapt the mouse click region depending on the card in the discard line (partially covered card versus end-of-line card)
			if last_card:
				line_clicked = self._mouse_click(x+(card_num*self.LINE_PX_OFFSET),y,width,height)
			else:
				line_clicked = self._mouse_click(x+(card_num*self.LINE_PX_OFFSET),y,self.LINE_PX_OFFSET,height)
			
			# If a card in the discard line was clicked, store the card's position in the discard line and exit the loop
			if line_clicked:
				line_index = card_num #stores the card that was selected in the discard line
				break

		return line_clicked,line_index

	def _new_round(self):
		"""Update round-specific values such as the deck and the player hands."""
		# Reset the deck
		self.deck = Deck()

		# Reset the player hands
		self.player1.hand = []
		self.player2.hand = []
		self.deck = self.player1.draw_from_deck(self.deck,10) #player 1 draws 10 cards, the deck is updated
		self.deck = self.player2.draw_from_deck(self.deck,10) #player 2 draws 10 cards, the deck is updated

		# Reset the player tabletops
		self.player1.tabletop = []
		self.player2.tabletop = []

		# Reset the player stages
		self.player1.stage = []
		self.player2.stage = []

		# Reset the discard line
		self.discard_line = []
		
		for i in range(5):
			self.discard_line.append(self.deck.draw()) #turn the top card of the deck to start the discard line

		# NOTE: POSSIBLY REMOVE OR RELOCATE THIS VARIABLE RESET
		self.player_drawn = False

	def _create_text(self,text,text_size,position,box_size,colour=(0,0,0),font="Arial",mode="center"):
		"""
		Prepare the text to be overlaid somewhere on the screen.
		text: string
		text_size: font size in points
		position: (x,y) tuple
		box_size: (width,height) tuple
		colour: (R,G,B) tuple, defaults to black
		font: string, font type, defaults to Arial
		mode: string, describes how the text should be overlaid relative to the surface, defaults to centered
		"""
		# Prepare the text to be overlaid onto the screen
		font = pygame.font.SysFont(font,text_size)
		text_surface = font.render(text, True, colour)
		text_rect = text_surface.get_rect()

		# Different text placements relative to the position and box size
		if mode == "center": #centered text
			text_rect.center = ((position[0] + box_size[0]/2),(position[1] + box_size[1]/2))
		else:
			raise NameError("Invalid text placement mode")

		# Display the text
		self.window.blit(text_surface, text_rect)

	def _display_line(self,card_line,start_x,start_y,button=False,action=None):
		"""
		Display a line of cards on the screen.
		card_line: list, cards to be displayed
		start_x: int, x position of the first image in the line
		start_y: int, y position of the image line
		button: bool, is this a line of images or of button images, defaults to False
		action: function, if this is a line of button images, what do the buttons do, defaults to None
		"""
		if button: #if the images in the line are also buttons, generate ImageButton objects
			for card_num in range(len(card_line)):
				
				# Set last_card to True if the last image in the line is reached
				if card_num == len(card_line) - 1:
					last_card = True
				else:
					last_card = False

				image = ImageButton(size=self.CARD_SIZE,position=(start_x+(card_num*self.LINE_PX_OFFSET),start_y),image=card_line[card_num].image,action=action,offset=self.LINE_PX_OFFSET,last_element=last_card)
				image.exist(self.window)

		else: #if the images in the line are simply images, display the images directly to the screen with no added logic
			for card_num in range(len(card_line)):
				self.window.blit(card_line[card_num].image,(start_x+(card_num*self.LINE_PX_OFFSET),start_y))

	def _mouse_click(self,x,y,width,height):
		"""Return True if a click is registered in the given region. Otherwise return False"""
		# Prevent clicks from being detected too quickly
		try:
			if (time.time() - self.time_of_click) < 0.2:
				return False
		except:
			pass

		# Get the mouse position for button shading effects
		mouse_position = pygame.mouse.get_pos()

		# Stores the left click in click[0]
		click = pygame.mouse.get_pressed()

		if (x < mouse_position[0] < (x + width)) and (y < mouse_position[1] < (y + height)) and (click[0] == 1):
			# Click in the designated region
			self.time_of_click = time.time() #store the time of the last click that was acted upon
			return True

		else:
			# No click in the designated region
			return False

	def _draw_from_deck(self):
		"""Draw from the deck."""
		# If the player has not drawn yet, allow the player to draw
		if not self.player_drawn:
			if self.state == 1:
				self.deck = self.player1.draw_from_deck(self.deck)
				self.player_drawn = True #prevents drawing multiple times per turn, must be reset after each turn
			elif self.state == 2:
				self.deck = self.player2.draw_from_deck(self.deck)
				self.player_drawn = True #prevents drawing multiple times per turn, must be reset after each turn

	def _draw_from_discard_line(self):
		"""Draw from the discard line."""
		# If the player has not drawn yet, allow the player to draw
		if not self.player_drawn:
			if self.state == 1:
				self.discard_line,self.drawn_discard_cards = self.player1.draw_from_discard_line(self.discard_line,self.discard_line_index)
				self.player_drawn = True #prevents drawing multiple times per turn, must be reset after each turn
			elif self.state == 2:
				self.discard_line,self.drawn_discard_cards = self.player2.draw_from_discard_line(self.discard_line,self.discard_line_index)
				self.player_drawn = True #prevents drawing multiple times per turn, must be reset after each turn

	def _player_card_selected(self):
		"""Move a card from the current player's hand to that player's stage."""
		if self.state == 1:
			self.player1.stage_for_discard(self.player_hand_index)
		elif self.state == 2:
			self.player2.stage_for_discard(self.player_hand_index)

	def _unstage_card(self):
		"""Move a card from the current player's stage to that player's hand."""
		if self.state == 1:
			self.player1.unstage(self.stage_index)
		elif self.state == 2:
			self.player2.unstage(self.stage_index)

	def _undo_discard_draw(self):
		"""Return all cards drawn from the discard line to the discard line."""
		if self.state == 1:
			self.discard_line = self.player1.undo_discard(self.discard_line,self.drawn_discard_cards)
		elif self.state == 2:
			self.discard_line = self.player2.undo_discard(self.discard_line,self.drawn_discard_cards)

	def _update_score(self):
		"""Update player scores after a round is completed."""
		pass