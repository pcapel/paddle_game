import pygame as pg
import sqlite3 as sq
#use sqlite db for save game data
#create classes and move this shit to OOP with a game loop

pg.init()

screen = pg.display.set_mode((600, 500))


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

strike_counter = 0

life_count = 3


def draw_player(paddle_width=75,
paddle_height=20,
flash=False, flash_color=(255,0,0)):

    return pg.draw.rect(screen,
            player_color,
            pg.Rect(player_x,
                player_y,
                paddle_width,
                paddle_height))

def draw_ball(size=15):
    return pg.draw.rect(screen,
            comp_color,
            pg.Rect(comp_x,
                comp_y,
                size,
                size))

while not done:
        for event in pg.event.get():
                if event.type == pg.QUIT:
                        done = True

        pressed = pg.key.get_pressed()
        print pressed

        if (pressed[pg.K_LEFT]
        and player_x > 0):
            player_x -= 5

        if (pressed[pg.K_RIGHT]
        and player_x < screen.get_width()
                    - player_paddle_width):
            player_x += 5



        screen.fill((0, 0, 0))
        p = draw_player()
        c = draw_ball()

        if p.colliderect(c):
            print "collide"

        # paddle_x_zone = (player_x + 1,
        #                 player_x + player_paddle_width + 1)
        #
        # comp_in_zone = (comp_x > paddle_x_zone[0]
        #                 and comp_x < paddle_x_zone[1])
        #
        # comp_in_contact = (comp_in_zone
        #                 and comp_y == screen.get_height()
        #                             - player_paddle_height
        #                             - comp_height)
        comp_below_contact = (comp_y > screen.get_height()
                                         - player_paddle_height
                                         - comp_height)
        #
        if p.colliderect(c) and comp_below_contact:
             y_dir = not y_dir
             x_dir = not x_dir
             strike_counter += 1
        elif p.colliderect(c) and not comp_below_contact:
            y_dir = not y_dir
        # elif (comp_in_zone
        # and comp_below_contact):
        #     x_dir = not x_dir

        score_text = font.render("Current Score: %d"%strike_counter,
                    True,
                    (0, 255,255))

        lives_text = font.render("Lives Remaining: %d"%life_count,
                    True,
                    (0,255,255))

        screen.blit(lives_text,
        (15, 15))
        screen.blit(score_text,
        (screen.get_width() - (score_text.get_width() + 15), 15))

        if (x_dir
        and y_dir):
            comp_x += 5
            comp_y += 5
        elif (not x_dir
        and not y_dir):
            comp_x -= 5
            comp_y -= 5
        elif (x_dir
        and not y_dir):
            comp_x += 5
            comp_y -= 5
        elif (not x_dir
        and y_dir):
            comp_x -= 5
            comp_y += 5

        if comp_x >= screen.get_width() - 15:
            x_dir = not x_dir
        elif comp_x <= 0:
            x_dir = not x_dir

        if comp_y >= screen.get_height() - 15:
            y_dir = not y_dir
        elif comp_y <= 0:
            y_dir = not y_dir

        pg.display.flip()
        clock.tick(60)


class Player(pg.draw):
    """
    the player class will represent the paddle that the player controls
    it will have methods associated with controlling power ups, actions,
    and the like
    """
    def __init__(self, *args, **kwargs):
        #define initial state and pass to GameState
        self.x_pos = None
        self.y_pos = None
        self.dir = None
        self.speed = None

    def add_aura(size=(20,20), color=(150,150,150), is_flash=False):
        """
        adds aura to player paddle, size is a tuple representing the (x,y) value
        of the rectangle that is used to draw the ellipse, probably use Rect.clamp()
        to keep it tied to player paddle
        """
        pass

    def move_right():
        self.x_pos += self.speed
        return None

    def move_left():
        self.x_pos -= self.speed
        return None

    def change_speed(value=5):
        pass

    def change_color(new_color=(0,155,155)):
        """
        change player color to passed value
        """
        pass

    def player_flash(color=None, period=1):
        """
        a method to make the player paddle flash certain colors based on
        in game criteria
        """
        pass

    def update_state(val_name=None, with_val=None):
        """
        use the GameState update method to update values in the game state
        """
        pass

    def _draw(paddle_width=75, paddle_height=20):

        return pg.draw.rect(screen,
                player_color,
                pg.Rect(player_x,
                    player_y,
                    paddle_width,
                    paddle_height))


class Ball(Player):
    """
    the ball class is the game ball, and will have methods associated with
    collision, such as tracking position and what type of surface it has collided
    with, as well as any relevant power up info
    """
    def __init__(self, *args, **kwargs):
        #define initial vectors and position then pass to GameState
        pass

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
        self.level_designs = {
        1: {
            'dimensions': (15, 15) #(x,y) block dimensions
            }
        }

        self.player_paddle_state = ['x', 'y']

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

    def update(var_name=None, with_val=None):
        """
        udates the passed var_name witht the value.
        should perform a type check on the value to ensure that correct
        update is performed, also, let's not break the game if it passes in
        nothing, eh?
        """
        pass

    def player_dir(paddle=1):
        """
        return the direction that the player is moving in
        uses player_paddle_state passed from player class
        """
        pass

    def ball_dir(ball=1):
        """
        returns the line that the ball is traveling on in the form of
        y = mx + b allowing projection of the x/y intercepts
        used for determining the slop modulation upon collision
        also useful for a faux AI like paddle.
        """
        pass

    def timer(start=1, end=5):
        """
        timer for various actions, power ups, etc
        defaults to 5 seconds, may not work right
        """
        pass
