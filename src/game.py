import pygame
import sys
import random
import time

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
    score = 0

    fontObj = pygame.font.Font('freesansbold.ttf', 50)
    while True:
        draw_blank()
        brick_rects = draw_bricks(is_brick)
        draw_player(player.rect)
        draw_ball(ball.rect)

        textSurfaceObj = fontObj.render(' %03d ' % score, True, GRAY, BLACK)
        textRectObj = textSurfaceObj.get_rect()
        textRectObj.center = (480, 45)
        DISPLAYSURF.blit(textSurfaceObj, textRectObj)

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP
                                      and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        check_border_collisions(ball, player, border_rects)
        old_brick = check_brick_collisions(ball, brick_rects, is_brick)

        for row in range(len(brick_rects)):
            for col in range(len(brick_rects[0])):
                if brick_rects[row][col] == old_brick:
                    score += 1
                    is_brick[row][col] = False
                    break

        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            player.move_left(BARWIDTH)
        elif keys[K_d] or keys[K_RIGHT]:
            player.move_right(BARWIDTH, WINDOWWIDTH)

        ball.update_ball_pos(ball.x_velocity, ball.y_velocity)

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


def check_border_collisions(ball, player, border_rects):
    if ball.rect.colliderect(player.rect):
        ball.apply_collision([player.rect])
    elif ball.rect.colliderect(border_rects[0]):
        ball.reflect_y_velocity()
    elif ball.rect.colliderect(border_rects[1]):
        ball.reflect_x_velocity()
        ball.update_ball_pos(5, 0)
    elif ball.rect.colliderect(border_rects[2]):
        ball.reflect_x_velocity()
        ball.update_ball_pos(-5, 0)


def check_brick_collisions(ball, brick_rects, is_brick):
    collided_bricks = []
    for row in range(len(brick_rects)):
        for col in range(len(brick_rects[0])):
            if (ball.rect.colliderect(brick_rects[row][col]) and
                    is_brick[row][col]):
                collided_bricks.append(brick_rects[row][col])
    if not collided_bricks:
        return
    ball.apply_collision(collided_bricks)
    return random.choice(collided_bricks)


if __name__ == '__main__':
    main()
