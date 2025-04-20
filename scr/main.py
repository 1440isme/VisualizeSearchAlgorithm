import sys
import pygame

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
    WHITE,
    WIDTH,
    HEIGHT,
    FPS
)

# Initialize PyGame
pygame.init()

# Set up window
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT), pygame.HWACCEL)
pygame.display.set_caption("Pathfinding Visualizer")

# Main menu buttons
visualize_mode_btn = Button(
    "Visualization Mode", "center", HEIGHT // 2 - 40,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=10, font_size=24, outline=True,
    surface=WINDOW,
)

game_mode_btn = Button(
    "Game Mode", "center", HEIGHT // 2 + 40,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=10, font_size=24, outline=True,
    surface=WINDOW,
)


def show_main_menu():
    """Display the main menu with options for Visualization Mode and Game Mode"""
    WINDOW.fill(DARK_BLUE)
    
    # Draw title
    menu_title = Label(
        "Maze Explorer", "center", HEIGHT // 4,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=10, font_size=36, bold=True, outline=False,
        surface=WINDOW,
    )
    menu_title.draw()
    
    # Draw buttons
    visualize_mode_btn.draw()
    game_mode_btn.draw()
    
    # Add a subtitle/description
    subtitle = Label(
        "Choose a mode to continue", "center", HEIGHT // 2 + 100,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=18, outline=False,
        surface=WINDOW,
    )
    subtitle.draw()
    
    pygame.display.update()


def main() -> None:
    """Start here"""
    # Initialize
    state = State()
    maze = Maze(surface=WINDOW)
    animator = Animator(surface=WINDOW, maze=maze)
    maze_generator = MazeGenerator(animator=animator)
    maze.animator = animator
    maze.generator = maze_generator
    
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
            # Run visualization mode
            result = run_visualize_mode(WINDOW, state, maze, animator)
            current_mode = result if result else "menu"
            
        elif current_mode == "game":
            # Run game mode
            result = run_game_mode(WINDOW, state, maze, animator)
            current_mode = result if result else "menu"
        
        # Update
        pygame.display.update()
        CLOCK.tick(FPS)
