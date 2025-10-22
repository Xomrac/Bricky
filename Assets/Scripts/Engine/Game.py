import pygame
import sys
from Engine.GameWindow import GameWindow
from Actors.Paddle import Paddle
from Actors.Ball import Ball
from pygame import QUIT
from UI.GameOverScreen import GameOverScreen
from pygame.locals import K_q, K_r
from Managers.BricksManager import BricksManager
from UI.ScoreCanvas import ScoreCanvas

class GameManager:
	game_window : GameWindow
	game_over_screen : GameOverScreen
	bricks_manager : BricksManager
	score_canvas : ScoreCanvas
	is_running = False
	clock : pygame.time.Clock
	tick_rate = 60
	paddle : Paddle
	ball : Ball
	score : int = 0
	ost_path : str = "Assets/Sounds/ost.wav"
	win_jingle_path : str = "Assets/Sounds/kenney_music-jingles/Audio/8-Bit jingles/jingles_NES12.ogg"
	lose_jingle_path : str = "Assets/Sounds/kenney_music-jingles/Audio/8-Bit jingles/jingles_NES13.ogg"
	ost_sound : pygame.mixer.Sound
	win_jingle_sound : pygame.mixer.Sound
	lose_jingle_sound : pygame.mixer.Sound
	ost_channel : pygame.mixer.Channel
	win_jingle_channel : pygame.mixer.Channel
	lose_jingle_channel : pygame.mixer.Channel

	PLAYER_VERTICAL_OFFSET : int = 25
	LOSE_ZONE_HEIGHT : int = 20
	BLOCKS_COLS : int = 10
	BLOCKS_ROWS : int = 4

	def __init__(self):
		pygame.init()
		pygame.mixer.init()
		pygame.mixer.set_reserved(5)
		self.ost_channel = pygame.mixer.Channel(0)
		self.win_jingle_channel = pygame.mixer.Channel(1)
		self.lose_jingle_channel = pygame.mixer.Channel(2)

		self.ost_sound = pygame.mixer.Sound(self.ost_path)
		self.ost_sound.set_volume(1)
		self.ost_channel.play(self.ost_sound, loops=-1)

		self.win_jingle_sound = pygame.mixer.Sound(self.win_jingle_path)
		self.win_jingle_sound.set_volume(.5)
		self.lose_jingle_sound = pygame.mixer.Sound(self.lose_jingle_path)
		self.lose_jingle_sound.set_volume(.5)
		self.game_window = GameWindow()
		self.score_canvas = ScoreCanvas(self.game_window.window, self.game_window.SIZE[0] // 2, self.score)
		self.clock = pygame.time.Clock()
		self.game_over_screen = GameOverScreen(self.game_window.window, (self.game_window.SIZE[0] // 2, self.game_window.SIZE[1] // 2))
		self.is_running = True
		self.score = 0
		self.ball = Ball(self.game_window.SIZE)
		start_pos = (self.game_window.SIZE[0] // 2, self.PLAYER_VERTICAL_OFFSET)
		self.paddle = Paddle(start_pos, self.game_window.SIZE, self.ball)
		self.bricks_manager = BricksManager(self.BLOCKS_ROWS, self.BLOCKS_COLS, self.game_window.SIZE[0], self)

	def GameLoop(self):
		self.EngineUpdate()
		if self.is_running:
			self.ActorsUpdate()		
		self.RenderUpdate()
		if self.has_lost() and self.is_running:
			self.ost_channel.stop()
			self.lose_jingle_channel.play(self.lose_jingle_sound)
			self.game_over_screen.toggle_game_over(False, self.score)
			self.is_running = False
		elif not self.is_running:
			pressed_keys = pygame.key.get_pressed()
			if pressed_keys[K_q]:
				pygame.quit()
				sys.exit()
			if pressed_keys[K_r]:
				self.__init__()
		self.clock.tick(self.tick_rate)

	def EngineUpdate(self):
		if self.is_quitting():
			pygame.quit()
			sys.exit()

	def ActorsUpdate(self):
		self.paddle.update()
		self.ball.update()
		self.bricks_manager.Update()
		if self.bricks_manager.all_bricks_destroyed() and self.is_running:
			self.ost_channel.stop()
			self.win_jingle_channel.play(self.win_jingle_sound)
			self.game_over_screen.toggle_game_over(True, self.score)
			self.is_running = False

	def RenderUpdate(self):
		self.game_window.RenderUpdate()
		self.paddle.RenderUpdate(self.game_window.window)
		self.ball.RenderUpdate(self.game_window.window)
		self.bricks_manager.RenderUpdate(self.game_window.window)
		self.game_over_screen.RenderUpdate()
		self.score_canvas.UpdateScore(self.score)
		pygame.display.update()
	
	def add_score(self, points: int):
		self.score = self.score + points
		self.score_canvas.score = self.score
		

	def has_lost(self) -> bool:
		return self.ball.rect.center[1] >= self.game_window.SIZE[1] - self.LOSE_ZONE_HEIGHT

	def is_quitting(self) -> bool:
		for event in pygame.event.get():
			if event.type == QUIT:
				return True
		return False