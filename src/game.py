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
    draw_borders()

    player_x = WINDOWWIDTH / 2
    player_y = WINDOWHEIGHT - 10
    # y-coord is fixed, player can only move along x-axis

    ball_x = WINDOWWIDTH / 2
    ball_y = BRICKCEILING + 200

    ball_velocity = [1, 1]

    bricks = [[True for _ in range(ROWSIZE)] for _ in BRICKCOLORS]

    while True:
        draw_blank()
        draw_bricks(bricks)
        draw_player(player_x, player_y)
        draw_ball(ball_x, ball_y)

        keys = pygame.key.get_pressed()
        if keys[K_a] or keys[K_LEFT]:
            player_x = max(BARWIDTH + PLAYERWIDTH / 2, player_x - PLAYERINC)
            # cannot go off left side of screen
        elif keys[K_d] or keys[K_RIGHT]:
            player_x = min(WINDOWWIDTH - BARWIDTH - PLAYERWIDTH / 2,
                          player_x + PLAYERINC)
            # cannot go off right side of screen

        # TODO: Implement collision detection
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
    pygame.draw.rect(DISPLAYSURF, GRAY, (0, HEADERHEIGHT,
                                         WINDOWWIDTH, BARWIDTH))
    pygame.draw.rect(DISPLAYSURF, GRAY, (0, HEADERHEIGHT, BARWIDTH, BARHEIGHT))
    pygame.draw.rect(DISPLAYSURF, GRAY, (WINDOWWIDTH - BARWIDTH, HEADERHEIGHT,
                                         BARWIDTH, BARHEIGHT))
    pygame.draw.rect(DISPLAYSURF, CYAN, (0, BARHEIGHT + HEADERHEIGHT,
                                         BARWIDTH, 20))
    pygame.draw.rect(DISPLAYSURF, RED,
                     (WINDOWWIDTH - BARWIDTH, BARHEIGHT + HEADERHEIGHT,
                      BARWIDTH, 20))


def draw_player(player_x, player_y):
    pygame.draw.rect(DISPLAYSURF, RED,
                     (player_x - PLAYERWIDTH / 2, player_y - PLAYERHEIGHT / 2,
                      PLAYERWIDTH, PLAYERHEIGHT))


# erases previous drawing of game
def draw_blank():
    pygame.draw.rect(DISPLAYSURF, BLACK,
                     (BARWIDTH, HEADERHEIGHT + BARWIDTH,
                      WINDOWWIDTH - BARWIDTH * 2,
                      WINDOWHEIGHT - HEADERHEIGHT - BARWIDTH))


def draw_bricks(bricks):
    for row in range(len(BRICKCOLORS)):
        for col in range(ROWSIZE):
            if bricks[row][col]:
                pygame.draw.rect(DISPLAYSURF, BRICKCOLORS[row],
                                 (BARWIDTH + col * BRICKWIDTH,
                                  BRICKCEILING + row * BRICKHEIGHT,
                                  BRICKWIDTH, BRICKHEIGHT))


def draw_ball(ball_x, ball_y):
    pygame.draw.rect(DISPLAYSURF, RED,
                     (ball_x - BALLWIDTH / 2, ball_y - BALLWIDTH / 2,
                      BALLWIDTH, BALLWIDTH))

if __name__ == '__main__':
    main()
