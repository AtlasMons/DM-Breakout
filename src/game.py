import pygame
import random

from src.player import Player
from src.ball import Ball
from src.constants import *
from pygame.locals import *


class Game:
    def __init__(self):

        self.ball = Ball(WINDOWWIDTH / 2, BRICKCEILING + 200, 1.0)
        self.player = Player(WINDOWWIDTH / 2, WINDOWHEIGHT - 10)
        # y-coord is fixed, player can only move along x-axis
        self.is_brick = [[True for _ in range(ROWSIZE)] for _ in BRICKCOLORS]
        self.score = 0
        self.lives = 0
        self.level = 1

    def draw_player(self, disp):
        pygame.draw.rect(disp, RED, self.player.rect)

    def draw_bricks(self, disp):
        brick_rects = []
        for row in range(len(BRICKCOLORS)):
            brick_rects.append([])
            for col in range(ROWSIZE):
                brick_rect = pygame.Rect(BARWIDTH + col * BRICKWIDTH,
                                         BRICKCEILING + row * BRICKHEIGHT,
                                         BRICKWIDTH, BRICKHEIGHT)
                brick_rects[row].append(brick_rect)
                if self.is_brick[row][col]:
                    pygame.draw.rect(disp, BRICKCOLORS[row], brick_rect)
        return brick_rects

    def draw_scoreboard(self, time, disp):
        font_obj = pygame.font.Font('freesansbold.ttf', 60)
        board_str = ' %05.1f    %03d      %d      %d' % \
                    (time, self.score, self.lives, self.level)
        text_surface_obj = font_obj.render(board_str, True, GRAY, BLACK)
        text_rect_obj = text_surface_obj.get_rect()
        text_rect_obj.center = (520, 45)
        disp.blit(text_surface_obj, text_rect_obj)

    def draw_ball(self, disp):
        pygame.draw.rect(disp, RED, self.ball.rect)

    def check_border_collisions(self, border_rects):
        if self.ball.rect.colliderect(self.player.rect):
            self.ball.apply_player_collision(self.player)
            self.ball.speed_up()
        elif self.ball.rect.colliderect(border_rects[0]):
            self.ball.reflect_y_velocity()
        elif self.ball.rect.colliderect(border_rects[1]):
            self.ball.reflect_x_velocity()
            self.ball.update_ball_pos(5, 0)
        elif self.ball.rect.colliderect(border_rects[2]):
            self.ball.reflect_x_velocity()
            self.ball.update_ball_pos(-5, 0)

    def check_brick_collisions(self, brick_rects):
        collided_bricks = []
        for row in range(len(brick_rects)):
            for col in range(len(brick_rects[0])):
                if (self.ball.rect.colliderect(brick_rects[row][col]) and
                        self.is_brick[row][col]):
                    collided_bricks.append(brick_rects[row][col])
        if not collided_bricks:
            return
        self.ball.apply_collision(collided_bricks)
        return random.choice(collided_bricks)

    def check_player_inputs(self, keys):
        if keys[K_a] or keys[K_LEFT]:
            self.player.move_left(BARWIDTH)
        elif keys[K_d] or keys[K_RIGHT]:
            self.player.move_right(BARWIDTH, WINDOWWIDTH)

    def is_win(self):
        for row in self.is_brick:
            if True in row:
                return False
        return True
