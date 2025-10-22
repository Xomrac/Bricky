import pygame
from pygame import Surface

class GameWindow:
	GAME_NAME = "Bricky"
	GAME_ICON = "Assets/Sprites/game_icon.png"
	BACKGROUND_COLOR = (0, 0, 0)
	SIZE = (502, 700)
	
	window : Surface
	
	def __init__(self):
		self.window = pygame.display.set_mode(self.SIZE)
		pygame.display.set_caption(self.GAME_NAME)
		pygame.display.set_icon(pygame.image.load(self.GAME_ICON))
	
	def RenderUpdate(self):
		self.window.fill(self.BACKGROUND_COLOR)
