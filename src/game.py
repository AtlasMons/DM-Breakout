import pygame
import sys

from src.player import Player
from src.ball import Ball
from pygame.locals import *

WINDOWWIDTH = 960
WINDOWHEIGHT = 630

HEADERHEIGHT = 90

BARWIDTH = 40
BARHEIGHT = 520

BRICKWIDTH = 40
BRICKHEIGHT = 20
BRICKCEILING = 210
# height at which bricks begin appearing
ROWSIZE = 22
# number of bricks per row


FPS = 120

# RGB values for colors
GRAY        = (141, 139, 141)
RED         = (190,  82,  71)
CYAN        = ( 57, 145, 133)
BLACK       = (  0,   0,   0)
ORANGE      = (206, 112,  55)
DARK_YELLOW = (188, 123,  46)
YELLOW      = (168, 158,  38)
GREEN       = ( 69, 150,  69)
BLUE        = ( 64,  80, 213)

BRICKCOLORS = [RED, ORANGE, DARK_YELLOW, YELLOW, GREEN, BLUE]


def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Breakout')
    border_rects = draw_borders()

    ball = Ball(WINDOWWIDTH / 2, BRICKCEILING + 200, 2)
    player = Player(WINDOWWIDTH / 2, WINDOWHEIGHT - 10)
    # y-coord is fixed, player can only move along x-axis
    is_brick = [[True for _ in range(ROWSIZE)] for _ in BRICKCOLORS]

    while True:
        draw_blank()
        brick_rects = draw_bricks(is_brick)
        draw_player(player.rect)
        draw_ball(ball.rect)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP
                                      and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        if ball.rect.colliderect(player.rect):
            ball.apply_collision(player.rect)
        elif ball.rect.colliderect(border_rects[0]):
            ball.reflect_y_velocity()
        elif ball.rect.collidelist(border_rects[1:3]) != -1:
            ball.reflect_x_velocity()

        # TODO: Fix buggy collision interactions
        for row in range(len(brick_rects) - 1, 0, -1):
            collision = ball.rect.collidelist(brick_rects[row])
            if collision != -1 and is_brick[row][collision]:
                brick = brick_rects[row][collision]
                is_brick[row][collision] = False
                ball.apply_collision(brick)

        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            player.move_left(BARWIDTH)

        elif keys[K_d] or keys[K_RIGHT]:
            player.move_right(BARWIDTH, WINDOWWIDTH)

        ball.update_ball_pos()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_borders():
    top_bar = pygame.Rect(0, HEADERHEIGHT, WINDOWWIDTH, BARWIDTH)
    left_bar = pygame.Rect(0, HEADERHEIGHT, BARWIDTH, BARHEIGHT)
    right_bar = pygame.Rect(WINDOWWIDTH - BARWIDTH, HEADERHEIGHT, BARWIDTH,
                            BARHEIGHT)
    cyan_bar = pygame.Rect(0, BARHEIGHT + HEADERHEIGHT, BARWIDTH, 20)
    red_bar = pygame.Rect(WINDOWWIDTH - BARWIDTH, BARHEIGHT + HEADERHEIGHT,
                      BARWIDTH, 20)

    pygame.draw.rect(DISPLAYSURF, GRAY, top_bar)
    pygame.draw.rect(DISPLAYSURF, GRAY, left_bar)
    pygame.draw.rect(DISPLAYSURF, GRAY, right_bar)
    pygame.draw.rect(DISPLAYSURF, CYAN, cyan_bar)
    pygame.draw.rect(DISPLAYSURF, RED, red_bar)

    return [top_bar, left_bar, right_bar, cyan_bar, red_bar]


def draw_player(player_rect):
    pygame.draw.rect(DISPLAYSURF, RED, player_rect)


# erases previous drawing of game
def draw_blank():
    pygame.draw.rect(DISPLAYSURF, BLACK,
                     (BARWIDTH, HEADERHEIGHT + BARWIDTH,
                      WINDOWWIDTH - BARWIDTH * 2,
                      WINDOWHEIGHT - HEADERHEIGHT - BARWIDTH))


def draw_bricks(is_brick):
    brick_rects = []
    for row in range(len(BRICKCOLORS)):
        brick_rects.append([])
        for col in range(ROWSIZE):
            brick_rect = pygame.Rect(BARWIDTH + col * BRICKWIDTH,
                                     BRICKCEILING + row * BRICKHEIGHT,
                                     BRICKWIDTH, BRICKHEIGHT)
            brick_rects[row].append(brick_rect)
            if is_brick[row][col]:
                pygame.draw.rect(DISPLAYSURF, BRICKCOLORS[row], brick_rect)
    return brick_rects


def draw_ball(ball_rect):
    pygame.draw.rect(DISPLAYSURF, RED, ball_rect)


if __name__ == '__main__':
    main()
