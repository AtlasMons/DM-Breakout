import pygame, sys
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

# TODO: Possibly want to add acceleration to player's movement
PLAYERWIDTH = 100
PLAYERHEIGHT = 15
PLAYERINC = 10
# how many pixels the player moves with each input

BALLWIDTH = 10

FPS = 60

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

    player_x = WINDOWWIDTH / 2
    player_y = WINDOWHEIGHT - 10
    # y-coord is fixed, player can only move along x-axis

    ball_x = WINDOWWIDTH / 2
    ball_y = BRICKCEILING + 200

    ball_velocity = [4, 4]

    is_brick = [[True for _ in range(ROWSIZE)] for _ in BRICKCOLORS]

    while True:
        draw_blank()
        brick_rects = draw_bricks(is_brick)

        player_rect = pygame.Rect(player_x - PLAYERWIDTH / 2,
                                 player_y - PLAYERHEIGHT / 2,
                                 PLAYERWIDTH, PLAYERHEIGHT)
        draw_player(player_rect)

        ball_rect = pygame.Rect(ball_x - BALLWIDTH / 2, ball_y - BALLWIDTH / 2,
                      BALLWIDTH, BALLWIDTH)
        draw_ball(ball_rect)

        if ball_rect.colliderect(player_rect) or \
                ball_rect.colliderect(border_rects[0]):
            ball_velocity[1] *= -1
        elif ball_rect.collidelist(border_rects[1:3]) != -1:
            ball_velocity[0] *= -1

        for row in range(len(brick_rects)):
            collision = ball_rect.collidelist(brick_rects[row])
            if collision != -1 and is_brick[row][collision]:
                brick = brick_rects[row][collision]
                if abs(ball_x - brick.left) < 5 or abs(ball_x - brick.right) < 4:
                    ball_velocity[0] *= -1
                    is_brick[row][collision] = False
                if abs(ball_y - brick.top) < 5 or abs(ball_y - brick.bottom) < 4:
                    ball_velocity[1] *= -1
                    is_brick[row][collision] = False


        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            player_x = max(BARWIDTH + PLAYERWIDTH / 2, player_x - PLAYERINC)
            # cannot go off left side of screen
        elif keys[K_d] or keys[K_RIGHT]:
            player_x = min(WINDOWWIDTH - BARWIDTH - PLAYERWIDTH / 2,
                          player_x + PLAYERINC)
            # cannot go off right side of screen

        ball_x += ball_velocity[0]
        ball_y += ball_velocity[1]

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP
                                      and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

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
