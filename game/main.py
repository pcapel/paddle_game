import pygame as pg
import math
import random
import sqlite3 as sq
#use sqlite db for save game data

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

class GameState():
    def __init__(self, level=1, *args, **kwargs):
        self.player_lives = 3
        self.current_score = 0
        self.level = level
        self.level_designs = {
        1: {
            'dimensions': (10, 4), #(x,y) block dimensions
            'upper left': ((scrn_w-500)/2, scrn_h/2),
            'block type': EasyBlock,
            },
        2: {
            'dimensions': (10, 5),
            'upper left': (scrn_w/2, scrn_h/2),
            'block type': MediumBlock,
        }
        }

        self.block_field = {}

        self.block_dict = {}

        for row in xrange(1, self.level_designs[level]['dimensions'][1]+1):
            for col in xrange(1, self.level_designs[level]['dimensions'][0]+1):
                self.block_field['row%dcol%d'%(row,col)] = (self.level_designs[level]['block type'](), (row, col))
        self.draw_field()


        self.player_paddle_state = ['prev_x', 'current_x']
        self.ball_travels = {'prev': 'up_pos_m'}

    def draw_field(self):
        self.clear_dead()
        top_corner = self.level_designs[self.level]['upper left']
        row_offset = 20
        col_offset = 40
        for key, tup in self.block_field.iteritems():
            rect = tup[0]
            row = tup[1][0]
            col = tup[1][1]
            rect.set_x_pos((col_offset * col) + top_corner[0])
            rect.set_y_pos((row_offset * row) + top_corner[1])
            self.block_dict[key] = rect._draw()
        return None

    def clear_dead(self):
        for key in self.block_field.keys():
            rect = self.block_field[key][0]
            if rect.get_hp() <= 0:
                self.current_score += rect.get_score_for_destroy()
                del self.block_field[key]
                del self.block_dict[key]
            else:
                continue
        return None

    def get_score(self):
        return self.current_score

    def get_lives(self):
        return self.player_lives

    def get_field(self):
        return self.block_field

    def get_blocks(self):
        return self.block_dict

    def update(self, var_name=None, with_val=None):
        #this really just overrides shit and could be used to
        #create any variable I wanted soooo
        #it's probably not good
        #but it works...
        self.var_name = with_val
        return None

    def player_dir(paddle=1):
        """
        return the direction that the player is moving in
        uses player_paddle_state passed from player class
        """
        prev = self.player_paddle_state[0]
        cur = self.player_paddle_state[1]
        dir_right = cur - prev > 0
        dir_left = cur - prev < 0
        if dir_left:
            return 'left'
        elif dir_right:
            return 'right'
        else:
            return 'stationary'

    def ball_dir(self, ball=1):
        """
        returns ball direction in the form of the string of the method name
        that was called to move it eg up_neg_m (upward motion, negative slope)
        the names descripe the characteristics of the line the ball travels
        """
        return self.ball_travels['prev']

    def right_edge(self):
        return pg.draw.rect(screen,
                (0,0,0),
                pg.Rect(scrn_w - 1,
                    0,
                    1,
                    scrn_h))

    def left_edge(self):
        return pg.draw.rect(screen,
                (0,0,0),
                pg.Rect(-4,
                    0,
                    5,
                    scrn_h))

    def top_edge(self):
        return pg.draw.rect(screen,
                (0,0,0),
                pg.Rect(0,
                    -4,
                    scrn_w,
                    5))

    def deathzone(self):
        return pg.draw.rect(screen,
                (0,0,0),
                pg.Rect(0,
                    scrn_h - 1,
                    scrn_w,
                    5))

    def timer(start=1, end=5):
        """
        timer for various actions, power ups, etc
        defaults to 5 seconds, may not work right
        """
        pass



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
