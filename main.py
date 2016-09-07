import pygame as pg
import math
import random
import sqlite3 as sq
#use sqlite db for save game data

from game.state import GameState as gs
from game.player import Player as p
from game.balls import Ball as b
from game.levels import Levels as Lvl
from game.blocks import GameBlock as gb

implementaion_ideas = """
fix the ball bounce glitches.

change the edges to be the actual screen edges

have the arrow keys bind to a launch direction arrow when you hold space bar to launch
the ball initially, this can also be used for missiles and such.

add intertial movement to the paddle to affect the feel of motion
"""

pg.init()

screen = pg.display.set_mode((800, 600))
scrn_h = screen.get_height()
scrn_w = screen.get_width()

done = False

player_color = (150, 0, 150)
comp_color = (255, 255, 255)

player_paddle_width = 75
player_paddle_height = 20
player_x = 175
player_y = screen.get_height() - player_paddle_height

comp_width = 15
comp_height = 15
comp_x = 150
comp_y = 150

clock = pg.time.Clock()

x_dir = True
y_dir = True

font = pg.font.Font(None, 25)

_state = GameState()
_player = Player(_state)
_ball = Ball(_state)
_block = DemonBlock()

#game loop
while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        done = True

        pressed = pg.key.get_pressed()

        if (pressed[pg.K_LEFT]
        and _player.get_x() > 0):
            _player.move_left()

        if (pressed[pg.K_RIGHT]
        and _player.get_x() < screen.get_width()
                    - player_paddle_width):
            _player.move_right()

        if (pressed[pg.K_SPACE]):
            _ball.launch()

        screen.fill((0, 0, 0))
        _state.draw_field()
        paddle = _player._draw()
        ball = _ball._draw(_player)
        death = _state.deathzone()
        right = _state.right_edge()
        left = _state.left_edge()
        top = _state.top_edge()
        if _ball.check_lauch():
            _ball.travel(_ball.check_collision(ball,
            left, top, right, death,
            paddle,
            _ball.hit_block(ball, _state.get_blocks())))





        score_text = font.render("Current Score: %d"%_state.get_score(),
                    True,
                    (0, 255,255))

        lives_text = font.render("Lives Remaining: %d"%_state.get_lives(),
                    True,
                    (0,255,255))

        screen.blit(lives_text,
        (15, 15))
        screen.blit(score_text,
        (screen.get_width() - (score_text.get_width() + 15), 15))

        pg.display.flip()
        clock.tick(60)
