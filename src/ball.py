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
        self.x_velocity *= -1.

    def reflect_y_velocity(self):
        self.y_velocity *= -1.

    def speed_up(self):
        if self.x_velocity > 0:
            self.x_velocity = min(4., self.x_velocity + .25)
        else:
            self.x_velocity = max(-4., self.x_velocity - .25)
        if self.y_velocity > 0:
            self.y_velocity = min(5., self.y_velocity + .25)
        else:
            self.y_velocity = max(-5., self.y_velocity - .25)

    def apply_player_collision(self, player):
        self.y -= 5
        if abs(self.x - player.x) < player.width / 2:
            base_velocity = 4 * (self.x - player.x) / (player.width / 2)

            if 0 <= base_velocity < .25:
                base_velocity = .25
            elif -.25 < base_velocity < 0:
                base_velocity = -.25

            self.reflect_y_velocity()
            self.x_velocity = base_velocity
        else:
            self.reflect_x_velocity()

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
            if (self.x_velocity > 0 and self.x < bricks[0].left) or \
                    (self.x_velocity <= 0 and self.x > bricks[0].right):
                self.reflect_x_velocity()
            else:
                self.reflect_y_velocity()
