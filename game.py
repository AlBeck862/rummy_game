import pygame
from deck import Deck
from player import Player
from button import Button

class Game:
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	LIGHT_GREEN = (0,180,0)
	FPS = 30 #fps at which the game runs
	DECK_LOC = (1400,390) #x,y position of the back of the deck
	CARD_SIZE = (125,191) #set size of a card, used for image scaling

	def __init__(self,p1="Player 1",p2="Player 2"):
		pygame.init()
		self.width = 1600
		self.height = 1000
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Rummy 500")
		self.bg = self.LIGHT_GREEN
		self.player1 = Player(p1, True)
		self.player2 = Player(p2, False)
		self.deck = None #the deck is initialized via the play() method below
		self.hand_size = 10 #number of cards dealt to each player
		self.discard_line = []
		self.card_back = pygame.image.load("card_backs/red_back.png")

	def play(self):
		"""Main function that runs the game."""

		# Initialize the clock
		clock = pygame.time.Clock()

		# Start the first round of the game
		self._new_round()

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
			
			if self.player1.turn:
				pass

			elif self.player2.turn:
				pass

			else:
				print("Player turn error.")

			# Refresh what is displayed on-screen
			self._draw_window()

		# Update the scores after the round ends
		# _update_score()


	def _draw_window(self):
		"""Update what is shown on-screen."""
		self.window.fill(self.bg)
		
		# Display the back of the deck and a count of cards remaining in the deck
		self.card_back = pygame.transform.scale(self.card_back,self.CARD_SIZE)
		self.window.blit(self.card_back,self.DECK_LOC)
		deck_num_surface,deck_num_rect = self._create_text(str(len(self.deck.contents)),14,self.DECK_LOC,self.CARD_SIZE,font="Arial Bold") #get the text to be overlaid on the deck
		self.window.blit(deck_num_surface,deck_num_rect) #overlay the number of cards remaining in the deck

		# Display the discard line
		# ***NOTE: must be expanded to be compatible with any length of the discard line
		self.window.blit(self.discard_line[0].image,(1250,390)) #NOTE: location should be made more adaptive to the length of the discard line

		# Test image
		# self.window.blit(self.deck.contents[0].image,(100,100))

		# Test button
		# button = Button((450,75),(200,500),self.WHITE,"Hello World!")
		# button.exist(self.window)

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

		return text_surface,text_rect

	def _update_score(self):
		"""Update player scores after a round is completed."""
		pass