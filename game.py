import pygame
from deck import Deck
from player import Player
from button import Button

class Game:
	def __init__(self,p1="Player 1",p2="Player 2"):
		pygame.init()
		self.width = 1100
		self.height = 700
		self.window = pygame.display.set_mode((self.width, self.height))
		pygame.display.set_caption("Rummy 500")
		self.bg = 0,180,0 #green
		self.player1 = Player(p1, True)
		self.player2 = Player(p2, False)
		self.deck = Deck()
		self.hand_size = 10 #number of cards dealt to each player
		self.discard_line = []

	def play(self):
		"""Main function that runs the game."""

		# Initialize the clock
		clock = pygame.time.Clock()

		# The following goes into a larger "game loop" that operates off of player scores:
		# while (self.player1.score < 500) and (self.player2.score < 500):
		self.new_round()

		while (len(self.player1.hand) != 0) and (len(self.player2.hand) != 0) and not self.deck.check_if_empty():

			clock.tick(30) #run the game at 30 fps

			for event in pygame.event.get():
				if event.type == pygame.QUIT: 
					pygame.quit()
					quit()

			self.window.fill(self.bg)

			if self.player1.turn:
				# Test to display the correct card on the screen
				# self.window.blit(self.deck.contents[0].image,(100,100))
				# print(self.deck.contents[0].suit)
				# print(self.deck.contents[0].value)
				pass

			elif self.player2.turn:
				pass

			else:
				print("Player turn error.")

			button = Button((450,75),(200,500),(255,255,255),"Hello World!")
			button.exist(self.window)


			pygame.display.update()

		# Update the scores after the round ends
		# update_score()


	def draw(self):
		"""Update what is shown on-screen."""
		pass

	def new_round(self):
		"""Update round-specific values such as the deck and the player hands."""
		self.deck = self.player1.draw_from_deck(self.deck,10) #player 1 draws 10 cards, the deck is updated
		self.deck = self.player2.draw_from_deck(self.deck,10) #player 2 draws 10 cards, the deck is updated
		self.discard_line.append(self.deck.draw()) #turn the top card of the deck to start the discard line


	def update_score(self):
		"""Update player scores after a round is completed."""
		pass