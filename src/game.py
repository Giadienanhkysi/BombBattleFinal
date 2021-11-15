import pygame
from settings import Settings
from canvaslevel import Canvas, Level
from monster import Monster
ASSETS = {
    'logo_game': pygame.image.load('assets/logo_game_1.png'),   
    'game_over_sound': pygame.mixer.Sound('assets/sound/game_over_sound.ogg') 
}
class Game:
    def __init__(self, ai_game, screen, initial_time=200):
        self.ai_game = ai_game
        self.screen = screen
        self.initial_time = initial_time

        self.time = None
        self.level = None 
        self.initialize_level()
        
    def loop(self, time):        
        self.time -= time
        self.time_ups_update()
        self.level.loop(time)

    def draw(self):
        self.draw_gamebar()
        self.level.draw()
        
    #xử lý nút bấm
    def handle_key(self, key):
        self.level.handle_key(key)
    
# Abstract method
    #khởi tạo level mới
    def initialize_level(self):
        pass

    #xử lý gamebar    
    def draw_gamebar(self):
        pass
    
    def time_ups_update(self):
        pass


class ClassicGame(Game):
    '''lơp này khởi tạo chế độ chơi'''
    def __init__(self, ai_game, screen, initial_time=Settings().playtime, lives=3):
        self.score = 0
        self.stage = 1
        self.lives = lives
        self.max_bomb  = 1
        self.bomb_blast_radius = 2
        self.high_score = Settings().high_score
        self.type = 'classic'
        self.restart_level_timer = None #thời gian khởi động lại màn chơi
        self.start_next_level_timer = None #thời gian chuyển màn chơi tiếp theo
        super().__init__(ai_game, screen, initial_time)
        
    def initialize_level(self):
        # khởi tạo màn chơi mới
        self.restart_level_timer = None
        self.start_next_level_timer = None
        self.time = self.initial_time

        canvas = Canvas(self.screen, (0, 130))
        e, b = self.game_difficulty()
        self.level = Level.singleplayer(self, canvas, 
          max_bomb = self.max_bomb, bomb_blast_radius=self.bomb_blast_radius,
          monsters_lim=e, boxes_lim=b
        )

    def game_difficulty(self):
        self.initial_time -= 2*self.stage #sau mỗi màn giảm thời gian chơi 
        if self.stage == 1:
            return 3, [15, 20]
        if self.stage == 2:
            return 4, [15, 30] 
        if self.stage == 3:
            return 5, [23, 35]
        if self.stage <= 5:
            return 6, [30, 40]
        if self.stage <= 10:
            return 7, [35, 45]
        return 10, [40, 60]

    def mission_failed(self):
        if self.lives > 1:
            self.lives -= 1
            self.initialize_level()
        else:
            # nếu hết mạng phát tiếng game over và chuyển ra menu gameover
            ASSETS['game_over_sound'].play()           
            self.ai_game.menu.open('gameover', score=self.score, stage=self.stage)
    
    def mission_complete(self):
        pygame.mixer.Sound('assets/sound/next_stage_sound.ogg').play()
        self.stage += 1
        self.bomb_blast_radius = self.level.players[0].bomb_blast_radius
        self.max_bomb = self.level.players[0].max_bomb 
        self.initialize_level()

    def loop(self, time):
        if self.restart_level_timer != None:
            self.restart_level_timer -= time
            if self.restart_level_timer <= 0:
                self.mission_failed()
        if self.start_next_level_timer != None:
            self.start_next_level_timer -= time
            if self.start_next_level_timer <= 0:
                self.mission_complete()
        super().loop(time)
    
    def draw_gamebar(self):
        if self.time <= 0: 
            timer = 'TIME\'S UP'
            timer = Settings().GAME_FONT_GAME_BAR.render(timer, True, (200, 0, 0))
        else:
            timer = 'TIME:  {:03d}'.format(int(self.time))
            timer = Settings().GAME_FONT_GAME_BAR.render(timer, True, (30, 30, 30))
        
        score = 'SCORE:  {:04d}'.format(self.score)
        score = Settings().GAME_FONT_GAME_BAR.render(score, True, (30, 30, 30))
        
        hscore = 'H.SCO:  {:04d}'.format(self.high_score)
        hscore = Settings().GAME_FONT_GAME_BAR.render(hscore, True, (30, 30, 30))

        stage = 'STAGE:  {:02d}'.format(self.stage)
        stage = Settings().GAME_FONT_GAME_BAR.render(stage, True, (30, 30, 30))
        
        lives = 'LIVES:  {:02d}'.format(self.lives)
        lives = Settings().GAME_FONT_GAME_BAR.render(lives, True, (30, 30, 30))

        logo_game = pygame.transform.scale(ASSETS['logo_game'], (250, 250))

        self.screen.blit(stage, stage.get_rect(left = 30, centery = 35))
        self.screen.blit(timer, timer.get_rect(right = 610, centery = 35))
        self.screen.blit(hscore, hscore.get_rect(left = 30, centery = 70))
        self.screen.blit(score, score.get_rect(left = 30, centery = 100))
        self.screen.blit(logo_game, logo_game.get_rect(centerx=325, top = -60))
        self.screen.blit(lives, lives.get_rect(right = 610, centery = 100))

    def time_ups_update(self):
        if self.time <= 0: 
            # khi gọi hàm khởi tạo màn mới 2 biến = None khi đó sẽ đặt thời gian khởi tạo màn mới
            if self.restart_level_timer == None and self.start_next_level_timer == None:                
                self.restart_level_timer = 2.5

    def player_died(self):
        # hàm initialize_level() đc gọi
        if self.restart_level_timer == None and self.start_next_level_timer == None:
            self.restart_level_timer = 4 # thời gian kể từ khi chết


class Game2Player(Game):
    def __init__(self, ai_game, screen, initial_time=Settings().playtime,
            max_bomb = [1,1],
            bomb_blast_radius =[2,2]
        ):
        
        self.score = 0
        self.stage = 1
        self.lives = [3,3]
        self.max_bomb  = max_bomb
        self.bomb_blast_radius = bomb_blast_radius
        self.high_score = Settings().high_score_2
        self.type = '2player'
        self.restart_level_timer = None #thời gian khởi động lại màn chơi
        self.start_next_level_timer = None #thời gian chuyển màn chơi tiếp theo
        super().__init__(ai_game, screen, initial_time)

    def initialize_level(self):
        self.restart_level_timer = None
        self.start_next_level_timer = None
        self.time = self.initial_time

        canvas = Canvas(self.screen, (0, 130))
        e, b = self.game_difficulty()

        self.level = Level.doubleplayer(self, canvas, 
                    max_bomb = self.max_bomb, bomb_blast_radius=self.bomb_blast_radius,
                    monsters_lim=e, boxes_lim=b, lives = self.lives
                )
            
        
    def game_difficulty(self):
        self.initial_time -= 2*self.stage #sau mỗi màn giảm thời gian chơi 
        # return [monster] [boxs]
        if self.stage == 1:
            return 3, [15, 20]
        if self.stage == 2:
            return 4, [15, 30] 
        if self.stage == 3:
            return 5, [23, 35]
        if self.stage <= 5:
            return 6, [30, 40]
        if self.stage <= 10:
            return 7, [35, 45]
        return 10, [40, 60]

    def mission_failed(self):
        if self.lives[0] > 1 or self.lives[1] > 1:
            if self.lives[0] > 0 and self.level.players[0].alive == False:
                self.level.players[0].lives -=1
                self.lives[0] = self.level.players[0].lives
                print(f"[Player 1] {self.lives[0]}")
            if self.lives[1] > 0 and self.level.players[1].alive == False:
                self.level.players[1].lives -=1
                self.lives[1] = self.level.players[1].lives
                print(f"[Player 2] {self.lives[1]}")
            self.initialize_level()
        else:
            # nếu hết mạng phát tiếng game over và chuyển ra menu gameover
            ASSETS['game_over_sound'].play()           
            self.ai_game.menu.open('gameover', score=self.score, stage=self.stage)

    def mission_complete(self):
        pygame.mixer.Sound('assets/sound/next_stage_sound.ogg').play()
        self.stage += 1
        self.bomb_blast_radius = [self.level.players[0].bomb_blast_radius,
                                    self.level.players[1].bomb_blast_radius]
        self.max_bomb = [self.level.players[0].max_bomb,
                        self.level.players[1].max_bomb]
        self.initialize_level()

    def loop(self, time):
        if self.restart_level_timer != None:
            self.restart_level_timer -= time
            if self.restart_level_timer <= 0:
                self.mission_failed()
        if self.start_next_level_timer != None:
            self.start_next_level_timer -= time
            if self.start_next_level_timer <= 0:
                self.mission_complete()
        super().loop(time)

    def draw_gamebar(self):
        if self.time <= 0: 
            timer = 'TIME\'S UP'
            timer = Settings().GAME_FONT_GAME_BAR.render(timer, True, (200, 0, 0))
        else:
            timer = 'TIME:  {:03d}'.format(int(self.time))
            timer = Settings().GAME_FONT_GAME_BAR.render(timer, True, (30, 30, 30))
        
        score = 'SCORE:  {:04d}'.format(self.score)
        score = Settings().GAME_FONT_GAME_BAR.render(score, True, (30, 30, 30))
        
        hscore = 'H.SCO:  {:04d}'.format(self.high_score)
        hscore = Settings().GAME_FONT_GAME_BAR.render(hscore, True, (30, 30, 30))

        stage = 'STAGE:  {:02d}'.format(self.stage)
        stage = Settings().GAME_FONT_GAME_BAR.render(stage, True, (30, 30, 30))

        # lives
        lives1 = 'LIVES1:  {:02d}'.format(self.lives[0])
        lives1 = Settings().GAME_FONT_GAME_BAR.render(lives1, True, (30, 30, 30))
        
        lives2 = 'LIVES2:  {:02d}'.format(self.lives[1])
        lives2 = Settings().GAME_FONT_GAME_BAR.render(lives2, True, (30, 30, 30))

        logo_game = pygame.transform.scale(ASSETS['logo_game'], (250, 250))

        self.screen.blit(stage, stage.get_rect(left = 30, centery = 35))
        self.screen.blit(timer, timer.get_rect(right = 610, centery = 35))
        self.screen.blit(hscore, hscore.get_rect(left = 30, centery = 70))
        self.screen.blit(score, score.get_rect(left = 30, centery = 100))
        self.screen.blit(logo_game, logo_game.get_rect(centerx=325, top = -60))
        self.screen.blit(lives1, lives1.get_rect(right = 610, centery = 70))
        self.screen.blit(lives2, lives2.get_rect(right = 610, centery = 100))

    def time_ups_update(self):
        if self.time <= 0: 
            # khi gọi hàm khởi tạo màn mới 2 biến = None khi đó sẽ đặt thời gian khởi tạo màn mới
            if self.restart_level_timer == None and self.start_next_level_timer == None:                
                self.restart_level_timer = 2.5

    def player_died(self):
        # hàm initialize_level() đc gọi
        if self.restart_level_timer == None and self.start_next_level_timer == None:
            self.restart_level_timer = 4 # thời gian kể từ khi chết

class GameSolo(Game):
    def __init__(self, ai_game, screen, initial_time=150,
            lives = [1,1],
            max_bomb = [1,1],
            bomb_blast_radius =[2,2]
        ):
        
        self.score = 0
        self.lives = lives
        self.max_bomb  = max_bomb
        self.bomb_blast_radius = bomb_blast_radius
        self.high_score = Settings().high_score

        self.restart_level_timer = None #thời gian khởi động lại màn chơi
        self.start_next_level_timer = None #thời gian chuyển màn chơi tiếp theo
        super().__init__(ai_game, screen, initial_time)

    def initialize_level(self):
        self.restart_level_timer = None
        self.start_next_level_timer = None
        self.time = self.initial_time

        canvas = Canvas(self.screen, (0, 130))

        self.level = Level.solo_mode(self, canvas, 
                    max_bomb = self.max_bomb, bomb_blast_radius=self.bomb_blast_radius,
                    monsters_lim=5, boxes_lim=[15,30], lives= self.lives
                )

    def mission_failed(self):
        ASSETS['game_over_sound'].play()       
        if(self.level.players[0].alive == False):
            self.ai_game.menu.open('gameoverSolo', score=0, stage=0 ,IDplayer = '2')
        elif(self.level.players[1].alive == False):
            self.ai_game.menu.open('gameoverSolo', score=0, stage=0 ,IDplayer = '1')
        else:
            self.ai_game.menu.open('gameoverSolo', score=0, stage=0 ,IDplayer = '0')

    def loop(self, time):
        if int(self.time) == 10:
            if len(self.level.monsters) < 50:
                self.level.monsters.append(Monster(self, 11,11, 'up'))
        if self.restart_level_timer != None:
            self.restart_level_timer -= time
            if self.restart_level_timer <= 0:
                self.mission_failed()        
        super().loop(time)

    def draw_gamebar(self):
        if self.time <= 0: 
            timer = 'TIME\'S UP'
            timer = Settings().GAME_FONT_GAME_BAR.render(timer, True, (200, 0, 0))
        else:
            timer = 'TIME:  {:03d}'.format(int(self.time))
            timer = Settings().GAME_FONT_GAME_BAR.render(timer, True, (30, 30, 30))
        
        mode = 'DEAD  OR  ALIVE'
        mode = Settings().GAME_FONT_GAME_BAR.render(mode, True, (30, 30, 30))
        logo_game = pygame.transform.scale(ASSETS['logo_game'], (250, 250))

        self.screen.blit(timer, timer.get_rect(right = 610, centery = 35))
        self.screen.blit(logo_game, logo_game.get_rect(centerx=325, top = -60))
        self.screen.blit(mode, mode.get_rect(left = 30, centery = 35))

    def time_ups_update(self):
        if self.time <= 0: 
            # khi gọi hàm khởi tạo màn mới 2 biến = None khi đó sẽ đặt thời gian khởi tạo màn mới
            if self.restart_level_timer == None and self.start_next_level_timer == None:                
                self.restart_level_timer = 2.5

    def player_died(self):
        # hàm initialize_level() đc gọi
        if self.restart_level_timer == None and self.start_next_level_timer == None:
            self.restart_level_timer = 4 # thời gian kể từ khi chết            