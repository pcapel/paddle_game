class GameState():
    def __init__(self, level=1, *args, **kwargs):
        self.player_lives = 3
        self.current_score = 0
        self.level = level
        #this is silly, these are probably going to work best as classes
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
