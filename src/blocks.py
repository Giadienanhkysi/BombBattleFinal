from enum import Enum
import pygame
import math
pygame.init()
ASSETS = {
    'grass': pygame.image.load('assets/grass.png'),
    'wall': pygame.image.load('assets/wall.png'),    
    'box': pygame.image.load('assets/box.png'),
    'goal_close': pygame.image.load('assets/goal_closed.png'),
    'goal_open': pygame.image.load('assets/goal_open.png'),
    'powerup_life': pygame.image.load('assets/powerup_life.png'),
    'goal_opening': [
        pygame.image.load('assets/goal_opening/goal_opening_{}.png'.format(i)) for i in range(1, 6)
    ],
    'powerup_blast': pygame.image.load('assets/powerup_blast.png'),
    'powerup_bombup': pygame.image.load('assets/powerup_bombup.png'),            
}
class Block(Enum):    
    """Lop ke thua tu enum dung de tao cac doi tuong khoi trong map"""
    GRASS = 0
    WALL = 1
    BOX = 2

    BOX_GOAL = 3
    GOAL_OPEN = 4    
    GOAL_CLOSE = 5

    BOX_POWERUP_LIFE = 6
    POWERUP_LIFE = 7

    BOX_POWERUP_BLAST = 8
    POWERUP_BLAST = 9
    
    BOX_POWERUP_BOMBUP = 10
    POWERUP_BOMBUP = 11

        
    def draw(self, canvas, x, y):
        """ham nay dung de ve cac khoi ra man hinh"""
        assets_indexes = {            
            Block.GRASS: 'grass',
            Block.WALL : 'wall',
            Block.BOX: 'box',
            Block.BOX_GOAL: 'box',
            Block.GOAL_OPEN: 'goal_open',
            Block.GOAL_CLOSE: 'goal_close',
            Block.BOX_POWERUP_LIFE : 'box',
            Block.POWERUP_LIFE: 'powerup_life',
            Block.BOX_POWERUP_BLAST : 'box',
            Block.POWERUP_BLAST: 'powerup_blast',
            Block.BOX_POWERUP_BOMBUP : 'box',
            Block.POWERUP_BOMBUP: 'powerup_bombup'
        }
        
        img = ASSETS[assets_indexes[self]]
        #ve grass lam nen cho cac powerup, neu khong ve nen map se bi "thung"
        if self in [Block.POWERUP_LIFE, Block.POWERUP_BLAST, Block.POWERUP_BOMBUP]:
            canvas.draw(ASSETS['grass'], (x,y))
        # ve
        canvas.draw(img, (x, y))
        

