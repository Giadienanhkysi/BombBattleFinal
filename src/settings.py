import math
import pygame
pygame.init()
class Settings:    
    def __init__(self):               
        self.DEFAULT_SINGLEPLAYER_CONTROLS = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'place_bomb': pygame.K_SPACE,
        }

        self.DEFAULT_DOUBLEPLAYER_CONTROLS_PLAYER_1 = {
            'up': pygame.K_w,
            'down': pygame.K_s,
            'left': pygame.K_a,
            'right': pygame.K_d,
            'place_bomb': pygame.K_SPACE,
        }

        self.DEFAULT_DOUBLEPLAYER_CONTROLS_PLAYER_2 = {
            'up': pygame.K_UP,
            'down': pygame.K_DOWN,
            'left': pygame.K_LEFT,
            'right': pygame.K_RIGHT,
            'place_bomb': pygame.K_RETURN,
        }

       
        self.GET_PRESSED = pygame.key.get_pressed()

        self.PAUSE_KEY = pygame.K_ESCAPE
        self.SELECT_KEY = pygame.K_RETURN
        self.UP_KEY = pygame.K_UP 
        self.DOWN_KEY = pygame.K_DOWN
        
        self.GAME_FONT_MENU = pygame.font.Font('assets/font/PixelMiners-KKal.otf', 32) 
        self.GAME_FONT_GAME_BAR = pygame.font.Font('assets/font/PixelMiners-KKal.otf', 20) 

        self.screen_size = 650, 780
        self.running = True
        self.playtime = 200
        self.high_score = self.read_file('assets/point.txt')
        self.high_score_2 = self.read_file('assets/point2.txt')

    def read_file(self, file_name):
        with open(file_name) as file_object:
            return int(file_object.read())

    def write_file(self, file_name, score):
        with open(file_name, 'w') as file_object:
            file_object.write(str(score))

class Calculate:
    @staticmethod
    def list_colliding_coordinates(x, y):
        print(x, y)
        print(math.floor(x), math.ceil(x), math.floor(y), math.ceil(y))
        return math.floor(x), math.ceil(x), math.floor(y), math.ceil(y)
        
    @staticmethod
    def calculate_distance(p1, p2):
        return ((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)**0.5