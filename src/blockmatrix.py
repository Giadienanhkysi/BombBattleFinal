# from settings import*
import pygame
from blocks import Block
from settings import Calculate
ASSETS = {  
    'goal_opening': [
        pygame.image.load('assets/goal_opening/goal_opening_{}.png'.format(i)) for i in range(1, 6)
    ],    
    'exploding_box': [
      pygame.image.load('assets/exploding_box/exploding_box_{}.png'.format(i)) for i in range(1, 7)],
    'power_up_sound': pygame.mixer.Sound('assets/sound/power_up_sound.ogg')
}

class BlockMatrix():
    """Lop nay dung de tạo map va xu ly map"""
    def __init__(self, matrix = None):
        self.exploding = [] # list lưu vị trí và thời gian nổ của box
        self.matrix = matrix
        self.goal_open = False
        self.door_opening = None  #List lưu vị trí cửa và thời gian mở cửa      

    def is_goal(self, x, y):
        # kiểm tra xem ô này có phải cổng hay không
        return self.matrix[y][x] == Block.GOAL_OPEN


    def is_solid(self, x, y):
        # kiểm tra xem ô này có phải vật cản hay không
        return self.matrix[y][x] in [
          Block.WALL, Block.BOX, Block.BOX_GOAL, Block.BOX_POWERUP_BLAST, 
          Block.BOX_POWERUP_BOMBUP, Block.BOX_POWERUP_LIFE
        ]

    def open_door(self):
        self.goal_open = True  
        # tìm trong ma trận xem ô nào là cổng, nếu là cổng thì thực hiện mở cổng
        for y, row in enumerate(self.matrix):
            for x, cell in enumerate(row):                
                if cell == Block.GOAL_CLOSE:          
                    self.door_opening = [(x, y), 0.5]# 0.5 là tổng thời gian để  chạy hết 5 khung hinh
                    self.matrix[y][x] = Block.GOAL_OPEN
                    return
                        

    def draw(self, canvas):
        # vẽ từng khối trong map
        for i, row in enumerate(self.matrix):
            for j, block in enumerate(row):
                block.draw(canvas, j, i)
        # open door
        if self.door_opening != None:
            pos, timer = self.door_opening
        # vẽ từng khung hình một
            current_frame = int(timer//0.1)#tổng thời gian chạy/thời gian chay 1 khung hinh           
            current_frame = ASSETS['goal_opening'][current_frame]
            # gọi hàm vẽ của lớp đồ họa
            canvas.draw(current_frame, pos)
        #vẽ hộp nổ
        for x, y, e_time in self.exploding:
            current_frame = int((0.3 - e_time)//0.06)
            current_frame = ASSETS['exploding_box'][current_frame]
            canvas.draw(current_frame, (x, y))
    
    def loop(self, time):
        # hàm này giảm thời gian 1 lượng fps dần về 0
        if self.door_opening != None:
            self.door_opening[1] -= time
            if self.door_opening[1] <=0:
                self.door_opening = None
        for i, (x, y, e_time) in enumerate(self.exploding):
            e_time -= time
            if e_time <= 0:
                del self.exploding[i]
                # nổ xong xóa ra khỏi list
                continue
            self.exploding[i] = (x, y, e_time)

    def explode_block(self, x, y):
        block = self.matrix[y][x]
        
        if block in [Block.POWERUP_BOMBUP, Block.BOX_POWERUP_BLAST, Block.POWERUP_LIFE]:
            self.matrix[y][x] = Block.GRASS
        elif block == Block.BOX:            
            self.exploding.append((x, y, 0.3))
            self.matrix[y][x] = Block.GRASS
        elif block == block.BOX_GOAL:
            self.exploding.append((x, y, 0.3))
            if self.goal_open:
                self.matrix[y][x] = Block.GOAL_OPEN
            else:
                self.matrix[y][x] = Block.GOAL_CLOSE
        elif block == Block.BOX_POWERUP_BLAST:
            self.exploding.append((x, y, 0.3))
            self.matrix[y][x] = Block.POWERUP_BLAST
        elif block == Block.BOX_POWERUP_BOMBUP:
            self.exploding.append((x, y, 0.3))
            self.matrix[y][x] = Block.POWERUP_BOMBUP
        elif block == Block.BOX_POWERUP_LIFE:
            self.exploding.append((x, y, 0.3))
            self.matrix[y][x] = Block.POWERUP_LIFE
        # tra ve loai block flame trúng để dùng trong hàm affect_environment trong class flame
        return block
            
    def check_eat_powerups(self, player):
        # hàm kiểm tra xem người chơi có "ăn" được powerup hay chưa
        x, y = player.pos
        rx, ry = int(round(x)), int(round(y)) # vì vị trí người chơi ở dạng thập phân nên cần là tròn về số nguyên
        # tại vị trí này là số gì trong ma trận (map) thì trả về đối tượng tương ứng với số đó
        if self.matrix[ry][rx] == Block.POWERUP_BOMBUP:            
            ASSETS['power_up_sound'].play()            
            self.matrix[ry][rx] = Block.GRASS
            player.max_bomb += 1
        elif self.matrix[ry][rx] == Block.POWERUP_BLAST:
            ASSETS['power_up_sound'].play()            
            self.matrix[ry][rx] = Block.GRASS
            player.bomb_blast_radius += 1
        elif self.matrix[ry][rx] == Block.POWERUP_LIFE:
            ASSETS['power_up_sound'].play()            
            self.matrix[ry][rx] = Block.GRASS
            player.lives += 1
            
    def check_enter_goal(self, x, y):
        # kiểm tra nguời chơi đi vào cổng
        x, y = round(x), round(y)
        return self.is_goal(x, y)

    def check_bomb_placeable(self, x, y):
        # kiểm tra xem có đặt được bom không, chỉ đặt được khi ở ô trống
        return self.matrix[y][x] in [Block.GRASS, Block.GOAL_CLOSE]
    
    def check_collides(self, x, y):
        # kiểm tra va chạm
        xl, xh, yl, yh = Calculate().list_colliding_coordinates(x, y) #tránh cho đối tượng không bi áp sát tường
        return self.is_solid(xl, yl) or self.is_solid(xl, yh) or self.is_solid(xh, yl) or self.is_solid(xh, yh)  





                
        
