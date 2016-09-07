

class GameBlock(pg.Rect):
    def __init__(self, to_destroy, **kwargs):
        self.has_bonus()
        self.width = 40
        self.height = 20
        self.x_pos = 150
        self.y_pos = 150
        self.to_destroy = to_destroy
        self.color_sequence = []
        self.score_per_strike = 10
        self.score_for_destroy = to_destroy * 100
        self.possible_bonus = {
        'missile': 'single misile, causes 1 strike to 1 block',
        'sidewinder missile': 'single missile, causes 3 strikes to 1 block, splash 1 damage 1 block radius',
        'nuclear missile': 'single missile, causes 25 damage to 1 block, splash damage 10 block radius, diminishes accordingly',
        '2x score': 'duh',
        '3x score': 'duh',
        'slow ball': 'slows ball speed by 2',
        'splash bomb': 'explosive causes 3 damage to one square and 1 to surrounding',
        'extra ball': 'need to add an is_extra attr to ball class',
        'triple ball': 'splits ball mid air, need to tweek ball class further',
        'drill': ('causes strike damage to anything thing in its path for a total of 15 eg 1',
                'easy block followed by 4 mediums, it destroys them successively'),
        'sticky bomb': 'allows angular launch, bounces from wall, but sticks to blocks acts like splash bomb',
        'explosive ball': 'may take some tweeking',
        'paddle expand': 'should it be stackable?',

        }

    def has_bonus(self):
        """
        uses a random number to return a bonus type.
        used to determine if a block in build_field will have a bonus.
        returns a bonus type as string, eg 'rockets', or False
        """
        pass

    def set_colors(self, red_mod=255, grn_mod=255, blu_mod=255):
        for num in range(1, self.to_destroy + 1):
            self.color_sequence.append( (15 + (num * (red_mod / self.to_destroy)),
            15 + (num * (grn_mod / self.to_destroy)),
            15 + (num * (blu_mod / self.to_destroy))))

    def get_hp(self):
        return self.to_destroy

    def get_score_for_destroy(self):
        return self.score_for_destroy

    def get_score_per_strike(self):
        return self.score_per_strike

    def decrement_hp(self):
        self.to_destroy -= 1
        return None

    def set_x_pos(self, pos):
        self.x_pos = pos
        return None

    def set_y_pos(self, pos):
        self.y_pos = pos
        return None

    def _draw(self):
        color_index = self.to_destroy - 1
        if color_index >= 0:
            color = self.color_sequence[color_index]
        return pg.draw.rect(screen,
                color,
                pg.Rect(self.x_pos,
                    self.y_pos,
                    self.width,
                    self.height), 2)

    class EasyBlock(GameBlock):
        def __init__(self, *args, **kwargs):
            GameBlock.__init__(self, 1)
            self.set_colors(0, 0, 240)

    class MediumBlock(GameBlock):
        def __init__(self, *args, **kwargs):
            GameBlock.__init__(self, 3)
            self.set_colors(150, 0, 240)

    class HardBlock(GameBlock):
        def __init__(self, *args, **kwargs):
            GameBlock.__init__(self, 5)
            self.set_colors(200, 0, 150)

    class InsaneBlock(GameBlock):
        def __init__(self, *args, **kwargs):
            GameBlock.__init__(self, 10)
            self.set_colors(200, 0, 100)

    class DemonBlock(GameBlock):
        def __init__(self, *args, **kwargs):
            GameBlock.__init__(self, 20)
            self.set_colors(240, 50, 50)
