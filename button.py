import pygame

BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (200,200,200)

class TextButton():
	def __init__(self,size,position,colour=WHITE,rollover_colour=GREY,text="",text_size=14,text_colour=BLACK,font="Arial",action=None):
		"""
		size: tuple, (width,height)
		position: tuple, (x,y of the top left corner of the button)
		colour: tuple, (R,G,B), defaults to white
		text: string, defaults to empty string
		text_size: int, defaults to 14
		text_colour: tuple, (R,G,B), defaults to black
		font: string, defaults to Arial
		action: function, defaults to None (image with roll-over effect)
		"""
		self.width = size[0]
		self.height = size[1]
		self.x = position[0]
		self.y = position[1]
		self.colour = colour
		self.rollover_colour = rollover_colour
		self.text = text #defaults to an empty string
		self.text_size = text_size
		self.text_colour = text_colour
		self.font = font
		self.action = action #the function to run when the button is clicked

	def exist(self,screen):
		"""Display the button and make it operational."""
		button_location = (self.x,self.y,self.width,self.height)
		
		# Get the mouse position for button shading effects
		mouse_position = pygame.mouse.get_pos()

		# Stores the left click in click[0]
		click = pygame.mouse.get_pressed()

		# Set the text to be displayed on the button
		font = pygame.font.SysFont(self.font,self.text_size)
		text_surface = font.render(self.text, True, self.text_colour)
		text_rect = text_surface.get_rect()
		text_rect.center = ((self.x + self.width/2),(self.y + self.height/2))

		if (self.x < mouse_position[0] < (self.x + self.width)) and (self.y < mouse_position[1] < (self.y + self.height)):
			# Cursor is hovering over the button
			pygame.draw.rect(screen,self.rollover_colour,button_location,border_radius=(self.height//2))
			screen.blit(text_surface, text_rect)

			# If the mouse is clicked, execute the function
			if (click[0] == 1) and (self.action != None):
				self.action() 

		else:
			# Cursor is not hovering over the button
			pygame.draw.rect(screen,self.colour,button_location,border_radius=(self.height//2))
			screen.blit(text_surface, text_rect)

class ImageButton():
	def __init__(self,size,position,image,text="",text_size=14,text_colour=BLACK,font="Arial",action=None,offset=None,last_element=False):
		"""
		size: tuple, (width,height)
		position: tuple, (x,y of the top left corner of the button)
		image: loaded PyGame image
		text: string, defaults to empty string
		text_size: int, defaults to 14
		text_colour: tuple, defaults to black
		font: string, defaults to Arial
		action: function, defaults to None (image with roll-over effect)
		offset: int, defaults to None (not a line of images with a set overlap)
		last_element: bool, defaults to False (not the last element in the line of images, not used if offset is None)
		"""
		self.width = size[0]
		self.height = size[1]
		self.x = position[0]
		self.y = position[1]
		self.image = image
		self.text = text #defaults to an empty string
		self.text_size = text_size
		self.text_colour = text_colour
		self.font = font
		self.action = action #the function to run when the button is clicked
		self.offset = offset
		self.last_element = last_element

	def exist(self,screen):
		"""Display the button and make it operational."""
		button_location = (self.x,self.y,self.width,self.height)
		
		# Get the mouse position for button shading effects
		mouse_position = pygame.mouse.get_pos()

		# Stores the left click in click[0]
		click = pygame.mouse.get_pressed()

		# Set the text to be displayed on the button
		font = pygame.font.SysFont(self.font,self.text_size)
		text_surface = font.render(self.text, True, self.text_colour)
		text_rect = text_surface.get_rect()
		text_rect.center = ((self.x + self.width/2),(self.y + self.height/2))

		if (self.x < mouse_position[0] < (self.x + self.width)) and (self.y < mouse_position[1] < (self.y + self.height)):
			# Scale and display the image
			self.image = pygame.transform.scale(self.image,(self.width,self.height)) #failsafe if image is not pre-scaled, might be redundant in some cases
			screen.blit(self.image,(self.x,self.y))

			# Display a black box around the selected card (logic necessary for image lines with a set offset)
			if (self.offset is not None) and not self.last_element and (self.x < mouse_position[0] < (self.x + self.offset)) and (self.y < mouse_position[1] < (self.y + self.height)): #it is an image line, it is not the last element in the line
				pygame.draw.rect(screen, BLACK, (self.x,self.y,self.width,self.height), width=5)

				# If the mouse is clicked, execute the function
				if (click[0] == 1) and (self.action != None):
					self.action()

			elif (self.offset is not None) and self.last_element and (self.x < mouse_position[0] < (self.x + self.width)) and (self.y < mouse_position[1] < (self.y + self.height)): #it is an image line, it is the last element in the line
				pygame.draw.rect(screen, BLACK, (self.x,self.y,self.width,self.height), width=5)

				# If the mouse is clicked, execute the function
				if (click[0] == 1) and (self.action != None):
					self.action()

			elif self.offset is None: # it is not an image line
				pygame.draw.rect(screen, BLACK, (self.x,self.y,self.width,self.height), width=5)
				
				# If the mouse is clicked, execute the function
				if (click[0] == 1) and (self.action != None):
					self.action()

			# Display the text over the button, if applicable
			screen.blit(text_surface, text_rect)

		else:
			# Cursor is not hovering over the button
			self.image = pygame.transform.scale(self.image,(self.width,self.height))
			screen.blit(self.image,(self.x,self.y))
			screen.blit(text_surface, text_rect)