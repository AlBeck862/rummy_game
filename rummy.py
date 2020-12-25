"""
Details here
"""

import pygame
import random
import itertools
from card import Card
# import numpy as np
pygame.init()

# Window parameters
size = width, height = 1100,700
bg = 0,180,0 #green background
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rummy 500")

# Card parameters
card_size = [50,100]
card_colour = 0,0,0
card_locations = [(50,50,card_size[0],card_size[1]),(150,50,card_size[0],card_size[1]),(250,50,card_size[0],card_size[1])]

# Generate a shuffled (randomized) deck of 52 unique cards
def shuffle_deck():
	deck = []
	suits = ["Hearts","Diamonds","Clubs","Spades"]
	values = ["A","2","3","4","5","6","7","8","9","10","J","Q","K"]
	all_cards =  list(itertools.product(suits,values)) #generate all possible card combinations
	random.shuffle(all_cards) #randomize the card combinations
	
	# Generate the randomized deck of cards
	for i in range(len(all_cards)):
		new_card = Card(all_cards[i][0],all_cards[i][1])

		deck.append(new_card)

	return deck #return the randomized deck of cards

run = False #skip the window creation while debugging
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False

	screen.fill(bg)

	for loc in card_locations:
		pygame.draw.rect(screen,card_colour,loc)

	pygame.display.update()


pygame.quit()