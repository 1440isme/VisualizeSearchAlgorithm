import sys
import pygame

pygame.font.init()
pygame.display.init()

# Màu sắc
BLACK = (0, 0, 0)
DARK = (11, 53, 71)

# Bảng màu hiện đại
# Màu chính
PRIMARY_DARK = (18, 30, 49)       # Xanh navy đậm - nền chính
PRIMARY_LIGHT = (240, 244, 248)   # Trắng ngà - nền sáng

# Màu nhấn
ACCENT_PRIMARY = (66, 133, 244)   # Xanh dương sáng - hành động chính
ACCENT_SUCCESS = (52, 168, 83)    # Xanh lá - thành công
ACCENT_WARNING = (251, 188, 5)    # Hổ phách - cảnh báo/đường đi
ACCENT_ERROR = (234, 67, 53)      # Đỏ - lỗi/chướng ngại vật
ACCENT_NEUTRAL = (154, 160, 166)  # Xám - thành phần trung tính

# Màu truyền thống (để tương thích ngược)
GREEN = (52, 168, 83)  # Thay đổi từ (26, 188, 157) sang màu hiện đại hơn
GREEN_2 = (104, 224, 185)
BLUE = (66, 133, 244)  # Thay đổi từ (100, 206, 228) sang màu hiện đại hơn
WHITE = (255, 255, 255)
YELLOW = (251, 188, 5)  # Thay đổi từ (255, 254, 106) sang màu ít chói hơn
GRAY = (154, 160, 166)  # Thay đổi từ (166, 222, 255) sang màu trung tính hơn
DARK_BLUE = (18, 30, 49)  # Thay đổi từ (52, 73, 94) sang màu hiện đại hơn
BLUE_2 = (81, 145, 228) 
DARK_BLUE_2 = (44, 67, 208)
PURPLE = (17, 104, 217)

# Màu trực quan hóa
VIZ_VISITED = (108, 142, 191)     # Xanh dương nhẹ cho các nút đã thăm
VIZ_PATH = (255, 213, 79)         # Vàng sáng cho đường đi
VIZ_WALL = (40, 53, 72)           # Xám đậm cho tường
VIZ_WEIGHT = (176, 190, 197)      # Xám nhạt cho nút có trọng số

# Kích thước cửa sổ
WINDOW_INFO = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = WINDOW_INFO.current_w, WINDOW_INFO.current_h
WIDTH = 1280 if SCREEN_WIDTH >= 1280 else SCREEN_WIDTH - 150
HEIGHT = 900 if SCREEN_HEIGHT >= 900 else SCREEN_HEIGHT - 150
HEADER_HEIGHT = 160  # Giảm chiều cao header để gọn gàng hơn

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

# Border radius cho các thành phần UI
BORDER_RADIUS = 8  # Bo tròn các góc

# Shadow parameters
SHADOW_OFFSET = 2
SHADOW_COLOR = (0, 0, 0, 40)  # RGBA với alpha=40 cho bóng mờ

# Các thông số animation
ANIMATION_SPEED = 200  # ms
HOVER_SCALE = 1.05  # Tỉ lệ phóng to khi hover
TRANSITION_SPEED = 150  # ms cho các hiệu ứng chuyển tiếp

# Load hình ảnh và chữ
WEIGHT = pygame.image.load("assets/images/weight.png")
START = pygame.image.load("assets/images/triangle.png")
GOAL = pygame.image.load("assets/images/circle.png")
FONT_14 = pygame.font.Font("assets/font/Montserrat-Regular.ttf", 14)
FONT_16 = pygame.font.Font("assets/font/Montserrat-Regular.ttf", 16)
FONT_18 = pygame.font.Font("assets/font/Montserrat-Regular.ttf", 18)
FONT_20 = pygame.font.Font("assets/font/Montserrat-Regular.ttf", 20)
FONT_24 = pygame.font.Font("assets/font/Montserrat-Regular.ttf", 24)
FONT_BOLD_18 = pygame.font.Font("assets/font/Montserrat-Bold.ttf", 18)
FONT_BOLD_20 = pygame.font.Font("assets/font/Montserrat-Bold.ttf", 20)
FONT_BOLD_24 = pygame.font.Font("assets/font/Montserrat-Bold.ttf", 24)

# Thông số animation
MIN_SIZE = 0.3 * CELL_SIZE
MAX_SIZE = 1.2 * CELL_SIZE
