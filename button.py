import pygame

class Button:
	def __init__(self,size,position,colour,text=""):
		"""
		Every button has a size (tuple: width,height down and to the right),
		a position (tuple: x,y of the top left corner of the button),
		a colour (tuple: R,G,B values),
		and its associated text (defaults to blank).
		"""
		self.width = size[0]
		self.height = size[1]
		self.x = position[0]
		self.y = position[1]
		self.colour = colour #RGB tuple

	def show(self,screen):
		"""Display the button."""
		button_location = (self.x,self.y,self.width,self.height)
		pygame.draw.rect(screen,self.colour,button_location)