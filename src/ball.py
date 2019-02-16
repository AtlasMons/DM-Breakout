from pygame import Rect


class Ball:
    def __init__(self, x, y, v):
        self.x = x
        self.y = y
        self.x_velocity = v
        self.y_velocity = v
        self.width = 10
        self.rect = Rect(self.x - self.width / 2, self.y - self.width / 2,
                         self.width, self.width)

    def update_ball_pos(self):
        self.x += self.x_velocity
        self.y += self.y_velocity
        self.rect = Rect(self.x - self.width / 2, self.y - self.width / 2,
                         self.width, self.width)

    def reflect_x_velocity(self):
        self.x_velocity *= -1

    def reflect_y_velocity(self):
        self.y_velocity *= -1

    def apply_collision(self, brick):
        if abs(self.y + self.width / 2 - brick.top) < 5:
            self.y -= 5
            self.reflect_y_velocity()
        elif abs(self.y - self.width / 2 - brick.bottom) < 5:
            self.y += 5
            self.reflect_y_velocity()
        elif abs(self.x + self.width / 2 - brick.left) < 5:
            self.x -= 10
            self.reflect_x_velocity()
        elif abs(self.x - self.width / 2 - brick.right) < 5:
            self.x += 10
            self.reflect_x_velocity()