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

    def update_ball_pos(self, delta_x, delta_y):
        self.x += delta_x
        self.y += delta_y
        self.rect = Rect(self.x - self.width / 2, self.y - self.width / 2,
                         self.width, self.width)

    def reflect_x_velocity(self):
        self.x_velocity *= -1

    def reflect_y_velocity(self):
        self.y_velocity *= -1

    def apply_collision(self, bricks):
        assert len(bricks) < 4, "This collision is not possible"
        if len(bricks) == 0:
            return
        elif len(bricks) == 3:
            self.reflect_y_velocity()
            self.reflect_x_velocity()
        elif len(bricks) == 2:
            if ((self.x > bricks[0].centerx and self.x > bricks[1].centerx) or
                    (self.x < bricks[0].centerx and self.x < bricks[1].centerx)):
                self.reflect_x_velocity()
            elif ((self.y > bricks[0].centery and self.y > bricks[1].centery) or
                  (self.y < bricks[0].centery and self.y < bricks[1].centery)):
                self.reflect_y_velocity()
            else:
                self.reflect_y_velocity()
                self.reflect_x_velocity()
        else:  # len == 1
            if self.x_velocity > 0:
                if self.x < bricks[0].left:
                    self.reflect_x_velocity()
                else:
                    self.reflect_y_velocity()
            else:
                if self.x > bricks[0].right:
                    self.reflect_x_velocity()
                else:
                    self.reflect_y_velocity()
        # if abs(self.y + self.width / 2 - brick.top) < self.y_velocity:
        #     self.reflect_y_velocity()
        # elif abs(self.y - self.width / 2 - brick.bottom) < self.y_velocity:
        #     self.reflect_y_velocity()
        # elif abs(self.x + self.width / 2 - brick.left) < self.x_velocity:
        #     self.reflect_x_velocity()
        # elif abs(self.x - self.width / 2 - brick.right) < self.x_velocity:
        #     self.reflect_x_velocity()
