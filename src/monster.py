import math, random
import pygame

from settings import Settings
# from game import ClassicGame, Game2Player
pygame.init()
ASSETS = {
    'monster': {
      'up': [
        pygame.image.load('assets/monster/monster_up_{}.png'.format(i)) for i in range(1, 5)
      ],
      'down': [
        pygame.image.load('assets/monster/monster_down_{}.png'.format(i)) for i in range(1, 5)
      ],
      'left': [
        pygame.image.load('assets/monster/monster_left_{}.png'.format(i)) for i in range(1, 5)
      ],
      'right': [
        pygame.image.load('assets/monster/monster_right_{}.png'.format(i)) for i in range(1, 5)
      ],
      'idle': [
        pygame.image.load('assets/monster/monster_idle_{}.png'.format(i)) for i in range(1, 5)
      ],
    },
    'monster_dead': [
      pygame.image.load('assets/monster/monster_dead_{}.png'.format(i)) for i in range(1, 6)
    ],
    'monster_dead_sound': pygame.mixer.Sound('assets/sound/monster_dead_sound.ogg'),
    'door_opening_sound': pygame.mixer.Sound('assets/sound/door_opening_sound.ogg')         
    
}
class Monster:
    V = 1.6 #van toc
    def __init__(self, game, x, y, direction):
        self.game = game
        self.pos = [x, y]        
        self.direction = direction
        self.alive = True
        self.score = 50
        self.time_to_disappear = None
        self.clock = 0
        self.seconds_since_eyes_closed = 0
        self.eyes_closed = False

    def die(self, lvl):
        ASSETS['monster_dead_sound'].play()
        self.alive = False
        self.game.score += self.score
        if(self.game.high_score < self.game.score):
            self.game.high_score = self.game.score
            if self.game.type == 'classic':
                Settings().write_file('assets/point.txt', self.game.score)
            elif self.game.type == '2player':
                Settings().write_file('assets/point2.txt', self.game.score)
        self.time_to_disappear = 1   
        if len(lvl.monsters) == 1:            
            pygame.mixer.Sound('assets/sound/door_opening_sound.ogg').play() 

    def loop(self, lvl, time):
        # t??nh to??n th???i gian v??? monster v?? th???i gian nh??y m???t
        self.clock += time
        self.seconds_since_eyes_closed += time
        self.loop_eyes()
        if self.alive:
            self.check_has_to_change_direction_due_to_bomb(lvl)
            self.move(lvl, self.V*time)
            for f in lvl.flames:
                if f.collides(*self.pos):
                    self.die(lvl)
        else:
            self.time_to_disappear -= time
            if self.time_to_disappear <= 0:
                lvl.monsters.remove(self)                

    def check_has_to_change_direction_due_to_bomb(self, lvl):
        """h??m n??y ki???m tra xem v??? tr?? ti???p theo ??i ?????n c?? tr??ng qu??? bom s??? ?????t kh??ng, n???u tr??ng 
        monster s??? ???? l??n bom v?? ??i qua bom"""
        if self.direction == 'up':
            px, nx = self.pos[0], self.pos[0]
            py, ny = math.ceil(self.pos[1]), math.floor(self.pos[1]) # vi tri c??, v??? tr?? ti???p theo s??? ?????n
            d = 'down'
        elif self.direction == 'down':
            px, nx = self.pos[0], self.pos[0]
            py, ny = math.floor(self.pos[1]), math.ceil(self.pos[1])
            d = 'up'
        elif self.direction == 'left':
            px, nx = math.ceil(self.pos[0]), math.floor(self.pos[0])
            py, ny = self.pos[1], self.pos[1]
            d = 'right'
        elif self.direction == 'right':
            px, nx = math.floor(self.pos[0]), math.ceil(self.pos[0])
            py, ny = self.pos[1], self.pos[1]
            d = 'left'
        elif self.direction == 'idle':
            return

        if (nx, ny) not in lvl.bombs:
            #n???u v??? tr?? ti???p kh??ng trung th?? ??i ti???p
            return
        elif (px, py) not in lvl.bombs:
            #n???u vt ti???p tr??ng v??? tr?? c?? kh??ng tr??ng th?? quay l???i
            self.direction = d      
        else:
            # n???u b??? ch???n th?? ?????ng y??n
            self.direction = 'idle'                          
    def maybe_try_change_directions(self, lvl):
        """h??m n??y s??? d???ng ????? ?????i h?????ng di chuy???n ng???u nhi??n"""
        x, y = int(self.pos[0]), int(self.pos[1])
        if self.direction == 'up':
            weights = [87, 3, 7, 3] #tr???ng s??? h?????ng t????ng ???ng c??c h?????ng [up, right, down, left]
        elif self.direction == 'right':
            weights = [3, 87, 3, 7]
        elif self.direction == 'down':
            weights = [7, 3, 87, 3]
        elif self.direction == 'left':
            weights = [3, 7, 3, 87]
        elif self.direction == 'idle':
            weights = [25, 25, 25, 25] # t???t c??? c??c h?????ng t????ng ??????ng nhau


        #[up, right, down, left]
        # ki???m tra c??c h?????ng xem c?? v???t c???n kh??ng, n???u kh??ng th?? ???????c ph??p ??i qua
        possible = [True, True, True, True]
        # ki???m tra xem c?? b??? bom ch???n v?? c?? v???t c???n nh?? t?????ng kh??ng
        for i, pos in enumerate([(x, y-1), (x+1, y), (x, y+1), (x-1, y)]):
            #ki???m tra bom
            for bomb in lvl.bombs.values():
                if bomb.collides(*pos):
                    possible[i] = False
                    break
            # ki???m tra v???t c???n
            possible[i] = possible[i] and not (lvl.matrix.is_solid(*pos))

         # T???ng tr???ng s??? c???a t???t c??? c??c h?????ng c?? th??? ??i
        total = sum([w for w, a in zip(weights, possible) if a])  

        # l??u l???i tr???ng s??? c???a c??c h?????ng(tr???ng s??? 1 h?????ng = tr???ng s??? c???a n?? chia t???ng (total))
        #  n???u kh??ng th??? ??i th?? l??u = 0   
        # (l??m theo c??ch n??y monster s??? ?????i h?????ng m?????t h??n, kh??ng b??? ?????t ng???t v?? ??i 1 ??o???n ????? d??i tr?????c khi ?????i) 
        weights = [w/total if a else 0 for w, a in zip(weights, possible)]   

        rnd = random.random()#ch???n gi?? tr??? ng???u nhi??n        
        d = 0
        # c???ng d???n tr???ng s??? c??c h?????ng 
        # ch???n h?????ng ?????u ti??n l??m cho t???ng c???ng d???n l???n h??n rnd ????? di chuy???n theo h?????ng ????
        for w, direction in zip(weights, ['up', 'right', 'down', 'left']):
            if w ==0:
                continue
            d += w
            if d > rnd:
                self.direction = direction
                return
        # n???u ko c??, kh???i t???o tr??? b???ng nhau
        self.direction = 'idle'        


    def move(self, lvl, distance):#0.0128
        cx, cy = self.pos
        rx, ry = round(self.pos[0]), round(self.pos[1])
        if (ry - cy == 0 and rx - cx == 0) or self.direction == 'idle':
        # n???u ?????ng th???ng v??? tr?? h??ng(c???t) th?? m???i th???c hi???n ?????i h?????ng, n???u kh??ng s??? b??? ???? l??n v???t c???n            
            self.maybe_try_change_directions(lvl)

        if self.direction == 'up':                                
            if -distance <= ry - cy < 0:
                self.pos[1] = ry
                self.maybe_try_change_directions(lvl)
                self.move(lvl, distance )
            else:
                self.pos[1] -= distance
        elif self.direction == 'down':                                
            if 0 < ry - cy <= distance:
                self.pos[1] = ry
                self.maybe_try_change_directions(lvl)
                self.move(lvl, distance )
            else:
                self.pos[1] += distance
        elif self.direction == 'left':                                
            if -distance <= rx - cx < 0:
                self.pos[0] = rx
                self.maybe_try_change_directions(lvl)
                self.move(lvl, distance )
            else:
                self.pos[0] -= distance
        elif self.direction == 'right':                                
            if 0 < rx - cx <= distance: # gi?? tr??? l??m tr??n b???ng, ho???c g???n b???ng b?????c ti???p theo(round_x = 4, current_x = 3.999)
                self.pos[0] = rx #th?? g??n lu??n v??? tr?? b???ng gi?? tr??? ????
                self.maybe_try_change_directions(lvl)
                self.move(lvl, distance )
            else:
                self.pos[0] += distance # n???u c??n c??ch xa th?? c???ng th??m b?????c nhay  
                          
    def collides(self, x, y):
        return -0.6 <= x - self.pos[0] <= 0.6 and -0.6 <= y - self.pos[1] <= 0.6
    
    def loop_eyes(self): 
        if self.seconds_since_eyes_closed >= 0.2:
            # th???i gian nh???m m???t >= 0.2s th?? m??? ra
            self.eyes_closed = False  
            #khi th???i gian self.seconds_since_eyes_closed >= 1.5       
            # th?? th???c hi???n ki???m tra xem c?? th??? nh???m m???t ti???p hay ko, n???u ???????c th?? g??n l???i
            # self.seconds_since_eyes_closed = 0
        if self.seconds_since_eyes_closed >= 1.5:
            if random.random() <= 0.5:
                self.eyes_closed = True
                self.seconds_since_eyes_closed = 0

    def draw(self, canvas):
        if self.alive:
            current_frame = int((self.clock%0.4)//0.2)# lu??n thu ???????c 2 gi?? tr??? 0, 1
            if self.eyes_closed:                
                # m???t ????ng in ra h??nh m???t ????ng
                current_frame += 2                
            canvas.draw(ASSETS['monster'][self.direction][current_frame], self.pos)
        else:
            current_frame = int((1-self.time_to_disappear)//0.2)
            canvas.draw(ASSETS['monster_dead'][current_frame], self.pos)                
            


