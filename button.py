import pygame

class Button:
	def __init__(self,size,position,colour,text=""):
		"""
		Every button has a size (tuple: width,height down and to the right),
		a position (tuple: x,y of the top left corner of the button),
		a colour (tuple: R,G,B values),
		and its associated text (defaults to an empty string).
		"""
		self.width = size[0]
		self.height = size[1]
		self.x = position[0]
		self.y = position[1]
		self.colour = colour #RGB tuple
		self.text = text #defaults to an empty string

	def exist(self,screen):
		"""Display the button and make it operational."""
		button_location = (self.x,self.y,self.width,self.height)
		
		# Get the mouse position for button shading effects
		mouse_position = pygame.mouse.get_pos()

		# Set the text to be displayed on the button
		font = pygame.font.SysFont("Arial",14)
		text_surface = font.render(self.text, True, (0,0,0))
		text_rect = text_surface.get_rect()
		text_rect.center = ((self.x + self.width/2),(self.y + self.height/2))

		if (self.x < mouse_position[0] < (self.x + self.width)) and (self.y < mouse_position[1] < (self.y + self.height)):
			# Cursor is hovering over the button
			pygame.draw.rect(screen,(220,220,220),button_location)
			screen.blit(text_surface, text_rect)
		else:
			# Cursor is not hovering over the button
			pygame.draw.rect(screen,self.colour,button_location)
			screen.blit(text_surface, text_rect)
