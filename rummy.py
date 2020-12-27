"""
Details here
"""

import pygame
import random
from rummy_fxns import *
# import numpy as np

# Initialize PyGame
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

### PUT ALL OF THIS INTO ANOTHER LOOP THAT ENDS WHEN A SCORE OF 500 IS REACHED

# Initialize a new hand of Rummy 500
deck,discard_line,player1_hand,player2_hand = start_new_hand()

# Set the turn order
player1_turn = True
player2_turn = False

# Play the hand. The hand ends when one player no longer has any cards in hand.
while (len(player1_hand) != 0) and (len(player2_hand) != 0):
	
	# First player's turn
	if player1_turn:
		player1_hand.append(deck.pop(0)) #pick a card from deck
		
		# Display the player's current hand.
		print("This is your hand:")
		print(player1_hand)

		# Check for and declare triplets in the player's hand.
		triplets = has_triplet(player1_hand)
		for key in triplets:
			if triplets[key]:
				print("You have a triplet of " + str(key).upper() + "'s!")
		
		# Check for and declare quartets in the player's hand.		
		quartets = has_quartet(player1_hand)
		for key in quartets:
			if quartets[key]:
				print("You have a quartet of " + str(key).upper() + "'s!")
				

		straights = has_straight(player1_hand)
		break
		for key in straights:
			pass

		#list what player has in hand (all cards + triplets, straights, etc.)
		#"do you want to discard [available combos] to the tabletop?"
		#which card do you want to discard to the discard line?
		#discard that card to the discard line

		# Switch to the other player's turn
		player1_turn = False
		player2_turn = True
	
	# Second player's turn
	elif player2_turn:
		pass
		
		# Switch to the other player's turn
		player1_turn = True
		player2_turn = False
	
	# Failsafe
	else:
		print("Error: nobody's turn.")

### END OF SCORE LOOP


run = False #skip the window creation while debugging
while run:
	for event in pygame.event.get():
		if event.type == pygame.QUIT: run = False

	screen.fill(bg)

	for loc in card_locations:
		pygame.draw.rect(screen,card_colour,loc)

	pygame.display.update()

# Quit PyGame
pygame.quit()