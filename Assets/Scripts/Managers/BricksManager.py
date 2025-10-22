from Actors.Brick import Brick
from random import choice
from Actors.Ball import Ball

class BricksManager:
	active_bricks : list[Brick] = []
	removed_bricks : list[Brick] = []
	ball : Ball
	MAX_BRICKS_WIDTH : int = 640
	SPACE_FROM_TOP : int = 50
	SPACE_FROM_EDGE : int = 2
	SPACE_BETWEEN_BRICKS : int = 2
	colors_index : int = -1
	possible_colors : list[tuple[int,int,int]] = [
		(251, 65, 65), # Red
		(255, 155, 47), # Orange
		(255, 215, 0), # Yellow
		(180, 229, 13), # Green
	]



	def __init__(self,rows: int, cols: int,screenSize: int, game_manager):
		self.active_bricks = []
		self.removed_bricks = []
		self.game_manager = game_manager
		self.ball = self.game_manager.ball
		brick_width = (screenSize - (self.SPACE_FROM_EDGE * 2) - (self.SPACE_BETWEEN_BRICKS * (cols - 1))) // cols
		if brick_width > self.MAX_BRICKS_WIDTH:
			brick_width = self.MAX_BRICKS_WIDTH
		
		total_bricks_width = cols * brick_width + (cols - 1) * self.SPACE_BETWEEN_BRICKS

		remaining_space = screenSize - total_bricks_width
		start_x = remaining_space // 2
		
		brick_height = brick_width // 2
		for row in range(rows):
			self.colors_index = (self.colors_index + 1) % len(self.possible_colors)
			for col in range(cols):
				x = start_x + col * (brick_width + self.SPACE_BETWEEN_BRICKS)
				y = self.SPACE_FROM_TOP + row * (brick_height + self.SPACE_BETWEEN_BRICKS)
				brick = Brick(x, y, brick_width, brick_height, self.possible_colors[self.colors_index], game_manager)
				self.active_bricks.append(brick)

	def RenderUpdate(self, surface):
		for brick in self.active_bricks + self.removed_bricks:
			brick.RenderUpdate(surface)
	
	def Update(self):
		for brick in self.active_bricks:
			if brick.rect.colliderect(self.ball.rect):

				overlap_left = self.ball.rect.right - brick.rect.left
				overlap_right = brick.rect.right - self.ball.rect.left
				overlap_top = self.ball.rect.bottom - brick.rect.top
				overlap_bottom = brick.rect.bottom - self.ball.rect.top
				
				min_overlap = min(overlap_left, overlap_right, overlap_top, overlap_bottom)
				

				if min_overlap == overlap_top or min_overlap == overlap_bottom:
					self.ball.bounce((self.ball.direction[0], -self.ball.direction[1]))
				else:
					self.ball.bounce((-self.ball.direction[0], self.ball.direction[1]))
				
				brick.destroy()
				self.game_manager.add_score(brick.score_reward)
				self.ball.Speed_Up()
				self.active_bricks.remove(brick)
				self.removed_bricks.append(brick)

	def all_bricks_destroyed(self) -> bool:
		return len(self.active_bricks) == 0