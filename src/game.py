import pygame, sys
from pygame.locals import *

WINDOWWIDTH = 960
WINDOWHEIGHT = 630

HEADERHEIGHT = 90

BARWIDTH = 40
BARHEIGHT = 520

FPS = 30

GRAY = (141, 139, 141)
RED  = (190,  82,  71)
CYAN = ( 57, 145, 133)

def main():
    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Breakout')
    draw_borders()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP
                                      and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def draw_borders():
    pygame.draw.rect(DISPLAYSURF, GRAY, (0, HEADERHEIGHT, WINDOWWIDTH, BARWIDTH))
    pygame.draw.rect(DISPLAYSURF, GRAY, (0, HEADERHEIGHT, BARWIDTH, BARHEIGHT))
    pygame.draw.rect(DISPLAYSURF, GRAY, (WINDOWWIDTH - BARWIDTH, HEADERHEIGHT, BARWIDTH, BARHEIGHT))
    pygame.draw.rect(DISPLAYSURF, CYAN, (0, BARHEIGHT + HEADERHEIGHT, BARWIDTH, 20))
    pygame.draw.rect(DISPLAYSURF, RED, (WINDOWWIDTH - BARWIDTH, BARHEIGHT + HEADERHEIGHT, BARWIDTH, 20))


if __name__ == '__main__':
    main()
