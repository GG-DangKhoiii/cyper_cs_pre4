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
WIN_IMG = pygame.image.load("./assets/player/win_gate.jpg")

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

WIN_KEY = 32
WIN_POS = get_pos(WIN_KEY)
# WIN_POS = {"X": 200, "Y": 500} 


WALL_POS = get_pos(21)
WALL_WIDTH = 8
WALL_HEIGHT = 100


# COLORS
RED = (255, 0, 0)
# GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
BROWN = (139, 69, 19)

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
            self.height = 8
        elif self.orientation == "vertical":
            self.width = 8
            self.height = GO_DISTANCE
    
        self.surface = pygame.Surface((self.width, self.height))
        self.surface.fill(self.color)
        
                # Thiết lập rect chính xác hơn
        self.rect = pygame.Rect(
            self.wall_pos['X'],
            self.wall_pos['Y'],
            self.width,
            self.height
        )
        
    def draw(self, orientation):
        self.setup(orientation)
        DISPLAY.blit(self.surface, (self.wall_pos['X'], self.wall_pos['Y']))

#TODO: GAME MANAGER
class GameManager:
    mummy_move = 0 
    can_player_move = True
    game_over = False
    waiting_for_restart = False
    win = False
    
    wall_list = []
    
    @classmethod
    def reset_game(cls, player, mummy):
        """Reset toàn bộ trạng thái game về ban đầu"""
        cls.mummy_move = 0
        cls.can_player_move = True
        cls.game_over = False
        cls.win = False

        # Reset player và mummy thông qua tham chiếu
        player.x, player.y = 0, 0
        player.go = 0
        player.update_rect()
        
        mummy.x, mummy.y = 500, 500
        mummy.run_pos = {'X': mummy.x, 'Y': mummy.y}
        mummy.update_rect()

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
        self.rect = pygame.Rect(self.x + 10, self.y + 10, 80, 80)  # Sửa ở đây
        self.reset_animation()

    def reset_animation(self):
        """Khởi tạo animation ban đầu"""
        self.surface.fill((0, 0, 0, 0))
        if hasattr(self, 'img'):
            self.surface.blit(self.img, (20, 20), SPRITES_OPTIONS.get(self.option, (0, 0, 60, 60)))


    def animate(self):
        """Cập nhật animation theo trạng thái hiện tại"""
        self.surface.fill((0, 0, 0, 0))
        coords = SPRITES_OPTIONS.get(self.option, (0, 0, 60, 60))
        self.surface.blit(self.img, (20, 20), coords)

    def get_collision_rect(self, x=None, y=None):
        x = x if x is not None else self.x
        y = y if y is not None else self.y
        return pygame.Rect(x + 10, y + 10, 80, 80)

    def check_collision(self, new_x, new_y):
        test_rect = pygame.Rect(
            new_x + 25,  # Offset từ biên
            new_y + 25,
            50,          # Chiều rộng hitbox (100 - 25*2)
            50           # Chiều cao hitbox
        )
        
        if (new_x < 0 or new_x > WINDOW_WIDTH - 100 or
            new_y < 0 or new_y > WINDOW_HEIGHT - 100):
            return True
            
        for wall in GameManager.wall_list:
            if test_rect.colliderect(wall.rect):
                return True
            
        return False

    def try_move(self, dx, dy):
        new_x = self.x + dx
        new_y = self.y + dy
        
        if not self.check_collision(new_x, new_y):
            self.x = new_x
            self.y = new_y
            return True
        else:
            return False

    def draw(self):
        DISPLAY.blit(self.surface, (self.x, self.y))

    def update_rect(self):
        self.collision_rect = self.get_collision_rect()

    def handle_turn_end(self):
        self.go = 0
        self.update_rect()
        if pygame.Rect(self.x, self.y, 100, 100).colliderect(mummy.rect):
            GameManager.game_over = True
        else:
            player_key = get_key(self.x, self.y)
            if player_key == WIN_KEY:
                GameManager.game_over = True
                GameManager.win = True
            else:
                GameManager.mummy_move = 1
                GameManager.can_player_move = True
                
    def update(self, left, down, up, right):
        if GameManager.mummy_move == 0:
            if self.go < GO_DISTANCE:
                # Xử lý animation chỉ khi di chuyển hợp lệ
                if left or right or up or down:
                    self.time_count += 1
                    if self.time_count > SPEED*5:
                        self.time_count = 0
                    
                    # Tính toán vị trí mới
                    new_x, new_y = self.x, self.y
                    if left: new_x -= SPEED
                    if right: new_x += SPEED
                    if up: new_y -= SPEED
                    if down: new_y += SPEED
                    
                    # Kiểm tra va chạm
                    if not self.check_collision(new_x, new_y):
                        # Di chuyển hợp lệ
                        self.x, self.y = new_x, new_y
                        self.go += SPEED
                        
                        # Cập nhật hình ảnh theo hướng di chuyển
                        if left: self.img = PLAYER_LEFT_IMG
                        elif right: self.img = PLAYER_RIGHT_IMG
                        elif up: self.img = PLAYER_UP_IMG
                        elif down: self.img = PLAYER_DOWN_IMG
                        
                        # Cập nhật animation chỉ khi di chuyển
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
                    else:
                        # Nếu đụng tường, vẫn tính là đã dùng lượt đi
                        self.go = GO_DISTANCE
                    
                    self.animate()
            else:
                # Kết thúc lượt đi
                self.handle_turn_end()
        
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
        for wall in GameManager.wall_list:
            if wall.rect.colliderect(pygame.Rect(new_x, new_y, self.rect.width, self.rect.height)):
                return True
        return False

    def try_move(self, direction):
        old_x, old_y = self.x, self.y
        
        if direction == "left":
            self.x -= SPEED
            self.img = MUMMY_LEFT_IMG
        elif direction == "right":
            self.x += SPEED
            self.img = MUMMY_RIGHT_IMG
        elif direction == "up":
            self.y -= SPEED
            self.img = MUMMY_UP_IMG
        elif direction == "down":
            self.y += SPEED
            self.img = MUMMY_DOWN_IMG
        
        if self.check_wall_collision(self.x, self.y):
            self.x, self.y = old_x, old_y
            return False
        return True

    def update(self, left, right, up, down):
        if self.go < GO_DISTANCE * 2:  # Đảm bảo di chuyển 2 ô (200px)
            if self.time_count < SPEED:
                self.option = 0
            elif self.time_count < SPEED * 2:
                self.option = 1
            elif self.time_count < SPEED * 3:
                self.option = 2
            elif self.time_count < SPEED * 4:
                self.option = 3
            elif self.time_count < SPEED * 5:
                self.option = 4

            if self.time_count > SPEED * 5:
                self.time_count = 0

            if left or right or up or down:
                self.surface.fill((0, 0, 0, 0))
                self.time_count += 1
                self.go += SPEED

                # Thử các hướng di chuyển theo thứ tự ưu tiên
                directions = []
                if left: directions.append("left")
                if right: directions.append("right")
                if up: directions.append("up")
                if down: directions.append("down")
                
                # Thêm các hướng khác nếu cần
                all_directions = ["left", "right", "up", "down"]
                for direction in all_directions:
                    if direction not in directions:
                        directions.append(direction)
                
                # Thử từng hướng cho đến khi thành công
                moved = False
                for direction in directions:
                    if self.try_move(direction):
                        moved = True
                        break
                
                self.animate()
        else:
            self.go = 0
            GameManager.mummy_move += 1
            
            if GameManager.mummy_move >= 2:  # Giữ nguyên cơ chế 2 bước
                GameManager.mummy_move = 0
                GameManager.can_player_move = True

    def run(self, key_player, player_x, player_y):
        if GameManager.mummy_move < 1:
            return
            
        key_mummy = get_key(self.x, self.y)
        
        # Kiểm tra va chạm với player
        if key_mummy == key_player:
            GameManager.game_over = True
            return
            
        # Nếu đã đến đích hoặc chưa có hướng đi
        if (self.x == self.run_pos["X"] and self.y == self.run_pos["Y"]) or self.go == 0:
            run_key = graph.find_next_step(key_mummy, key_player)
            if run_key is not None:
                new_pos = get_pos(run_key)
                
                # Kiểm tra xem vị trí mới có hợp lệ không
                temp_rect = pygame.Rect(new_pos["X"], new_pos["Y"], self.rect.width, self.rect.height)
                valid_move = True
                for wall in GameManager.wall_list:
                    if wall.rect.colliderect(temp_rect):
                        valid_move = False
                        break
                
                if valid_move:
                    self.run_pos = new_pos
                else:
                    # Nếu đường đi bị chặn, tìm đường khác
                    self.find_alternative_path(key_mummy, key_player)
        
        # Xác định hướng di chuyển
        dx = self.run_pos["X"] - self.x
        dy = self.run_pos["Y"] - self.y
        
        move_left = move_right = move_up = move_down = False
        
        if abs(dx) > abs(dy):  # Ưu tiên di chuyển ngang
            if dx > 0:
                move_right = True
            else:
                move_left = True
        else:  # Ưu tiên di chuyển dọc
            if dy > 0:
                move_down = True
            else:
                move_up = True
        
        self.update(move_left, move_right, move_up, move_down)

    def find_alternative_path(self, current_key, target_key):
        """Tìm đường đi thay thế khi đường chính bị chặn"""
        neighbors = graph.adjacency_list.get(current_key, [])
        for neighbor in neighbors:
            neighbor_pos = get_pos(neighbor)
            temp_rect = pygame.Rect(neighbor_pos["X"], neighbor_pos["Y"], self.rect.width, self.rect.height)
            
            # Kiểm tra va chạm với tường
            valid = True
            for wall in GameManager.wall_list:
                if wall.rect.colliderect(temp_rect):
                    valid = False
                    break
            
            if valid:
                self.run_pos = neighbor_pos
                return
        
        # Nếu không tìm được đường nào hợp lệ, đứng yên
        self.run_pos = {"X": self.x, "Y": self.y}
                    

#? VÒNG LẶP GAME
running = True

player = Player()
mummy = Mummy()

# wall_surface = pygame.Surface((WALL_WIDTH, WALL_HEIGHT))
#wall_surface2 = pygame.Surface((WALL_WIDTH2, WALL_HEIGHT2))

# win_surface = pygame.Surface((100, 100))

wall_hori = Wall(26, BROWN , "horizontal")
wall_verti = Wall(20, BROWN , "vertical")
wall_verti2 = Wall(16, BROWN , "vertical")

# Đưa các tường vào danh sách wall_list
GameManager.wall_list = [wall_hori, wall_verti, wall_verti2 ]

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
            
        # Xử lý click chuột để chơi lại
        if event.type == MOUSEBUTTONDOWN and GameManager.game_over:
            if event.button == 1:  # Nhấn chuột trái
                GameManager.reset_game(player, mummy)
            
    #? CLEAR WINDOW
    DISPLAY.fill((0, 0, 0, 0))
    
    # Setup map 
    DISPLAY.blit(MAP_SURFACE, (0, 0))

        # Vẽ cổng chiến thắng (gate)
    WIN_IMG = pygame.transform.scale(WIN_IMG, (100, 100))  # Kích thước cổng
    DISPLAY.blit(WIN_IMG, (WIN_POS['X'], WIN_POS['Y'] ))  # Vị trí cổng trên bản đồ
        
    # # Setup wall    
    # wall_surface.fill(RED)
    # DISPLAY.blit(wall_surface, (WALL_POS['X'], WALL_POS['Y']))
    wall_hori.draw("horizontal")
    wall_verti.draw("vertical")
    wall_verti2.draw("vertical")

    
    # # Setup ô chiến thắng
    # win_surface.fill((0, 255, 0))
    # DISPLAY.blit(win_surface, (WIN_POS['X'], WIN_POS['Y']))
    
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
            
            #  nhấn để chơi lại
            font = pygame.font.SysFont('Arial', 30)
            restart_text = font.render("CLICK MOUSE TO TRY AGAIN", True, (255, 255, 255))
            restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH // 2, 350))
            lose_board_surface.blit(restart_text, restart_rect)            
            
            DISPLAY.blit(lose_board_surface, (30, 100))
            

        else:  # Load thông tin thắng game: 
            
            win_message = pygame.transform.scale(pygame.image.load("./assets/win_text.png"), (591, 282))
            DISPLAY.blit(win_message, (0, 150))
            
            
        # Vẽ hình ảnh cổng chiến thắng tại vị trí WIN_POS
            WIN_IMG = pygame.transform.scale(WIN_IMG, (100, 100))  # Kích thước cổng
            DISPLAY.blit(WIN_IMG, (WIN_POS['X'], WIN_POS['Y']))  # Vị trí cổng trên bản đồ
    
    #? CẬP NHẬT TRẠNG THÁI GAME
    pygame.display.update()
    pygame.time.Clock().tick(60)
    

pygame.quit()