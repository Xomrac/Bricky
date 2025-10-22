import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Assets', 'Scripts'))

from Engine.Game import GameManager

if __name__ == "__main__":
	game = GameManager()
	while True:
		game.GameLoop()