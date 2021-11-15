import sys
import pygame
from settings import Settings
from menu import Menu
from canvaslevel import Canvas
from game import ClassicGame, Game2Player, GameSolo
from blockmatrix import BlockMatrix


MUSIC = pygame.mixer.music.load('assets/sound/game_music.ogg')
pygame.mixer.music.play(-1)
class BomBattle():
    def __init__(self):
        self.settings = Settings()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.settings.screen_size)
        pygame.display.set_caption('BomB Battle')
        pygame.display.set_icon(pygame.image.load('assets/icon.png'))
        self.matrix = BlockMatrix()
        self.canvas = Canvas(self.screen, (0, 130))
        self.menu = Menu(self.screen, self)
        self.running = True
        self.game = None
    #cac hàm dùng trong menu
    def new_classic_game_1_player(self):
        self.menu.is_open = False
        self.game = None
        self.game = ClassicGame(self, self.screen)

    def new_classic_game_2_player(self):
        self.menu.is_open = False
        self.game = None
        self.game = Game2Player(self, self.screen)

    def new_classic_game_solo(self):
        self.menu.is_open = False
        self.game = None
        self.game = GameSolo(self, self.screen)

    def quit(self):
        self.running = False

    def resume_game(self):
        if self.game != None:
            self.menu.is_open = False

    def restart_game(self):
        self.menu.is_open = False
        if type(self.game) is ClassicGame:
            self.game = ClassicGame(self, self.screen)
        if type(self.game) is Game2Player:
            self.game = Game2Player(self, self.screen)
        if type(self.game) is GameSolo:
            self.game = GameSolo(self, self.screen)
        

    # hàm chạy chương trình
    def run_game(self):
        while self.running:
            self.clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if event.type == pygame.KEYDOWN:
                    if self.menu.is_open:
                        self.menu.handle_key(event.key)
                    elif event.key == self.settings.PAUSE_KEY:
                        self.menu.open('pause')
                    else:
                        self.game.handle_key(event.key)

            if self.menu.is_open:
                self.screen.fill((0, 0, 0))
                self.menu.draw()
            else:
                self.screen.fill((170, 220, 255))            
                self.game.loop(self.clock.get_time()/1000)                
                self.game.draw()
            
            pygame.display.flip()

        pygame.display.quit()
        pygame.quit()
        sys.exit()

if __name__ =='__main__':
    ai = BomBattle()    
    ai.run_game()