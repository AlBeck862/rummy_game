import pygame
from deck import Deck
from player import Player

class Game:
	def __init__(self,p1="Player 1",p2="Player 2"):
		pygame.init()
		self.width = 1100
		self.height = 700
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Rummy 500")
		self.bg = 0,180,0 #green
		self.player1 = Player(p1)
		self.player2 = Player(p2)
		self.deck = Deck()
		self.hand_size = 10 #number of cards dealt to each player
		self.discard_line = []

	def play(self):
		"""Main function that runs the game."""

		# Initialize the clock
		clock = pygame.time.Clock()

		# Game loop
		run = True
		while run:

			clock.tick(30) #run the game at 30 fps

			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					pygame.quit()
					quit()

			self.screen.fill(self.bg)

	def new_round(self):
		"""Update round-specific values such as the deck and the player hands."""
		self.deck = self.player1.draw_from_deck(self.deck,10) #player 1 draws 10 cards, the deck is updated
		self.deck = self.player2.draw_from_deck(self.deck,10) #player 2 draws 10 cards, the deck is updated
		self.discard_line.append(self.deck.draw()) #turn the top card of the deck to start the discard line


	def update_score(self):
		"""Update player scores after a round is completed."""
		pass