import sys
import pygame
import math

from .state import State
from .maze import Maze
from .animations import Animator
from .generate import MazeGenerator
from .visualize_mode import run_visualize_mode
from .game_mode import run_game_mode

from .widgets import (
    Button,
    Label
)

from .constants import (
    CLOCK,
    DARK_BLUE,
    PRIMARY_DARK,
    PRIMARY_LIGHT,
    ACCENT_PRIMARY,
    ACCENT_SUCCESS,
    WHITE,
    WIDTH,
    HEIGHT,
    FPS,
    FONT_24,
    FONT_BOLD_24
)

# Initialize PyGame
pygame.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWACCEL)
pygame.display.set_caption("MAZE EXPLORER")

# Tạo nút menu chính với thiết kế hiện đại
visualize_mode_btn = Button(
    "Visualization Mode", "center", HEIGHT // 2 - 50,
    background_color=pygame.Color(*ACCENT_PRIMARY),
    foreground_color=pygame.Color(*WHITE),
    padding=20, font_size=24, bold=True,
    surface=WINDOW,
)

game_mode_btn = Button(
    "Game Mode", "center", HEIGHT // 2 + 50,
    background_color=pygame.Color(*ACCENT_SUCCESS),
    foreground_color=pygame.Color(*WHITE),
    padding=20, font_size=24, bold=True,
    surface=WINDOW,
)

# Thời gian bắt đầu cho animation
start_time = pygame.time.get_ticks()

def show_main_menu():
    """Hiển thị menu chính với animation và hiệu ứng hiện đại"""
    current_time = pygame.time.get_ticks()
    elapsed = current_time - start_time
    
    # Tạo hiệu ứng gradient động cho nền
    WINDOW.fill(PRIMARY_DARK)
    
    # Vẽ hiệu ứng sóng động
    for x in range(0, WIDTH, 20):
        for y in range(0, HEIGHT, 20):
            # Tạo hiệu ứng sóng động theo thời gian
            offset = math.sin((x + y) / 50 + elapsed / 1000) * 5
            size = 3 + offset
            
            # Điều chỉnh màu theo vị trí và thời gian
            hue = (x + y + elapsed / 30) % 100 / 100
            color_value = 50 + int(hue * 50)
            
            # Vẽ hình tròn tạo hiệu ứng sóng
            pygame.draw.circle(
                WINDOW, 
                (30, 50 + color_value, 90 + color_value), 
                (x, y), 
                max(1, size)
            )
    
    # Vẽ overlay mờ để làm nổi bật nội dung chính
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((18, 30, 49, 200))  # Semi-transparent overlay
    WINDOW.blit(overlay, (0, 0))
    
    # Vẽ tiêu đề với hiệu ứng pulse
    pulse = math.sin(elapsed / 500) * 0.1 + 1  # Dao động từ 0.9 đến 1.1
    title_font = pygame.font.Font("assets/font/Montserrat-Bold.ttf", int(60 * pulse))
    title_surface = title_font.render("MAZE EXPLORER", True, WHITE)
    title_rect = title_surface.get_rect(center=(WIDTH//2, HEIGHT//4))
    
    # Tạo hiệu ứng glow cho tiêu đề
    for offset in range(5, 0, -1):
        glow_surface = title_font.render("MAZE EXPLORER", True, (100, 150, 255, 100//offset))
        glow_rect = glow_surface.get_rect(center=(WIDTH//2 + offset//2, HEIGHT//4 + offset//2))
        WINDOW.blit(glow_surface, glow_rect)
    
    WINDOW.blit(title_surface, title_rect)
    
    # Vẽ subtitle với hiệu ứng fade in từ trái sang phải
    subtitle_text = "Maze Pathfinder Visualization - Maze Game"
    subtitle_font = pygame.font.Font("assets/font/Montserrat-Regular.ttf", 20)
    subtitle_full = subtitle_font.render(subtitle_text, True, WHITE)
    subtitle_width = subtitle_full.get_width()
    
    # Hiệu ứng fade-in
    visible_chars = min(len(subtitle_text), int(elapsed / 50)) 
    if visible_chars < len(subtitle_text):
        subtitle_text = subtitle_text[:visible_chars]
    
    subtitle_surface = subtitle_font.render(subtitle_text, True, WHITE)
    subtitle_rect = subtitle_surface.get_rect(center=(WIDTH//2, HEIGHT//4 + 70))
    WINDOW.blit(subtitle_surface, subtitle_rect)
    
    # Vẽ các nút
    visualize_mode_btn.draw()
    game_mode_btn.draw()
    
    # Vẽ thông tin phiên bản ở góc dưới
    version_label = Label(
        "v2.0 - Modern UI Edition", WIDTH - 20, HEIGHT - 30,
        background_color=pygame.Color(0, 0, 0, 0),  # Trong suốt
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=14, outline=False,
        surface=WINDOW,
    )
    version_label.rect.right = WIDTH - 20  # Canh phải
    version_label.draw()
    
    # Hiệu ứng highlight theo thời gian
    highlight_strength = (math.sin(elapsed / 1000) + 1) / 2  # 0-1
    highlight_color = (
        int(255 * highlight_strength), 
        int(255 * highlight_strength), 
        int(255 * highlight_strength), 
        int(50 * highlight_strength)
    )
    highlight = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    
    # Vẽ viền sáng dọc theo các cạnh màn hình
    edge_thickness = 2
    highlight.fill((0, 0, 0, 0))
    pygame.draw.rect(highlight, highlight_color, (0, 0, WIDTH, edge_thickness))
    pygame.draw.rect(highlight, highlight_color, (0, 0, edge_thickness, HEIGHT))
    pygame.draw.rect(highlight, highlight_color, (0, HEIGHT - edge_thickness, WIDTH, edge_thickness))
    pygame.draw.rect(highlight, highlight_color, (WIDTH - edge_thickness, 0, edge_thickness, HEIGHT))
    
    WINDOW.blit(highlight, (0, 0))
    
    pygame.display.update()


def main() -> None:
    """Start here"""
    # Initialize
    state = State()
    
    # Tạo maze riêng cho từng chế độ
    game_maze = Maze(surface=WINDOW)
    visual_maze = Maze(surface=WINDOW)
    
    # Tạo animator và generator cho mỗi maze
    game_animator = Animator(surface=WINDOW, maze=game_maze)
    visual_animator = Animator(surface=WINDOW, maze=visual_maze)
    
    game_generator = MazeGenerator(animator=game_animator)
    visual_generator = MazeGenerator(animator=visual_animator)
    
    # Thiết lập các tham chiếu cho mỗi maze
    game_maze.animator = game_animator
    game_maze.generator = game_generator
    
    visual_maze.animator = visual_animator
    visual_maze.generator = visual_generator
    
    # Start in menu mode
    current_mode = "menu"

    # Game loop
    running = True
    while running:
        if current_mode == "menu":
            # Show the main menu
            show_main_menu()
            
            # Handle menu events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check for visualization mode button click
                    if visualize_mode_btn.rect.collidepoint(mouse_pos):
                        current_mode = "visualize"
                        
                    # Check for game mode button click
                    elif game_mode_btn.rect.collidepoint(mouse_pos):
                        current_mode = "game"
        
        elif current_mode == "visualize":
            # Run visualization mode with its own maze
            result = run_visualize_mode(WINDOW, state, visual_maze, visual_animator)
            current_mode = result if result else "menu"
            
        elif current_mode == "game":
            # Run game mode with its own maze
            result = run_game_mode(WINDOW, state, game_maze, game_animator)
            current_mode = result if result else "menu"
        
        # Update
        pygame.display.update()
        CLOCK.tick(FPS)
