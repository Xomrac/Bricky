import pygame.freetype

class GameOverScreen:
	window : pygame.Surface
	is_hidden = True
	WIN_MESSAGE_TEMPLATE = "You Won!\nScore: {}\n\"R\" to Restart\n\"Q\" to Quit"
	LOSE_MESSAGE_TEMPLATE = "You Lost!\nScore: {}\n\"R\" to Restart\n\"Q\" to Quit"
	LINE_HEIGHT = 60
	has_won = False
	screen_center : tuple[int,int]
	game_font : pygame.freetype.Font

	message = ""
	def __init__(self, window: pygame.Surface, screen_center : tuple[int,int]):
		pygame.freetype.init()
		self.game_font = pygame.freetype.Font("Assets/Fonts/kenney_kenney-fonts/Kenney High.ttf", 64)
		self.window = window
		self.screen_center = screen_center

	def toggle_game_over(self, is_winner, score=0):
		self.has_won = is_winner
		if is_winner:
			self.message = self.WIN_MESSAGE_TEMPLATE.format(score)
		else:
			self.message = self.LOSE_MESSAGE_TEMPLATE.format(score)
			print(self.message)
		self.is_hidden = False
		
	def RenderUpdate(self):
		if self.is_hidden:
			return
		lines = self.message.split('\n')
		y_offset = self.screen_center[1] - (len(lines) * self.LINE_HEIGHT) // 2
		
		for i in range(0,len(lines),1):
			line = lines[i]
			if line.strip():
				color = (255, 255, 255)
				if i == 0:
					color = (0, 200, 0) if self.has_won else (200, 0, 0)
				text_surface, text_rect = self.game_font.render(line, fgcolor=color, bgcolor=(5, 5, 5))
				self.window.blit(text_surface, (self.screen_center[0] - text_rect.width // 2, y_offset))
			y_offset += self.LINE_HEIGHT