class Player(pg.Rect):
    """
    the player class will represent the paddle that the player controls
    it will have methods associated with controlling power ups, actions,
    and the like
    """
    def __init__(self, state, *args, **kwargs):
        self.game_state = state
        self.width = 120
        self.height = 20
        self.x_pos = 175
        self.y_pos = scrn_h - player_paddle_height
        self.center = ((self.x_pos + self.width / 2), self.y_pos)
        self.dir = None
        self.speed = 9
        self.color = (255, 30, 150)

    def add_aura(type='normal'):
        """
        I think that this can work as a decorator for the _draw function
        I'll have to figure out how I want to define the different types
        though.
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

    def _draw(self, width=None, height=None, color=None):
        if not color:
            color = self.color
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
