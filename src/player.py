from pygame import Rect


class Player:
    # TODO: Possibly want to add acceleration to player's movement

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 120
        self.height = 15
        self.rect = Rect(self.x - self.width / 2, self.y - self.height / 2,
                         self.width, self.height)
        self.incr = 8
        # how many pixels the player moves with each input

    def move_left(self, bar_width):
        self.x = max(bar_width + self.width / 2, self.x - self.incr)
        # cannot go off left side of screen
        self.update_rect()

    def move_right(self, bar_width, window_width):
        self.x = min(window_width - bar_width - self.width / 2,
                     self.x + self.incr)
        # cannot go off right side of screen
        self.update_rect()

    def update_rect(self):
        self.rect = Rect(self.x - self.width / 2, self.y - self.height / 2,
                         self.width, self.height)
