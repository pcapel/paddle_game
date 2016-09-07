import pygame as pg
import math

class Ball():
    """
    the ball class is the game ball, and will have methods associated with
    collision, such as tracking position and what type of surface it has collided
    with, as well as any relevant power up info
    """
    def __init__(self, state, screen, *args, **kwargs):
        #define initial vectors and position then pass to GameState
        self.screen = screen
        self.call_dict = {
        'up_pos_m': self.up_pos_m,
        'up_neg_m': self.up_neg_m,
        'down_pos_m': self.down_pos_m,
        'down_neg_m': self.down_neg_m
        }
        self.game_state = state
        self.x_pos = -5
        self.y_pos = -5
        self.speed = 5
        self.angle = 60
        self.is_launched = False

    #I need to add in the slope variability so that the ball
    #will travel at different angles
    #abstract collision_with into a method returns bool
    def travel(self, collision_with):
        prev = self.game_state.ball_travels['prev']
        left = (collision_with == 'right'
                or collision_with == 'block')
        right = (collision_with == 'left'
                or collision_with == 'block')
        down = (collision_with == 'top'
                or (collision_with == 'block' and prev == 'up_neg_m')
                or (collision_with == 'block' and prev == 'up_pos_m'))
        up = (collision_with == 'paddle'
             or (collision_with == 'block' and prev == 'down_pos_m')
             or (collision_with == 'block' and prev == 'down_neg_m'))
        killed = collision_with == 'dead'
        leftward = (prev == 'up_neg_m'
                    or prev == 'down_pos_m')
        rightward = (prev == 'up_pos_m'
                    or prev == 'down_neg_m')
        upward = (prev == 'up_pos_m'
                    or prev == 'up_neg_m')
        downward = (prev == 'down_neg_m'
                    or prev == 'down_pos_m')

        if up and rightward:
            self.up_pos_m()
            self.game_state.current_score += 1
        elif up and leftward:
            self.up_neg_m()
            self.game_state.current_score += 1
        elif down and rightward:
            self.down_neg_m()
        elif down and leftward:
            self.down_pos_m()
        elif right and upward:
            self.up_pos_m()
        elif right and downward:
            self.angle = -self.angle
            self.down_neg_m()
        elif left and upward:
            self.angle = -self.angle
            self.up_neg_m()
        elif left and downward:
            self.angle = -self.angle
            self.down_pos_m()
        elif killed:
            self.is_launched = False
            self.game_state.player_lives -= 1
        else:
            self.call_dict[prev]()
        return None

    def up_pos_m(self):
        self.x_pos += math.sin(self.angle) * self.speed
        self.y_pos += math.cos(self.angle) * self.speed
        self.game_state.ball_travels['prev'] = 'up_pos_m'
        return None

    def down_pos_m(self):
        self.x_pos -= math.sin(self.angle) * self.speed
        self.y_pos -= math.cos(self.angle) * self.speed
        self.game_state.ball_travels['prev'] = 'down_pos_m'
        return None

    def up_neg_m(self):
        self.x_pos -= math.sin(self.angle) * self.speed
        self.y_pos += math.cos(self.angle) * self.speed
        self.game_state.ball_travels['prev'] = 'up_neg_m'
        return None

    def down_neg_m(self):
        self.x_pos += math.sin(self.angle) * self.speed
        self.y_pos -= math.cos(self.angle) * self.speed
        self.game_state.ball_travels['prev'] = 'down_neg_m'
        return None

    def check_collision(self, ball, left, top, right, bottom, paddle, block):
        """
        everything except block is a rect instance
        block is the output from hit_block which is a bool
        """
        if ball.colliderect(left):
            return 'left'
        elif ball.colliderect(top):
            return 'top'
        elif ball.colliderect(right):
            return 'right'
        elif ball.colliderect(bottom):
            return 'dead'
        elif ball.colliderect(paddle):
            return 'paddle'
        elif block:
            return 'block'
        else:
            return None

    def hit_block(self, ball, block_dict):
        for key, rect in block_dict.iteritems():
            if ball.colliderect(rect):
                self.game_state.block_field[key][0].decrement_hp()
                self.game_state.current_score += self.game_state.block_field[key][0].get_score_per_strike()
                return True
            else:
                continue
        else:
            return False

    def check_lauch(self):
        return self.is_launched

    def launch(self):
        self.is_launched = True
        self.game_state.update('ball_travels', 'up_pos_m')
        return None

    def _draw(self, player_instance, radius=8, color=(255,255,255)):
        if not self.is_launched:
            start_from = player_instance.return_center()
            self.x_pos = start_from[0]
            self.y_pos = start_from[1]
            return pg.draw.circle(self.screen,
                color,
                player_instance.return_center(),
                radius)
        else:
            return pg.draw.circle(self.screen,
                color,
                (int(self.x_pos), int(self.y_pos)),
                radius)
