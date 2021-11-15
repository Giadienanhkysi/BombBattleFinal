import pygame
import math
from flame import CenterFlame
from settings import Calculate
ASSETS = {  
    'bomb': [
      pygame.image.load('assets/bomb/bomb_{}.png'.format(i)) for i in range(1, 11)
    ],
    'bomb_chaining': pygame.image.load('assets/chaining_bomb.png'), 
    'bomb_explode_sound': pygame.mixer.Sound('assets/sound/explode.ogg')       
}

    
class Bomb:
    """Lop bom"""
    def __init__(self, x, y, placer, radius = 2, timer = 3):
        self.pos = (x, y)
        self.timer = timer
        self.placer = placer # biến lưu player
        self.radius = radius
        self.chaining = False
    
    def loop(self, lvl, time):
    # timer giảm dần 1 lượng bằng fps
    # time = Clock().get_time
        self.timer -= time
        if self.timer <=0:
            self.fire(lvl)

    def fire(self, lvl):   
        # hàm khai hỏa
        ASSETS['bomb_explode_sound'].play()     
        x, y = self.pos
        flame_list = lvl.flames
        flame = CenterFlame(lvl, x, y, flame_list, self.radius)
        flame_list.append(flame)
        lvl.bombs[self.pos] = None

        

    def collides(self, x, y):
        xl, xh, yl, yh = Calculate.list_colliding_coordinates(x, y)
        return xl <= self.pos[0] <= xh and yl <= self.pos[1] <= yh
    # kiểm tra xem có thể đi xuyên qua bomb hay không
    def collides_closer(self, x, y):
    # kiểm tra xem player đã đi ra khỏi khoảng cách cho phép hay chưa (nếu có thì không thể quay lại đi xuyên qua bom)
        return -0.45 <= x - self.pos[0] <= 0.45 and -0.45 <= y - self.pos[1] <= 0.45

    def draw(self, canvas):
        if self.chaining:
            # nếu 1 quả bom nổ thì quả bên cạnh nổ theo
            canvas.draw(ASSETS['bomb_chaining'], self.pos)
        else:
            # có 10 bức hình bom, nên ta sẽ cài cho current_frame sẽ chạy từ 0-10, ví dụ:
            # self.timer bắt đầu bằng 3 => curent_frame = (3-3)//0.3 = 0
            current_frame = int((3-self.timer)//0.3)          
            canvas.draw(ASSETS['bomb'][current_frame], self.pos)




