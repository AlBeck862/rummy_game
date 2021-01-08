import pygame
from deck import Deck
from player import Player
from button import Button

class Game:
	WHITE = (255,255,255)
	LIGHT_GREEN = (0,180,0)
	FPS = 30

	def __init__(self,p1="Player 1",p2="Player 2"):
		pygame.init()
		self.width = 1100
		self.height = 700
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Rummy 500")
		self.bg = self.LIGHT_GREEN
		self.player1 = Player(p1, True)
		self.player2 = Player(p2, False)
		self.deck = None #the deck is initialized via the play() method below
		self.hand_size = 10 #number of cards dealt to each player
		self.discard_line = []

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
		
		# Test image
		self.window.blit(self.deck.contents[0].image,(100,100))

		# Test button
		button = Button((450,75),(200,500),self.WHITE,"Hello World!")
		button.exist(self.window)

		pygame.display.update()

	def _new_round(self):
		"""Update round-specific values such as the deck and the player hands."""
		self.deck = Deck()
		self.deck = self.player1.draw_from_deck(self.deck,10) #player 1 draws 10 cards, the deck is updated
		self.deck = self.player2.draw_from_deck(self.deck,10) #player 2 draws 10 cards, the deck is updated
		self.discard_line.append(self.deck.draw()) #turn the top card of the deck to start the discard line


	def _update_score(self):
		"""Update player scores after a round is completed."""
		pass