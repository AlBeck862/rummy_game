"""
Details here
"""

import pygame
import random
from rummy_fxns import start_new_hand

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

# Initialize a new hand of Rummy 500
deck,discard_line,player1_hand,player2_hand = start_new_hand()

# Set the turn order
player1_turn = True
player2_turn = False

# Play the hand. The hand ends when one player no longer has any cards in hand.
while (len(player1_hand) != 0) or (len(player2_hand) != 0):
	discard_prob = random.random()
	
	if player1_turn:
		if discard_prob <= 0.5:
			discard_line.append(player1_hand.pop())
	elif player2_turn:
		if discard_prob <= 0.5:
			discard_line.append(player2_hand.pop())
	else:
		print("Error: nobody's turn.")

print(len(player1_hand))
print(len(player2_hand))
# CURRENT ERROR: POP FROM EMPTY LIST (UNSOLVED ISSUE)




# print(deck)
# print(discard_line)
# print(player1_hand)
# print(player2_hand)
# print(len(deck))





run = False #skip the window creation while debugging
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False

	screen.fill(bg)

	for loc in card_locations:
		pygame.draw.rect(screen,card_colour,loc)

	pygame.display.update()


pygame.quit()