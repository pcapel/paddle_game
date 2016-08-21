import pygame as pg
import sqlite3 as sq
#use sqlite db for save game data
#create classes and move this shit to OOP with a game loop

pg.init()

screen = pg.display.set_mode((800, 700))
scrn_h = screen.get_height()
scrn_w = screen.get_width()

class GameState():
    """
    the game state class is a modelling class that tracks all the changes to the
    state of the game and will be initialized according to level vars to allow
    for many levels.
    perhaps it will track whether you're in menu, paused, or dead as well
    yeah, that seems smart
    """
    def __init__(self, *args, **kwargs):
        #init will have all the inital positions and vectors for things
        self.player_lives = 3
        self.current_score = 0
        self.level_designs = {
        1: {
            'dimensions': (15, 15) #(x,y) block dimensions
            }
        }

        self.player_paddle_state = ['prev_x', 'current_x']
        self.ball_travels = {'prev': 'up_pos_m'}

    def build_field(level=1):
        """
        this'll be a doozy, based on level, read out from field design dict
        and initialize all the blocks in the field with randomized chances for
        drops.
        """
        pass

    def has_bonus():
        """
        uses a random number to return a bonus type.
        used to determine if a block in build_field will have a bonus.
        returns a bonus type as string, eg 'rockets', or False
        """
        pass

    def get_score(self):
        return self.current_score

    def get_lives(self):
        return self.player_lives

    def update(self, var_name=None, with_val=None):
        """
        udates the passed var_name witht the value.
        should perform a type check on the value to ensure that correct
        update is performed, also, let's not break the game if it passes in
        nothing, eh?
        """
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
        returns the line that the ball is traveling on in the form of
        y = mx + b allowing projection of the x/y intercepts
        used for determining the slop modulation upon collision
        also useful for a faux AI like paddle.
        """
        return self.ball_travels

    def right_edge(self):
        return pg.draw.rect(screen,
                (0,0,255),
                pg.Rect(scrn_w - 1,
                    0,
                    1,
                    scrn_h))

    def left_edge(self):
        return pg.draw.rect(screen,
                (0,0,255),
                pg.Rect(-4,
                    0,
                    5,
                    scrn_h))

    def top_edge(self):
        return pg.draw.rect(screen,
                (0,0,255),
                pg.Rect(0,
                    -4,
                    scrn_w,
                    5))

    def deathzone(self):
        return pg.draw.rect(screen,
                (0,0,255),
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


class Player(pg.Rect):
    """
    the player class will represent the paddle that the player controls
    it will have methods associated with controlling power ups, actions,
    and the like
    """
    def __init__(self, state, *args, **kwargs):
        #define initial state and pass to GameState
        self.game_state = state
        self.width = 75
        self.height = 20
        self.x_pos = 175
        self.y_pos = scrn_h - player_paddle_height
        self.center = ((self.x_pos + self.width / 2), self.y_pos)
        self.dir = None
        self.speed = 5

    def add_aura(size=(20,20), color=(150,150,150), is_flash=False):
        """
        adds aura to player paddle, size is a tuple representing the (x,y) value
        of the rectangle that is used to draw the ellipse, probably use Rect.clamp()
        to keep it tied to player paddle
        """
        pass

    def move_right(self):
        self.x_pos += self.speed
        self.center = ((self.x_pos + self.width / 2), self.y_pos)
        return None

    def move_left(self):
        self.x_pos -= self.speed
        self.center = ((self.x_pos + self.width / 2), self.y_pos)
        return None

    def change_speed(self, value=5):
        pass

    def change_color(self, new_color=(0,155,155)):
        """
        change player color to passed value
        """
        pass

    def player_flash(self, color=None, period=1):
        """
        a method to make the player paddle flash certain colors based on
        in game criteria
        """
        pass

    def update_state(self, val_name=None, with_val=None):
        """
        use the GameState update method to update values in the game state
        """
        pass

    def get_x(self):
        return self.x_pos

    def return_center(self):
        return self.center

    def _draw(self, width=None, height=None, color=(0,255,0)):
        if not width:
            width = self.width
        if not height:
            height = self.height

        return pg.draw.rect(screen,
                color,
                pg.Rect(self.x_pos,
                    self.y_pos,
                    width,
                    height))

class Ball(Player):
    """
    the ball class is the game ball, and will have methods associated with
    collision, such as tracking position and what type of surface it has collided
    with, as well as any relevant power up info
    """
    def __init__(self, state, *args, **kwargs):
        #define initial vectors and position then pass to GameState
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
        self.is_launched = False

    def travel(self, collision_with):
        down = collision_with == 'top'
        left = collision_with == 'right'
        right = collision_with == 'left'
        up = collision_with == 'paddle'
        killed = collision_with == 'dead'
        prev = self.game_state.ball_travels['prev']
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
        elif up and leftward:
            self.up_neg_m()
        elif down and rightward:
            self.down_neg_m()
        elif down and leftward:
            self.down_pos_m()
        elif right and upward:
            self.up_pos_m()
        elif right and downward:
            self.down_neg_m()
        elif left and upward:
            self.up_neg_m()
        elif left and downward:
            self.down_pos_m()
        elif killed:
            self.is_launched = False
            self.game_state.player_lives -= 1
        else:
            self.call_dict[prev]()
        return None

    def up_pos_m(self):
        self.x_pos += self.speed
        self.y_pos -= self.speed
        self.game_state.ball_travels['prev'] = 'up_pos_m'
        return None

    def down_pos_m(self):
        self.x_pos -= self.speed
        self.y_pos += self.speed
        self.game_state.ball_travels['prev'] = 'down_pos_m'
        return None

    def up_neg_m(self):
        self.x_pos -= self.speed
        self.y_pos -= self.speed
        self.game_state.ball_travels['prev'] = 'up_neg_m'
        return None

    def down_neg_m(self):
        self.x_pos += self.speed
        self.y_pos += self.speed
        self.game_state.ball_travels['prev'] = 'down_neg_m'
        return None

    def check_collision(self, ball, left, top, right, bottom, paddle):
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
        else:
            return None

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
            return pg.draw.circle(screen,
                color,
                player_instance.return_center(),
                radius)
        else:
            return pg.draw.circle(screen,
                color,
                (self.x_pos, self.y_pos),
                radius)

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
        paddle = _player._draw()
        ball = _ball._draw(_player)
        death = _state.deathzone()
        right = _state.right_edge()
        left = _state.left_edge()
        top = _state.top_edge()
        if _ball.check_lauch():
            _ball.travel(_ball.check_collision(ball, left, top, right, death, paddle))

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
