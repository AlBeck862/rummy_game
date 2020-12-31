"""
Details here
"""

import pygame
import random
from rummy_fxns import *
from button import Button
from deck import Deck
# import numpy as np

# Initialize PyGame
pygame.init()

# Initialize the clock
# clock = pygame.time.Clock()

# Window parameters
size = width, height = 1100,700
bg = 0,180,0 #green background
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Rummy 500")

# Card parameters
card_size = [50,100]
card_colour = 0,0,0
card_locations = [(50,50,card_size[0],card_size[1]),(150,50,card_size[0],card_size[1]),(250,50,card_size[0],card_size[1])]

run = True
while run:

	for event in pygame.event.get():
		if event.type == pygame.QUIT: 
			pygame.quit()
			quit()

	screen.fill(bg)

	test = Button((75,75),(450,100),(0,0,0))
	test.create(screen)

	for loc in card_locations:
		pygame.draw.rect(screen,card_colour,loc)

	pygame.display.update()


## PLAN ##
# one loop for the game/screen refresh --> must be triggered every time an action of any kind is taken (how do I implement this?)
# one loop to play the hand
# one loop to play the game (includes many hands)
## PLAN ##

## IDEAS ##
# create a "game" class that contains all game info like the current deck, the current scores, player names?
## IDEAS ##


### PUT ALL OF THIS INTO ANOTHER LOOP THAT ENDS WHEN A SCORE OF 500 IS REACHED --> "game loop"

# Initialize a new hand of Rummy 500
deck,discard_line,player1_hand,player2_hand = start_new_hand()

# Set the turn order
player1_turn = True
player2_turn = False

# Play the hand. The hand ends when one player no longer has any cards in hand. --> "hand loop"
while (len(player1_hand) != 0) and (len(player2_hand) != 0) and not deck.check_if_empty():
	
	# First player's turn
	if player1_turn:
		player1_hand.append(deck.draw()) #pick a card from deck
		
		# Display the player's current hand.
		print("This is your hand:")
		print(player1_hand)

		# Check for and declare triplets in the player's hand.
		triplets = has_triplet(player1_hand)
		for key in triplets:
			if triplets[key]:
				print("You have a triplet of " + str(key) + "'s!")
		
		# Check for and declare quartets in the player's hand.
		quartets = has_quartet(player1_hand)
		for key in quartets:
			if quartets[key]:
				print("You have a quartet of " + str(key) + "'s!")
				
		# Check for and declare straights in the player's hand.
		straights = has_straight(player1_hand) #fetch straight data
		suit_types = ["Hearts","Diamonds","Clubs","Spades"]
		card_options = ["Ace","2","3","4","5","6","7","8","9","10","Jack","Queen","King","Ace"]
		for straight in straights:
			if straight:
				suit_type = suit_types[straight[0]-1]
				first_card = card_options[straight[1]]
				last_card = card_options[straight[2]]
				print("You have a straight from the " + first_card + " to the " + last_card + " of " + suit_type + "!")
		
		# print("What would you like to do? Type the number of the desired option.")
		# print("Option #1: Discard to the discard line and end your turn.")
		# print("Option #2: Discard a triplet to your tabletop.")
		# print("Option #3: Discard a quartet to your tabletop.")
		# print("Option #4: Discard a straight to your tabletop.")
		# print("\n")

		# decision_making = True
		# while decision_making:

		# 	option = input()

		# 	if option == 1:
		# 		print("This is your hand:")
		# 		print(player1_hand)
		# 		while True:
		# 			print("What would you like to discard? Type the card as shown.")
		# 			discard = input()

		# 			if discard.lower() in [item.lower() for item in player1_hand]:
		# 				# Move that card from the hand to the discard line.
		# 				break
		# 			else:
		# 				print("Invalid card. Try again.")

			# elif option == 2:
			# 	pass
			# elif option == 3:
			# 	pass
			# elif option == 4:
			# 	pass
			# else:
			# 	print("Invalid option number. Try again.")




		#list what player has in hand (all cards + triplets, straights, etc.) ***(DONE)***
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

# Quit PyGame
pygame.quit()