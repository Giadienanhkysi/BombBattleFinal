import pygame
from settings import Settings

ASSETS = {
    'player_up': pygame.image.load('assets/player/player_up.png'),
    'player_down': pygame.image.load('assets/player/player_right.png'),
    'player_left': pygame.image.load('assets/player/player_left.png'),
    'player_right': pygame.image.load('assets/player/player_right.png'),
    'player_die': [
      pygame.image.load('assets/player/player_die_{}.png'.format(i)) for i in range(1, 4)
    ],
    'player2_up': pygame.image.load('assets/player/player2_up.png'),
    'player2_down': pygame.image.load('assets/player/player2_right.png'),
    'player2_left': pygame.image.load('assets/player/player2_left.png'),
    'player2_right': pygame.image.load('assets/player/player2_right.png'),
    'player2_die': [
      pygame.image.load('assets/player/player2_die_{}.png'.format(i)) for i in range(1, 4)
    ],
    'player_die_sound': pygame.mixer.Sound('assets/sound/player_death_voice.ogg'),
    'bomb_placed_sound': pygame.mixer.Sound('assets/sound/place_bomb_sound.ogg')       
}

DEFAULT_SINGLEPLAYER_CONTROLS = {
    'up': pygame.K_UP,
    'down': pygame.K_DOWN,
    'left': pygame.K_LEFT,
    'right': pygame.K_RIGHT,
    'place_bomb': pygame.K_SPACE,
}


def calculate_distance(p1, p2):
    return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5

class Player:
    V = 2.0
    def __init__(self, game, x, y, sprite = 'p1',lives = 3, control = Settings().DEFAULT_SINGLEPLAYER_CONTROLS, max_bomb = 1, bomb_blast_radius = 2, alive = True):
        self.pos = [x, y]
        self.direction = 'down'
        self.lives = lives
        self.game = game
        self.sprite = sprite
        self.control = control
        self.max_bomb = max_bomb
        self.bomb_blast_radius = bomb_blast_radius
        self.alive = alive
        self.time_since_dead = 0
        self.trying_to_place_bomb_timer = 0

    def loop(self, lvl, time):
        if self.alive:
            for f in lvl.flames:
                if f.collides(*self.pos):
                    self.die()
            for e in lvl.monsters:
                if e.collides(*self.pos):
                    self.die()
            self.check_key_move(lvl, time)

            # xu ly đặt bom mượt hơn
            # khi đặt liên tiếp bom, trong thời gian trying_to_place_bomb_timer cho phép sẽ tự động đặt bom
            self.trying_to_place_bomb_timer -= time
            if self.trying_to_place_bomb_timer > 0:
                lvl.try_place_bomb(*self.pos, self)
        else:
            self.time_since_dead += time

    def die(self):
        self.alive = False
        self.time_since_dead = 0
        self.game.player_died()
        ASSETS['player_die_sound'].play()        
        # pass
    
    def draw(self, canvas):
        if self.sprite == 'p1':
            if self.alive:
                if self.direction == 'up':
                    img = ASSETS['player_up']
                elif self.direction == 'down':
                    img = ASSETS['player_down']
                elif self.direction == 'left':
                    img = ASSETS['player_left']
                elif self.direction == 'right':
                    img = ASSETS['player_right']
            else:
                current_frame = int((self.time_since_dead)//0.2) # 3 khung hinh moi khung hinh 0.2 s
                if current_frame == 0:
                    img = ASSETS['player_down']#khung hinh 1
                elif current_frame >= 4:
                    return
                else:
                    img = ASSETS['player_die'][current_frame-1] #trong list player die chi luu 3 khung hinh

        # phan nay de lam player2
        elif self.sprite == 'p2':
            if self.alive:
                if self.direction == 'up':
                    img = ASSETS['player2_up']
                elif self.direction == 'down':
                    img = ASSETS['player2_down']
                elif self.direction == 'left':
                    img = ASSETS['player2_left']
                elif self.direction == 'right':
                    img = ASSETS['player2_right']
            else:
                current_frame = int((self.time_since_dead)//0.2)
                if current_frame == 0:
                    img = ASSETS['player2_down']
                elif current_frame >= 4:
                    return
                else:
                    img = ASSETS['player2_die'][current_frame-1]
        canvas.draw(img, self.pos)
        

    def check_key_move(self, lvl, time):
        new_pos = self.pos[:]       
        pressed = Settings().GET_PRESSED
        distance = self.V * time

        if pressed[self.control['up']]:
            new_pos[1] -= distance
            self.direction = 'up'
        elif pressed[self.control['down']]:
            new_pos[1] += distance
            self.direction = 'down'
        elif pressed[self.control['left']]:
            new_pos[0] -= distance
            self.direction = 'left'
        elif pressed[self.control['right']]:
            new_pos[0] += distance
            self.direction = 'right'
        else:
            return
        
        if lvl.matrix.check_collides(*new_pos):
            # khi di chuyen o goc, neu du rong van se di chuyen duoc
            rounded_pos = new_pos[:]
            if self.direction == 'down' or self.direction == 'up':
                rounded_pos[0] = round(rounded_pos[0])
            elif self.direction == 'left' or self.direction == 'right':
                rounded_pos[1] = round(rounded_pos[1])
            if lvl.matrix.check_collides(*rounded_pos): #neu sau khi lam tron van va cham thi return                
                return
            
            distance *= 2            
            # xu ly di chuyen o goc
            if self.direction == 'up' or self.direction == 'down':
                dif = rounded_pos[0] - new_pos[0]
                # rounded pos cach xa new pos
                if dif > distance:#down right                                       
                    new_pos[0] += distance
                elif dif < -distance:#up left                                       
                    new_pos[0] += -distance
                else:      
                    # khi tang den khi new_pos ~ rounded pos thi cong new pos voi khoang cach do luon                  
                    new_pos[0] += dif

            elif self.direction == 'left' or self.direction == 'right':
                dif = rounded_pos[1] - new_pos[1]
                if dif > distance:
                    new_pos[1] += distance
                elif dif < -distance:
                    new_pos[1] += -distance
                else:
                    new_pos[1] += dif
            
        for bomb in lvl.bombs.values():
            if (
              bomb.collides(*new_pos) #vi tri tiep theo se den, cham bom
              and not bomb.collides_closer(*self.pos) # vi tri hien tai chua cap nhat, khong cham bom
              and calculate_distance(bomb.pos, new_pos) < calculate_distance(bomb.pos, self.pos)
            ):
                return
        self.pos = new_pos
        lvl.matrix.check_eat_powerups(self)
        if lvl.matrix.check_enter_goal(*self.pos):
            if  self.game.start_next_level_timer == None and self.game.restart_level_timer == None:
                self.game.start_next_level_timer = 0.25 #thoi gian khoi dong man moi
        
    def handle_key(self, key, lvl):
        if self.alive:
            if key == self.control['place_bomb']:
                if lvl.placed_bombs(self) < self.max_bomb:
                    if lvl.try_place_bomb(*self.pos, self):
                        ASSETS['bomb_placed_sound'].play()                        
                        self.trying_to_place_bomb_timer = 0
                    else:                        
                        self.trying_to_place_bomb_timer = 0.2
            