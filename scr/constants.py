import sys
import pygame

pygame.font.init()
pygame.display.init()

# Màu sắc
BLACK = (0, 0, 0)
DARK = (11, 53, 71)
GREEN = (26, 188, 157)
GREEN_2 = (104, 224, 185)
BLUE = (100, 206, 228)
WHITE = (255, 255, 255)
YELLOW = (255, 254, 106)
GRAY = (166, 222, 255)
DARK_BLUE = (52, 73, 94)
BLUE_2 = (81, 145, 228)
DARK_BLUE_2 = (44, 67, 208)
PURPLE = (17, 104, 217)

# Kích thước cửa sổ
WINDOW_INFO = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_INFO.current_w, WINDOW_INFO.current_h
WIDTH = 1280 if SCREEN_WIDTH >= 1280 else SCREEN_WIDTH - 150
HEIGHT = 900 if SCREEN_HEIGHT >= 900 else SCREEN_HEIGHT - 150
HEADER_HEIGHT = 200 # phần header UI phía trên mê cung.

# Thiết lập kích thước ô - (CELL_SIZE)

CELL_SIZE = 26 # mỗi ô mặc định 26px * 26px 
if len(sys.argv) > 1:
    arg = sys.argv[1]

    try:
        assert arg.startswith("--cell-size:") == True

        size = arg.split(":")[1]
        size = int(size)

        if size < 10:
            size = 10
        elif size > 90:
            size = 90

        CELL_SIZE = size
    except:
        print("\nInvalid command line arguments")
        print("USAGE: python3 run.pyw [ --cell-size:<int> ]")
        exit(1)

# Tính toán lại kích thước mê cung 
# Tính phần dư của chiều ngang
REMAINDER_W = WIDTH % CELL_SIZE
if REMAINDER_W == 0:
    REMAINDER_W = CELL_SIZE

# Tính phần cư của chiều cao (ko tính header)
REMAINDER_H = (HEIGHT - HEADER_HEIGHT) % CELL_SIZE
if REMAINDER_H == 0:
    REMAINDER_H = CELL_SIZE

MAZE_WIDTH = WIDTH - REMAINDER_W # chiều rộng mê cung (chia hết cho CELL_SIZE)
MAZE_HEIGHT = HEIGHT - HEADER_HEIGHT - REMAINDER_H #	chiều cao mê cung (bỏ phần header, chia hết CELL_SIZE)

# Thiết lập FPS - tốc độ chạy chương trình
FPS = 60
CLOCK = pygame.time.Clock()

# Load hình ảnh và chữ
WEIGHT = pygame.image.load("assets/images/weight.png")
START = pygame.image.load("assets/images/triangle.png")
GOAL = pygame.image.load("assets/images/circle.png")
FONT_14 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 14)
FONT_18 = pygame.font.Font("assets/fonts/Montserrat-Regular.ttf", 18)

# Thông số animation
MIN_SIZE = 0.3 * CELL_SIZE
MAX_SIZE = 1.2 * CELL_SIZE
