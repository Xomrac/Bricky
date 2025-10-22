import pygame
from pygame.locals import K_LEFT, K_RIGHT, K_a, K_d
from Actors.Ball import Ball

class Paddle(pygame.sprite.Sprite):
	max_width : int = 640
	pixel_per_frame : int = 5
	speed_multiplier : float = 1.0
	ball : Ball 

	def __init__(self,startpos : tuple[int,int],screen_size : tuple[int,int], ball : Ball):
		super().__init__() 
		self.image = pygame.image.load("Assets/Sprites/kenney_puzzle-pack/paddleBlu.png")
		self.rect = self.image.get_rect()
		startpos = (startpos[0], screen_size[1]-(startpos[1] + self.rect.height // 2))
		self.rect.center = startpos
		self.max_width = screen_size[0]
		self.ball = ball

	def update(self):
		pressed_keys = pygame.key.get_pressed()

		if self.rect.left > 0:
			if pressed_keys[K_LEFT] or pressed_keys[K_a]:
				self.move(-1)
		if self.rect.right < self.max_width:
			if pressed_keys[K_RIGHT] or pressed_keys[K_d]:
				self.move(1)
		if self.rect.colliderect(self.ball.rect):
			ball_center_x = self.ball.rect.centerx
			paddle_center_x = self.rect.centerx
			hit_pos = (ball_center_x - paddle_center_x) / (self.rect.width // 2)
			new_direction = (hit_pos, -abs(self.ball.direction[1]))
			self.ball.bounce(new_direction)

	def move(self,direction : int):
		self.rect.move_ip(direction * self.pixel_per_frame * self.speed_multiplier, 0)

	def RenderUpdate(self, surface):
		surface.blit(self.image, self.rect)