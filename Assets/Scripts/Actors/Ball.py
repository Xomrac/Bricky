import pygame
import math
from pygame.locals import K_LEFT, K_RIGHT
from random import choice

class Ball(pygame.sprite.Sprite):
	x_bounds : tuple[int,int]
	y_bounds : tuple[int,int]
	pixel_per_frame : int = 7
	speed_multiplier : float = 1.0
	multiplier_increment : float = 0.02
	direction : tuple[float,float]
	bounce_wall_sounds_paths = [
	"Assets/Sounds/kenney_impact-sounds/impactSoft_medium_000.ogg",
	"Assets/Sounds/kenney_impact-sounds/impactSoft_medium_001.ogg",
	"Assets/Sounds/kenney_impact-sounds/impactSoft_medium_002.ogg",
	"Assets/Sounds/kenney_impact-sounds/impactSoft_medium_003.ogg",
	"Assets/Sounds/kenney_impact-sounds/impactSoft_medium_004.ogg"
	]
	bounce_wall_sounds : list[pygame.mixer.Sound]
	bounce_wall_sound_channel : pygame.mixer.Channel
	SOUND_VOLUME = 0.2

	def __init__(self,screen_size : tuple[int,int]):
		super().__init__() 
		self.image = pygame.image.load("Assets/Sprites/kenney_puzzle-pack/ballGrey.png")
		self.rect = self.image.get_rect()
		self.rect.center = (screen_size[0] // 2, screen_size[1] // 2)
		self.x_bounds = (0, screen_size[0])
		self.y_bounds = (0, screen_size[1])
		random_x = choice([-.4,.4])
		random_y = choice([.8,1])
		self.direction = (random_x, random_y)
		self.bounce_wall_sound_channel = pygame.mixer.Channel(4)
		self.bounce_wall_sounds = [pygame.mixer.Sound(path) for path in self.bounce_wall_sounds_paths]

	def update(self):
		step = self.pixel_per_frame * self.speed_multiplier
		direction_magnitude = math.sqrt(self.direction[0]**2 + self.direction[1]**2)
		if direction_magnitude > 0:
			normalized_direction = (self.direction[0] / direction_magnitude, self.direction[1] / direction_magnitude)
		else:
			normalized_direction = self.direction
		movement_vector = (normalized_direction[0] * step, normalized_direction[1] * step)
		self.rect.move_ip(movement_vector)
		self.handle_window_bounds()
		self.clamp_position()

	def bounce(self,new_direction : tuple[float,float], playSound: bool = True):
		self.direction = new_direction
		if playSound:
			sound = choice(self.bounce_wall_sounds)
			sound.set_volume(self.SOUND_VOLUME)
			self.bounce_wall_sound_channel.play(sound)

	def handle_window_bounds(self):
		if self.rect.left <= self.x_bounds[0] or self.rect.right >= self.x_bounds[1]:
			self.bounce(( -self.direction[0], self.direction[1]))

		if self.rect.top <= self.y_bounds[0] or self.rect.bottom >= self.y_bounds[1]:
			self.bounce(( self.direction[0], -self.direction[1]))

	def clamp_position(self):
		if self.rect.left < self.x_bounds[0]:
			self.rect.left = self.x_bounds[0]
		if self.rect.right > self.x_bounds[1]:
			self.rect.right = self.x_bounds[1]
		if self.rect.top < self.y_bounds[0]:
			self.rect.top = self.y_bounds[0]
		if self.rect.bottom > self.y_bounds[1]:
			self.rect.bottom = self.y_bounds[1]

	def RenderUpdate(self, surface):
		surface.blit(self.image, self.rect)
	
	def Speed_Up(self):
		self.speed_multiplier += self.multiplier_increment