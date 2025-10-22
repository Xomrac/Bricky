
import pygame


class Brick:
	
    rect : pygame.Rect
    is_destroyed : bool = False
    score_reward : int = 100
    animation_duration : float = .6 # seconds
    is_animating_shrink : bool = False
    elapsed_time : float = 0.0
    color : tuple[int,int,int]
    start_time : float = 0.0
    original_width : int = 0
    original_height : int = 0
    destruction_sound_path = "Assets/Sounds/kenney_digital-audio/powerUp7.ogg"
    destruction_sound : pygame.mixer.Sound
    destruction_sound_channel : pygame.mixer.Channel
    SOUND_VOLUME = 0.2

    def __init__(self, x, y, width, height, color: tuple[int,int,int], game_manager):
        self.rect = pygame.Rect(x, y, width, height)
        self.original_width = width
        self.original_height = height
        self.is_destroyed = False
        self.game_manager = game_manager
        self.color = color
        self.is_destroyed = False
        self.is_animating_shrink = False
        self.start_time = 0.0
        self.elapsed_time = 0.0
        self.destruction_sound = pygame.mixer.Sound(self.destruction_sound_path)
        self.destruction_sound.set_volume(self.SOUND_VOLUME)
        self.destruction_sound_channel = pygame.mixer.Channel(3)

    def RenderUpdate(self, surface):
        self.animate_shrink()
        if not self.is_destroyed or self.is_animating_shrink:
            pygame.draw.rect(surface, self.color, self.rect)


    def destroy(self):
        self.is_animating_shrink = True
        self.is_destroyed = True
        self.destruction_sound_channel.play(self.destruction_sound)
        self.start_time = pygame.time.get_ticks()

    def animate_shrink(self):
        if not self.is_animating_shrink:
            return

        current_time = pygame.time.get_ticks()
        self.elapsed_time = (current_time - self.start_time) / 1000.0
        
        if self.elapsed_time <= self.animation_duration:
            eased_time = self.easeOutBack(self.elapsed_time / self.animation_duration)
            shrink_ratio = eased_time
            new_width = int(self.original_width * (1 - shrink_ratio))
            new_height = int(self.original_height * (1 - shrink_ratio))
            center_x = self.rect.centerx
            center_y = self.rect.centery
            self.rect.width = new_width
            self.rect.height = new_height
            self.rect.centerx = center_x
            self.rect.centery = center_y
        else:
            self.is_animating_shrink = False

    def easeOutBack(self, x: float) -> float:
        c1 = 1.70158
        c3 = c1 + 1
        return 1 + c3 * (x - 1) ** 3 + c1 * (x - 1) ** 2
    
    def easePunchOut(self, x: float) -> float:
        if x < 0.5:
            return self.easeOutBack(x * 2) / 2
        else:
            return (1 - self.easeOutBounce((1 - x) * 2)) / 2 + 0.5

    def easeOutBounce(self, x: float) -> float:
        n1 = 7.5625
        d1 = 2.75

        if x < 1 / d1:
            return n1 * x * x
        elif x < 2 / d1:
            x -= 1.5 / d1
            return n1 * x * x + 0.75
        elif x < 2.5 / d1:
            x -= 2.25 / d1
            return n1 * x * x + 0.9375
        else:
            x -= 2.625 / d1
            return n1 * x * x + 0.984375