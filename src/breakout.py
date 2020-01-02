import pygame
import time
import os
import neat
import numpy as np

from src.player import Player
from src.ball import Ball
from src.game import Game
from src.constants import *
from pygame.locals import *


def main(genomes, config):
    nets = []
    ge = []
    games = []
    i = 0
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        games.append(Game())
        g.fitness = 0
        ge.append(g)
        i += 1

    global FPSCLOCK, DISPLAYSURF
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

    pygame.display.set_caption('Breakout')
    start_time = pygame.time.get_ticks()

    while games:
        new_time = (pygame.time.get_ticks() - start_time) / 1000

        draw_blank()
        border_rects = draw_borders()

        games[0].draw_scoreboard(new_time, DISPLAYSURF)
        brick_rects = games[0].draw_bricks(DISPLAYSURF)
        for game in games:
            game.draw_player(DISPLAYSURF)
            game.draw_ball(DISPLAYSURF)

        # Collision detection
        for x, game in enumerate(games):
            if new_time > 100:
                games.pop(x)
                nets.pop(x)
                ge.pop(x)
                continue
            game.check_border_collisions(border_rects)
            old_brick = game.check_brick_collisions(brick_rects)
            if old_brick:
                for row in range(len(brick_rects)):
                    for col in range(len(brick_rects[0])):
                        if brick_rects[row][col] == old_brick:
                            game.score += 1
                            ge[x].fitness += 1
                            game.is_brick[row][col] = False
                            continue
            game.ball.update_ball_pos(game.ball.x_velocity,
                                      game.ball.y_velocity)

            # Lost a life
            if game.ball.y > WINDOWHEIGHT + game.ball.width:
                if game.lives == 0:
                    ge[x].fitness -= 1
                    games.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    continue

                time.sleep(1)
                game.ball = Ball(WINDOWWIDTH / 2, BRICKCEILING + 200, 1.0)
                game.lives -= 1

            output = nets[x].activate((game.player.x, game.ball.y, game.ball.x,
                                       bricks_product(game.is_brick)))
            if output[0] > 0.5:
                game.player.move_right(BARWIDTH, WINDOWWIDTH)
            if output[1] > 0.5:
                game.player.move_left(BARWIDTH)

            if game.is_win():
                if game.level == 1:
                    ge[x].fitness += 100 - new_time
                    games.pop(x)
                    nets.pop(x)
                    ge.pop(x)
                    continue
                # reset whole game
                time.sleep(1)
                game.ball = Ball(WINDOWWIDTH / 2, BRICKCEILING + 200, 1.0)
                game.player = Player(WINDOWWIDTH / 2, WINDOWHEIGHT - 10)
                game.is_brick = [[True for _ in range(ROWSIZE)]
                                 for _ in BRICKCOLORS]
                game.level += 1

        pygame.display.update()
        FPSCLOCK.tick(FPS)
    pygame.quit()


def bricks_product(is_brick):
    flat = [b for brick in is_brick for b in brick]
    temp = [brick * prime for brick, prime in zip(flat, PRIMES)]
    temp = [a for a in temp if a != 0]
    return np.prod(np.array(temp))


# erases previous drawing of game
def draw_blank():
    pygame.draw.rect(DISPLAYSURF, BLACK,
                     (BARWIDTH, HEADERHEIGHT + BARWIDTH,
                      WINDOWWIDTH - BARWIDTH * 2,
                      WINDOWHEIGHT - HEADERHEIGHT - BARWIDTH))


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


def run(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                                neat.DefaultSpeciesSet, neat.DefaultStagnation,
                                config_path)
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main, 5000)


if __name__ == '__main__':
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    run(config_path)
