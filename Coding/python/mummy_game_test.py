import pygame
from pygame.locals import *

import json

from mummy_graph import Graph

#? PHƯƠNG THỨC LOAD + READ DATA TỪ FILE JSON
with open("./assets/map.json", "r") as file:
    map_data = json.load(file)


def get_key(X, Y):
    for item in map_data:
        if item["X"] == X and item["Y"] == Y:
            return item["key"]


def get_pos(key):
    return {"X": map_data[key]["X"], "Y": map_data[key]["Y"]}

#? KHỞI TẠO MAP
graph = Graph(6, 6)
graph.add_rectangle_vertex() # Thêm 36 nút
graph.add_rectangle_edges() # Thêm cạnh cho 36 nút của bản đồ

#? KHỞI TẠO GAME
pygame.init()
pygame.display.set_caption("Mummy Maze")

#? TẠO WINDOW
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

DISPLAY = pygame.display.set_mode((600, 600))

#? ASSETS
MAP_IMG = pygame.image.load("./assets/map.jpg")

# Player's Sprites
PLAYER_UP_IMG = pygame.image.load("./assets/player/player_up.png")
PLAYER_DOWN_IMG = pygame.image.load("./assets/player/player_down.png")
PLAYER_LEFT_IMG = pygame.image.load("./assets/player/player_left.png")
PLAYER_RIGHT_IMG = pygame.image.load("./assets/player/player_right.png")

# Mummy's Sprites
MUMMY_UP_IMG = pygame.image.load("./assets/mummy/mummy_up.png")
MUMMY_DOWN_IMG = pygame.image.load("./assets/mummy/mummy_down.png")
MUMMY_LEFT_IMG = pygame.image.load("./assets/mummy/mummy_left.png")
MUMMY_RIGHT_IMG = pygame.image.load("./assets/mummy/mummy_right.png")

#? CONSTANTS
SPRITES_OPTIONS = {
    0: (0, 0, 60, 60),
    1: (60, 0, 60, 60),
    2: (120, 0, 60, 60),
    3: (180, 0, 60, 60),
    4: (240, 0, 60, 60),
}

MAP_SURFACE = pygame.transform.scale(MAP_IMG, (600, 600))

SPEED = 5

GO_DISTANCE = 100

WIN_KEY = 35
WIN_POS = get_pos(WIN_KEY)
WIN_POS = {"X": 300, "Y": 500} 


WALL_POS = get_pos(21)
WALL_WIDTH = 8
WALL_HEIGHT = 100


# COLORS
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

class Wall:
    """
        @param orientation: nhận giá trị "horizontal" hoặc "vertical"
    """
    def __init__(self, wall_key, color, orientation="horizontal"):
        self.width = 100
        self.height = 15
        self.surface = pygame.Surface((self.width, self.height))
        self.wall_pos = get_pos(wall_key)
        self.color = color
        self.orientation = orientation  # Thêm thuộc tính orientation
        
        # Thêm thuộc tính rect để kiểm tra va chạm
        self.rect = pygame.Rect(self.wall_pos['X'], self.wall_pos['Y'], self.width, self.height)
    
    def setup(self, orientation):
        self.surface.fill((0, 0, 0, 0))
        
        if self.orientation == "horizontal":
            self.width = GO_DISTANCE
            self.height = 5
        elif self.orientation == "vertical":
            self.width = 5
            self.height = GO_DISTANCE
    
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        
    def draw(self, orientation):
        self.setup(orientation)
        DISPLAY.blit(self.surface, (self.wall_pos['X'], self.wall_pos['Y']))

#TODO: GAME MANAGER
class GameManager:
    mummy_move = 0 
    can_player_move = True
    game_over = False
    win = False
    
    wall_list = []

#TODO: CLASS PLAYER - NHÂN VẬT NGƯỜI CHƠI
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.img = PLAYER_DOWN_IMG
        self.surface = pygame.Surface((100, 100), SRCALPHA)
        self.option = 0
        self.time_count = 0
        
        self.go = 0
        
        self.rect = self.surface.get_rect()
        
    def animate(self):
        if self.option in SPRITES_OPTIONS:
            coords = SPRITES_OPTIONS[self.option]
            self.surface.blit(self.img, (20, 20), coords)
            
    def draw(self):
        DISPLAY.blit(self.surface, (self.x, self.y))
        
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)
        
    def update(self, left, down, up, right):
        
        if GameManager.mummy_move == 0:
            if self.go < GO_DISTANCE:
                if self.time_count < SPEED:
                    self.option = 0
                elif self.time_count < SPEED*2:
                    self.option = 1
                elif self.time_count < SPEED*3:
                    self.option = 2
                elif self.time_count < SPEED*4:
                    self.option = 3
                elif self.time_count < SPEED*5:
                    self.option = 4
                
                if self.time_count > SPEED*5:
                    self.time_count = 0
                    
                # Xử lí di chuyển    
                if left or right or up or down:
                    self.surface.fill((0, 0, 0, 0))
                    self.time_count += 1
                    self.go += SPEED
                
                    if left:
                        self.img = PLAYER_LEFT_IMG
                        self.x -= SPEED
                        
                    if right:
                        self.img = PLAYER_RIGHT_IMG
                        self.x += SPEED
                        
                    if up:
                        self.img = PLAYER_UP_IMG
                        self.y -= SPEED
                        
                    if down:
                        self.img = PLAYER_DOWN_IMG
                        self.y += SPEED
                    
                self.animate()
            else:
                self.go = 0
                
                # Kiểm tra người chơi có chủ động đụng mummy không?
                if player.rect.colliderect(mummy.rect):
                    GameManager.game_over = True
                else:
                    # Kiểm tra chiến thắng
                    player_key = get_key(player.x, player.y)
                    
                    if player_key == WIN_KEY:
                        GameManager.game_over = True
                        GameManager.win = True
                    else:
                        GameManager.mummy_move = 1 
        
#TODO: CLASS MUMMY - NHÂN VẬT NPC XÁC UỚP
class Mummy:
    def __init__(self):
        self.x = 500
        self.y = 500
        self.img = MUMMY_DOWN_IMG
        self.surface = pygame.Surface((100, 100), SRCALPHA)
        self.option = 0
        self.time_count = 0
        
        self.go = 0
        self.run_pos = {"X": self.x, "Y": self.y}
        
        self.rect = self.surface.get_rect()
        
    def animate(self):
        if self.option in SPRITES_OPTIONS:
            coords = SPRITES_OPTIONS[self.option]
            self.surface.blit(self.img, (20, 20), coords)
            
    def draw(self):
        DISPLAY.blit(self.surface, (self.x, self.y))
    
    def update_rect(self):
        self.rect.topleft = (self.x, self.y)
        
    
    def check_wall_collision(self, new_x, new_y):
        # Kiểm tra va chạm với tất cả các bức tường
        for wall in GameManager.wall_list:
            if wall.rect.colliderect(pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)):
                return True  # Nếu va chạm, trả về True
        return False  # Nếu không va chạm, trả về False    
        
    def update(self, left, right, up, down):
        if self.go < GO_DISTANCE:
            if self.time_count < SPEED:
                self.option = 0
            elif self.time_count < SPEED*2:
                self.option = 1
            elif self.time_count < SPEED*3:
                self.option = 2
            elif self.time_count < SPEED*4:
                self.option = 3
            elif self.time_count < SPEED*5:
                self.option = 4
            
            if self.time_count > SPEED*5:
                self.time_count = 0
                
            if left or right or up or down:
                self.surface.fill((0, 0, 0, 0))
                self.time_count += 1
                self.go += SPEED
                
                # Lưu trữ vị trí cũ của mummy
                old_x, old_y = self.x, self.y
            
                if left:
                    self.img = MUMMY_LEFT_IMG
                    self.x -= SPEED
                    
                if right:
                    self.img = MUMMY_RIGHT_IMG
                    self.x += SPEED
                    
                if up:
                    self.img = MUMMY_UP_IMG
                    self.y -= SPEED
                    
                if down:
                    self.img = MUMMY_DOWN_IMG
                    self.y += SPEED
                    
                # Kiểm tra va chạm với tường
                if self.check_wall_collision(self.x, self.y):
                    # Nếu có va chạm, quay lại vị trí cũ
                    self.x, self.y = old_x, old_y    
                    
            self.animate()
        else:
            self.go = 0
            GameManager.mummy_move += 1
            
            # kiểm tra xác ướp đã đi 2 lượt chưa
            if GameManager.mummy_move == 3:
                GameManager.mummy_move = 0
                GameManager.can_player_move = True
        
        
    def run(self, key_player, player_x, player_y):
        
        # Kiểm tra vị trí của nút tiếp theo để di chuyển mummy
        
        # Thay đổi theo chiều dọc
        if self.y != self.run_pos["Y"]:
            # TH1: đi lên
            if self.y > self.run_pos["Y"]:
                self.update(up=True, down=False, left=False, right=False)
            else: # TH2: đi xuống
                self.update(up=False, down=True, left=False, right=False)
        elif self.x != self.run_pos["X"]:
            # Thay đổi theo chiều ngang
            if self.x > self.run_pos["X"]: # TH3: đi qua trái
                self.update(up=False, down=False, left=True, right=False)
            else: # TH4: đi qua phải
                self.update(up=False, down=False, left=False, right=True)
        else:
            key_mummy = get_key(self.x, self.y)
            
            # Kiểm tra mummy có đụng player chưa
            if key_mummy == key_player:
                GameManager.game_over = True
                
            else:    
                # Kiểm tra logic tường
                wall_key = 21
                
                # Đk1: mummy đang đứng bên phải cái tường, Đk2: # mummy đang đứng bên trái cái tường
                if (key_mummy == wall_key and player_x < mummy.x) or (key_mummy == wall_key - 1 and player_x > mummy.x): 
                    if player_y == mummy.y: # đang đứng ngang với mummy (có tường dọc che)
                        GameManager.mummy_move = 0
                        GameManager.can_player_move = True
                    elif player_y < mummy.y:
                        self.run_pos["Y"] -= GO_DISTANCE
                    else:
                        self.run_pos["Y"] += GO_DISTANCE
                else:
                    run_key = graph.find_next_step(key_mummy, key_player)
                    self.run_pos = get_pos(run_key)
                    

#? VÒNG LẶP GAME
running = True

player = Player()
mummy = Mummy()

# wall_surface = pygame.Surface((WALL_WIDTH, WALL_HEIGHT))
#wall_surface2 = pygame.Surface((WALL_WIDTH2, WALL_HEIGHT2))

win_surface = pygame.Surface((100, 100))

wall_hori = Wall(27, BLUE , "horizontal")
wall_verti = Wall(21, RED , "vertical")
wall_verti2 = Wall(16, RED , "vertical")

# Đưa các tường vào danh sách wall_list
GameManager.wall_list = [wall_hori, wall_verti, wall_verti2]

#? STATES
player_up, player_down, player_left, player_right = False, False, False, False

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
            
        if event.type == KEYDOWN and GameManager.can_player_move:
            if event.key == K_UP:
                player_up = True
            if event.key == K_DOWN:
                player_down = True
            if event.key == K_LEFT:
                player_left = True
            if event.key == K_RIGHT:
                player_right = True        
            
            GameManager.can_player_move = False
            
        if event.type == KEYDOWN and event.key == K_r and GameManager.game_over == True:
            # Reset Game
            player.x, player.y = 0, 0
            mummy.x, mummy.y = 500, 200
            
            mummy.run_pos = {'X': mummy.x, 'Y': mummy.y}
            
            
            player.go = 0
            
            GameManager.game_over = False
            GameManager.win = False
            GameManager.mummy_move = 0
            GameManager.can_player_move = True
        
            
    #? CLEAR WINDOW
    DISPLAY.fill((0, 0, 0, 0))
    
    # Setup map 
    DISPLAY.blit(MAP_SURFACE, (0, 0))
    
    # # Setup wall    
    # wall_surface.fill(RED)
    # DISPLAY.blit(wall_surface, (WALL_POS['X'], WALL_POS['Y']))
    wall_hori.draw("horizontal")
    wall_verti.draw("vertical")
    wall_verti2.draw("vertical")
    
    # Setup ô chiến thắng
    win_surface.fill((0, 255, 0))
    DISPLAY.blit(win_surface, (WIN_POS['X'], WIN_POS['Y']))
    

    
    #? TẠO PLAYER VÀ MUMMY TRÊN GAME
    player.draw()
    
    #? KIỂM TRA PLAYER CÓ ĐƯỢC DI CHUYỂN HAY KHÔNG? --> 1. Vị trí trên bản đồ, 2. Bức tường
    
    player.update(up=player_up, down=player_down, left=player_left, right=player_right)
    
    mummy.draw()
    mummy.animate()
    
    #? CẬP NHẬT TRẠNG THÁI CỦA NHÂN VẬT
    player.update_rect()
    mummy.update_rect()

    
    if GameManager.game_over == False:
        if player.go == 0:
            player_up, player_down, player_left, player_right = False, False, False, False
        
        if GameManager.mummy_move >= 1:
            player_key = get_key(player.x, player.y)
            mummy.run(player_key, player.x, player.y)
    else:
        player_up, player_down, player_left, player_right = False, False, False, False
        
        if GameManager.win == False:
            # Load thông tin thua game
            lose_message = pygame.transform.scale(pygame.image.load("./assets/try_again_text.png"), (250, 46))
            lose_background = pygame.transform.scale(pygame.image.load("./assets/end.png"), (540, 401))
            
            lose_board_surface = pygame.Surface((540, 401), SRCALPHA)
            lose_board_surface.blit(lose_background, (0, 0))
            lose_board_surface.blit(lose_message, (150, 300))
            
            DISPLAY.blit(lose_board_surface, (30, 100))
            

        else:  # Load thông tin thắng game: 
            
            win_message = pygame.transform.scale(pygame.image.load("./assets/win_text.png"), (591, 282))
            DISPLAY.blit(win_message, (0, 150))
    
    #? CẬP NHẬT TRẠNG THÁI GAME
    pygame.display.update()
    pygame.time.Clock().tick(60)
    

pygame.quit()