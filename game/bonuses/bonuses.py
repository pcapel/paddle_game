import pygame as pg

class Bonus():
    class Missile():
        pass
    class SidewinderMissile():
        pass
    class NuclearMissile():
        pass
    class TwoX():
        pass
    class ThreeX():
        pass
    class Slow():
        pass
    class Bomb():
        pass
    class SplashBomb():
        pass
    class StickyBomb():
        pass
    class ExtraBall():
        pass
    class TripleBall():
        pass
    class ExplosiveBall():
        pass
    class Drill():
        pass
    class ExpandPaddle():
        pass

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
