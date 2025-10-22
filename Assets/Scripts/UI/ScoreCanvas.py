import pygame.freetype

class ScoreCanvas:
	window : pygame.Surface
	distance_from_top : int = 5
	game_font : pygame.freetype.Font
	screen_center : int
	score : int = 0

	def __init__(self, window: pygame.Surface, screen_center : int, score: int = 0):
		pygame.freetype.init()
		self.game_font = pygame.freetype.Font("Assets/Fonts/kenney_kenney-fonts/Kenney High.ttf", 64)
		self.window = window
		self.screen_center = screen_center
		self.score = score

		
	def UpdateScore(self, score: int):
		self.score = score
		text_surface, text_rect = self.game_font.render(f"Score: {self.score}", fgcolor=(255, 255, 255), bgcolor=(5, 5, 5))
		self.window.blit(text_surface, (self.screen_center - text_rect.width // 2, self.distance_from_top))
		