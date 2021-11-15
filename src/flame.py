import pygame
from blocks import Block
ASSETS = {    
    'flame_center': [
      pygame.image.load('assets/explosion/explosion_center_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_right': [
      pygame.image.load('assets/explosion/explosion_right_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_left': [
      pygame.image.load('assets/explosion/explosion_left_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_up': [
      pygame.image.load('assets/explosion/explosion_up_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_down': [
      pygame.image.load('assets/explosion/explosion_down_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_right_end': [
      pygame.image.load('assets/explosion/explosion_right_end_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_left_end': [
      pygame.image.load('assets/explosion/explosion_left_end_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_up_end': [
      pygame.image.load('assets/explosion/explosion_up_end_{}.png'.format(i)) for i in range(1, 4)
    ],
    'flame_down_end': [
      pygame.image.load('assets/explosion/explosion_down_end_{}.png'.format(i)) for i in range(1, 4)
    ],

}
class Flame:
    def __init__(self, lvl, x, y, timer = 0.5):
        self.pos = (x, y)
        self.timer = timer
        self.can_spread = not self.affect_environment(lvl)

        if lvl.bombs.get(self.pos) != None: #vi tri flame trung voi bom chua no
            bomb = lvl.bombs[self.pos]
            bomb.chaining = True
            if bomb.timer > 0.25:
                bomb.timer = 0.25


    def affect_environment(self, lvl):
        '''tác động đến môi trường xung quanh'''
        x, y = self.pos
        matrix = lvl.matrix.matrix
        if not(0 <= x <= len(matrix[0]) and 0<= y <= len(matrix)):
            return False
        block = lvl.matrix.explode_block(x, y)

        return block in [
            Block.BOX, Block.BOX_GOAL, Block.BOX_POWERUP_BOMBUP, Block.BOX_POWERUP_BLAST, Block.BOX_POWERUP_LIFE,
            Block.WALL
        ]

    def loop(self, lvl, time):
        self.timer -= time
        if self.timer <= 0:
            lvl.flames.remove(self)

    def collides(self, x, y):
        # kiểm tra va chạm 
        # chạm tính bắt đầu từ viền
        return - 0.6 <= x - self.pos[0] <= 0.6 and - 0.6 <= y - self.pos[1]<= 0.6            
    # astract
    def draw(self, canvas):
        pass
        

class CenterFlame(Flame):
    def __init__(self, lvl, x, y, flame_list, radius, timer = 0.5):        
        super().__init__(lvl, x, y, timer)
        
        if radius > 1 and self.can_spread:
            l = HorizontalFlame(lvl, x-1, y, flame_list, radius-1, timer, False)
            r = HorizontalFlame(lvl, x+1, y, flame_list, radius-1, timer, True)
            u = VerticalFlame(lvl, x, y-1, flame_list, radius-1, timer, False)
            d = VerticalFlame(lvl, x, y+1, flame_list, radius-1, timer, True)
            new_flame = [l, r, u, d] #list luu ngon lua xung quanh
            flame_list += [f for f in new_flame if f.can_spread] #neu lua khong cham tuong thi lan rong ra

    def draw(self, canvas):
        current_frame = self.timer//0.1
        # in ảnh theo thứ tự 0 1 2 1 0 
        if current_frame > 2:
            current_frame = 4 - current_frame
        current_frame = int(current_frame)
        canvas.draw(ASSETS['flame_center'][current_frame], self.pos)


class VerticalFlame(Flame):
    def __init__(self, lvl, x, y, flame_list, radius, timer, up_to_down):
        super().__init__(lvl, x, y, timer)
        self.up_to_down = up_to_down
        self.radius = radius

        if radius > 1 and self.can_spread:
            if up_to_down:
                ny = y + 1
            else:
                ny = y - 1      
            # mỗi  lần in ra 1 flame thì giảm biến radius 1
            flame = VerticalFlame(lvl, x, ny, flame_list, radius - 1, timer, up_to_down)
            if flame.can_spread:
                flame_list.append(flame)
    def draw(self, canvas):
        if self.radius == 1:
            flame = 'flame_down_end' if self.up_to_down else 'flame_up_end'
        else:
            flame = 'flame_down' if self.up_to_down else 'flame_up'

        current_frame = self.timer//0.1
        if current_frame > 2:
            current_frame = 4- current_frame
        current_frame = int(current_frame)
        canvas.draw(ASSETS[flame][current_frame], self.pos)


class HorizontalFlame(Flame):
    def __init__(self, lvl, x, y, flames_list, radius, timer, left_to_right):
        super().__init__(lvl, x, y, timer)
        self.radius = radius 
        self.left_to_right = left_to_right

        if radius > 1 and self.can_spread:
            if self.left_to_right:
                nx = x+1
            else:
                nx = x-1
            flame = HorizontalFlame(lvl, nx, y, flames_list, radius-1, timer, left_to_right)
            if flame.can_spread:
                flames_list.append(flame)

    def draw(self, canvas):
        if self.radius == 1:
            flame = 'flame_right_end' if self.left_to_right else 'flame_left_end'
        else:
            flame = 'flame_right' if self.left_to_right else 'flame_left'

        current_frame = self.timer//0.1
        if current_frame > 2:
            current_frame = 4-current_frame
        current_frame = int(current_frame)
        canvas.draw(ASSETS[flame][current_frame], self.pos)
            
