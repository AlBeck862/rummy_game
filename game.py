import pygame
from deck import Deck
from player import Player
from button import *

class Game:
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	LIGHT_GREEN = (0,180,0)
	FPS = 30 #fps at which the game runs
	DECK_LOC = (50,390) #x,y position of the back of the deck
	CARD_SIZE = (125,191) #set size of a card, used for image scaling

	def __init__(self,p1="Player 1",p2="Player 2"):
		pygame.init()
		self.width = 1600
		self.height = 1000
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Rummy 500")
		self.bg = self.LIGHT_GREEN
		self.player1 = Player(p1)
		self.player2 = Player(p2)
		self.deck = None #the deck is initialized via the play() method below
		self.hand_size = 10 #number of cards dealt to each player
		self.discard_line = []
		self.card_back = pygame.image.load("card_backs/red_back.png")
		self.state = 2 #set player 1 as the first player (Player 1: 1, Player 2: 2, Pause: 3)

	def play(self):
		"""Main function that runs the game."""

		# Initialize the clock
		clock = pygame.time.Clock()

		# Start the first round of the game
		self._new_round()

		# TEST CODE, REMOVE ASAP ************************
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


			# End the round if either player hand is empty or if the deck is empty
			if (len(self.player1.hand) == 0) or (len(self.player2.hand) == 0) or self.deck.check_if_empty():
				# The round is over
				print("new round started")
				# ADD: tally points
				self._new_round()

			# INSERT PLAYER-STATE CHANGE LOGIC HERE (must be before player-specific logic)
			# INCLUDE: reset of "self.player_drawn" variable to False

			if self.state == 1: #player 1
				# Check whether the deck has been clicked (True: clicked, False: not clicked)
				self.deck_click = self._mouse_click(self.DECK_LOC[0], self.DECK_LOC[1], self.CARD_SIZE[0], self.CARD_SIZE[1])

				#check for click on a specific discard line card


			elif self.state == 2: #player 2
				# Check whether the deck has been clicked (True: clicked, False: not clicked)
				self.deck_click = self._mouse_click(self.DECK_LOC[0], self.DECK_LOC[1], self.CARD_SIZE[0], self.CARD_SIZE[1])

				#check for click on a specific discard line card
			

			elif self.state == 3: #pause menu
				pass


			# Refresh what is displayed on-screen
			self._draw_window()

		# Update the scores after the round ends
		# _update_score()


	def _draw_window(self):
		"""Update what is shown on-screen."""
		self.window.fill(self.bg)

		# Display the back of the deck and a count of cards remaining in the deck
		if self.deck_click:
			card_back = ImageButton(size=self.CARD_SIZE,position=self.DECK_LOC,image=self.card_back,text=str(len(self.deck.contents)),font="Arial Bold",action=self._draw_from_deck()) #add action: _draw_from_deck --> move card from deck to active player (check player.turn)
			card_back.exist(self.window)
			self.deck_click = False #reset deck_click after the click is acted upon
		else:
			card_back = ImageButton(size=self.CARD_SIZE,position=self.DECK_LOC,image=self.card_back,text=str(len(self.deck.contents)),font="Arial Bold") #add action: _draw_from_deck --> move card from deck to active player (check player.turn)
			card_back.exist(self.window)

		# Display the discard line
		self._display_line(self.discard_line,200,390) #should this be converted to a series of ImageButton objects? *************

		# Display player 1's hand
		self._display_line(self.player1.hand,50,180)

		# Display player 2's hand
		self._display_line(self.player2.hand,50,600)

		# Display the name of the player whose turn it is currently (or pause if the game state is set to pause)
		if self.state == 1:
			current_player_name = self.player1.name
			self._create_text(current_player_name + "'s turn",20,(1450,925),(100,100))
		elif self.state == 2:
			current_player_name = self.player2.name
			self._create_text(current_player_name + "'s turn",20,(1450,925),(100,100))
		elif self.state == 3:
			self._create_text("Game Paused",20,(1450,925),(100,100))

		pygame.display.update()

	def _new_round(self):
		"""Update round-specific values such as the deck and the player hands."""
		self.deck = Deck()
		self.deck = self.player1.draw_from_deck(self.deck,10) #player 1 draws 10 cards, the deck is updated
		self.deck = self.player2.draw_from_deck(self.deck,10) #player 2 draws 10 cards, the deck is updated
		self.discard_line.append(self.deck.draw()) #turn the top card of the deck to start the discard line

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
		font = pygame.font.SysFont(font,text_size)
		text_surface = font.render(text, True, colour)
		text_rect = text_surface.get_rect()

		if mode == "center":
			text_rect.center = ((position[0] + box_size[0]/2),(position[1] + box_size[1]/2))
		else:
			raise NameError("Invalid text placement mode")

		self.window.blit(text_surface, text_rect)

	def _display_line(self,card_line,start_x,start_y):
		"""
		Display a line of cards on the screen.
		card_line: list, cards to be displayed
		start_x: int, x position of the first card in the line
		start_y: int, y position of the card line
		"""
		if len(card_line) <= 40:
			px_offset = 30 #offset between discard line cards
		else: #if too many cards are in the discard line, compress the line to fit more cards on the screen
			px_offset = 25

		for card_num in range(len(card_line)):
			self.window.blit(card_line[card_num].image,(start_x+(card_num*px_offset),start_y))

	def _mouse_click(self,x,y,width,height):
		"""Return True if a click is registered in the given region. Otherwise return False"""		
		# Get the mouse position for button shading effects
		mouse_position = pygame.mouse.get_pos()

		# Stores the left click in click[0]
		click = pygame.mouse.get_pressed()

		if (x < mouse_position[0] < (x + width)) and (y < mouse_position[1] < (y + height)) and (click[0] == 1):
			# Click in the designated region
			return True

		else:
			# No click in the designated region
			return False

	def _draw_from_deck(self):
		"""Draw from the deck."""
		# If the player has not drawn yet, allow the player to draw
		if not self.player_drawn:
			if self.state == 1:
				self.player1.draw_from_deck(self.deck)
				self.player_drawn = True #prevents drawing multiple times per turn, must be reset after each turn
			elif self.state == 2:
				self.player2.draw_from_deck(self.deck)
				self.player_drawn = True #prevents drawing multiple times per turn, must be reset after each turn

	def _update_score(self):
		"""Update player scores after a round is completed."""
		pass