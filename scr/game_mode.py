import pygame

from .state import State
from .generate import MazeGenerator
from .animations import Animator
from .maze import Maze
from .levels import LevelManager  # Import the LevelManager

from .widgets import (
    Button,
    Label,
    Menu,
)

from .constants import (
    BLUE,
    CLOCK,
    DARK,
    DARK_BLUE,
    FONT_18,
    FONT_BOLD_20,
    GRAY,
    HEADER_HEIGHT,
    BLUE_2,
    WHITE,
    WIDTH,
    HEIGHT,
    FPS,
    YELLOW,
    START,
    GOAL,
)

# Top bar
top = pygame.Rect(0, 0, WIDTH, 80)

# Title
title = Label(
    "Maze Game", 20, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, bold=True,
    surface=None,
)
title.rect.centery = top.centery

# Button instance for returning to main menu
back_btn = Button(
    "Back to Menu", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=18, outline=False,
    surface=None,
)
back_btn.rect.centery = top.centery
back_btn.rect.x = 20


# Add a new button for challenging map generation
challenging_map_btn = Button(
    "Challenging Map", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False,
    surface=None,
)
challenging_map_btn.rect.centery = top.centery
challenging_map_btn.rect.left = back_btn.rect.right + 20

# Create level manager
level_manager = LevelManager()

def initialize(window):
    """Initialize game mode by setting the surfaces"""
    # Set window as the surface for all UI elements
    title.surface = window
    back_btn.surface = window
    challenging_map_btn.surface = window



def draw(window, state, maze):
    """Draw game mode interface"""
    # Fill white, draw top background and title text
    window.fill(WHITE)
    pygame.draw.rect(window, DARK_BLUE, top)
    title.draw()
    back_btn.draw()
    challenging_map_btn.draw()  # Just draw the button, don't handle click here

    x = 50
    y = top.bottom + 20

    # Draw level info
    current_level = level_manager.get_current_level()
    level_text = f"Level {current_level['id']}: {current_level['name']}"
    level_surf = FONT_BOLD_20.render(level_text, True, DARK)
    level_rect = level_surf.get_rect(topright=(WIDTH - 50, top.bottom + 20))
    window.blit(level_surf, level_rect)

    # Draw time remaining if level has time limit
    if hasattr(state, 'time_remaining') and state.time_remaining is not None:
        minutes = int(state.time_remaining // 60)
        seconds = int(state.time_remaining % 60)
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        time_surf = FONT_BOLD_20.render(time_text, True, DARK)
        time_rect = time_surf.get_rect(topright=(WIDTH - 50, top.bottom + 50))
        window.blit(time_surf, time_rect)

    # Draw state labels
    state.label.draw()
    
    # Draw control instructions
    if state.show_controls:
        control_text = FONT_18.render("Use WASD or Arrow Keys to move", True, DARK)
        control_rect = control_text.get_rect()
        control_rect.center = (WIDTH // 2, top.bottom + 50)
        window.blit(control_text, control_rect)

    # Draw the maze
    maze.draw()
    
    # Draw level selection menu if active
    if state.show_level_select:
        draw_level_select(window, state, maze)


def draw_level_select(window, state, maze):
    """Draw the level selection screen"""
    # Draw semi-transparent overlay
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 150))
    window.blit(overlay, (0, 0))
    
    # Draw level selection panel
    panel_width = 600
    panel_height = 400
    panel_x = (WIDTH - panel_width) // 2
    panel_y = (HEIGHT - panel_height) // 2
    
    pygame.draw.rect(window, WHITE, (panel_x, panel_y, panel_width, panel_height))
    pygame.draw.rect(window, DARK_BLUE, (panel_x, panel_y, panel_width, panel_height), 2)
    
    # Draw title
    title_surf = FONT_BOLD_20.render("Level Selection", True, DARK)
    title_rect = title_surf.get_rect(center=(WIDTH // 2, panel_y + 30))
    window.blit(title_surf, title_rect)
    
    # Draw close button
    close_btn = Button(
        "X", panel_x + panel_width - 30, panel_y + 10,
        background_color=pygame.Color(*DARK_BLUE),
        foreground_color=pygame.Color(*WHITE),
        padding=6, font_size=18, outline=False,
        surface=window
    )
    
    if close_btn.draw():
        state.show_level_select = False
        state.need_update = True
    
    # Draw level buttons
    btn_width = 120
    btn_height = 80
    btn_margin = 20
    btn_per_row = 3
    
    for i, level in enumerate(level_manager.levels):
        row = i // btn_per_row
        col = i % btn_per_row
        
        btn_x = panel_x + (col * (btn_width + btn_margin)) + btn_margin
        btn_y = panel_y + 70 + (row * (btn_height + btn_margin))
        
        # Determine background color based on level status
        if level["id"] == level_manager.current_level_id:
            bg_color = BLUE
        elif level["unlocked"]:
            bg_color = DARK_BLUE
        else:
            bg_color = GRAY  # Locked level
        
        level_btn = Button(
            f"Level {level['id']}", btn_x, btn_y,
            width=btn_width,
            height=btn_height,
            background_color=pygame.Color(*bg_color),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=18, outline=False,
            surface=window
        )
        
        # Add level name below level number
        if level_btn.draw() and level["unlocked"]:
            level_manager.set_current_level(level["id"])
            state.show_level_select = False
            load_level(window, state, maze)
            
        # Draw level name
        name_surf = FONT_18.render(level["name"], True, WHITE)
        name_rect = name_surf.get_rect(center=(btn_x + btn_width // 2, btn_y + btn_height // 2 + 10))
        window.blit(name_surf, name_rect)
        
        # Draw lock icon for locked levels
        if not level["unlocked"]:
            lock_text = FONT_BOLD_20.render("🔒", True, WHITE)
            lock_rect = lock_text.get_rect(center=(btn_x + btn_width // 2, btn_y + btn_height // 2 - 10))
            window.blit(lock_text, lock_rect)


def load_level(window, state, maze):
    """Load the current level"""
    # Get current level data
    current_level = level_manager.get_current_level()

    # Reset player position to ensure they're not stuck
    maze.reset_player_position()

    # Set label for level loading
    state.label = Label(
        f"Loading Level {current_level['id']}: {current_level['name']}", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 30

    # Set time limit
    if current_level["time_limit"] > 0:
        state.time_remaining = current_level["time_limit"]
        state.level_start_time = pygame.time.get_ticks()
    else:
        state.time_remaining = None

    # Resize maze according to the level's difficulty
    width, height = level_manager.get_maze_size_for_current_level()
    maze.resize(width, height)

    # Mark the level as not loaded yet
    state.level_loaded = False

    # Set timeout to ensure we don't hang if callback isn't called after 2 seconds
    level_timeout = pygame.time.get_ticks() + 2000

    # Show loading message
    waiting_text = f"Loading Level {current_level['id']}..."
    wait_label = FONT_BOLD_20.render(waiting_text, True, DARK)
    wait_rect = wait_label.get_rect(center=(WIDTH//2, HEIGHT//2-50))
    window.blit(wait_label, wait_rect)
    pygame.display.update()

    # Define callback after maze generation
    def after_generation():
        # Mark level as loaded
        state.level_loaded = True
        state.overlay = False
        state.need_update = True

        # Update UI label
        state.label = Label(
            f"Level {current_level['id']}: {current_level['name']} - Find the exit!", "center", 0,
            background_color=pygame.Color(*WHITE),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=20, outline=False,
            surface=window,
        )
        state.label.rect.bottom = HEADER_HEIGHT - 30

    # Set overlay during maze generation
    state.overlay = True

    # Use create_standard_maze for consistent maze generation
    maze.create_standard_maze(
        algorithm="Randomised DFS",  # Force DFS algorithm for consistent maze generation
        after_generation=after_generation
    )

    # Update UI during generation
    new_text = "Generating maze for level using Randomised DFS"
    state.label = Label(
        new_text, "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 30

    # Ensure we don't hang if callback isn't triggered
    while not state.level_loaded and pygame.time.get_ticks() < level_timeout:
        pygame.display.update()
        pygame.time.wait(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

    # If level still not loaded after timeout, force completion
    if not state.level_loaded:
        print(f"Level loading timeout - forcing completion for Level {current_level['id']}")
        after_generation()

    # Update state
    state.need_update = True


def run_game_mode(window, state, maze, animator):
    """Run the game mode loop"""
    # Initialize UI elements with the window surface
    initialize(window)

    # Set initial UI state
    state.player_mode = True
    state.need_update = True
    state.show_controls = True  # Initially show controls
    state.show_level_select = False  # Level selection screen is initially hidden
    state.label = Label(
        "Player Mode: Use WASD or Arrow Keys to move", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 30
    
    # Load the first level
    load_level(window, state, maze)
    
    # Clear any visited cells
    maze.clear_visited()
    
    # Indicate when user clicks back button
    exit_to_menu = False
    
    # Variables to control movement speed
    move_delay = 100  # milliseconds between moves
    last_move_time = 0
    
    # Main loop
    while not exit_to_menu:
        current_time = pygame.time.get_ticks()
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check for back button click
                if back_btn.rect.collidepoint(mouse_pos):
                    exit_to_menu = True
                    break

                # Handle challenging map button click - improved version
                if challenging_map_btn.rect.collidepoint(mouse_pos) and not maze.animator.animating:
                    print("Challenging map button clicked!")
                    
                    # Generate the challenging map immediately
                    def callback():
                        # Make sure we reset all relevant state flags
                        state.overlay = False
                        state.need_update = True
                        # Update wall positions after generation
                        maze.update_wall_positions()
                        
                        # Show a brief confirmation message
                        state.label = Label(
                            "Challenging map generated!", "center", 0,
                            background_color=pygame.Color(*WHITE),
                            foreground_color=pygame.Color(*DARK),
                            padding=6, font_size=20, outline=False,
                            surface=window,
                        )
                        state.label.rect.bottom = HEADER_HEIGHT - 30
                    
                    # Generate the map
                    maze.generate_challenging_map(after_generation=callback)
        
        # Update timer if level has time limit
        current_level = level_manager.get_current_level()
        if hasattr(state, 'time_remaining') and state.time_remaining is not None:
            elapsed = (current_time - state.level_start_time) / 1000  # Convert to seconds
            state.time_remaining = current_level["time_limit"] - elapsed
            
            # Check for time out
            if state.time_remaining <= 0:
                state.time_remaining = 0
                # Show game over message
                state.label = Label(
                    "Time's up! Press any key to try again.", "center", 0,
                    background_color=pygame.Color(*WHITE),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=window,
                )
                state.label.rect.bottom = HEADER_HEIGHT - 30
                state.need_update = True
                
                # Wait for key press to restart level
                restart_level = False
                while not restart_level and not exit_to_menu:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            return None
                        if event.type == pygame.KEYDOWN:
                            # Reload the current level
                            load_level(window, state, maze)
                            restart_level = True
                        
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            mouse_pos = pygame.mouse.get_pos()
                            if back_btn.rect.collidepoint(mouse_pos):
                                exit_to_menu = True
                                restart_level = True
                                break
                    
                    # Keep updating display while waiting for restart
                    if not restart_level:
                        draw(window, state, maze)
                        pygame.display.update()
                        CLOCK.tick(FPS)
        
        # Check if we should exit to menu
        if exit_to_menu:
            break
        
        # Update game display
        if state.need_update:
            draw(window, state, maze)
            state.need_update = False
        
        # Handle player movement with delay to control speed
        if current_time - last_move_time >= move_delay:
            keys = pygame.key.get_pressed()
            current_pos = maze.start  # Current player position is the start point
            new_pos = list(current_pos)
            moved = False

            # Move with WASD or arrow keys
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                new_pos[0] -= 1  # Up
                moved = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                new_pos[0] += 1  # Down
                moved = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                new_pos[1] -= 1  # Left
                moved = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                new_pos[1] += 1  # Right
                moved = True

            # If a move key was pressed
            if moved:
                # Update last move time
                last_move_time = current_time
                
                # Ensure we have a proper tuple with exactly 2 integers
                new_pos_tuple = (new_pos[0], new_pos[1])

                # Check valid move and update position
                if maze.is_valid_move(new_pos_tuple):
                    maze.move_player(current_pos, new_pos_tuple)
                    state.need_update = True
                    
                    # Check win condition - player reached the goal
                    if new_pos_tuple == maze.goal:
                        current_level = level_manager.get_current_level()
                    
                        # Complete level
                        level_manager.complete_level(current_level["id"])
                    
                        # Create completion message
                        message = f"Level {current_level['id']} completed! Press SPACE to continue."
                            
                        state.label = Label(
                            message, "center", 0,
                            background_color=pygame.Color(*WHITE),
                            foreground_color=pygame.Color(*DARK),
                            padding=6, font_size=20, outline=False,
                            surface=window,
                        )
                        state.label.rect.bottom = HEADER_HEIGHT - 30
                        state.need_update = True
                    
                        # Show unlock message if next level exists
                        if current_level["id"] < len(level_manager.levels):
                            next_level_id = current_level["id"] + 1
                            level_manager.complete_level(current_level['id'])
                            unlock_message = f"Level {next_level_id} unlocked!"
                            unlock_surf = FONT_BOLD_20.render(unlock_message, True, BLUE)
                            unlock_rect = unlock_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
                            window.blit(unlock_surf, unlock_rect)
                            pygame.display.update()
                    
                        # Wait for a key press to continue
                        next_level = False
                        while not next_level and not exit_to_menu:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    return None
                                if event.type == pygame.KEYDOWN:
                                    if current_level["id"] < len(level_manager.levels):
                                        level_manager.set_current_level(current_level["id"] + 1)
                                        load_level(window, state, maze)
                                    else:
                                        state.label = Label(
                                            "Congratulations! You completed all levels!", "center", 0,
                                            background_color=pygame.Color(*WHITE),
                                            foreground_color=pygame.Color(*DARK),
                                            padding=6, font_size=20, outline=False,
                                            surface=window,
                                        )
                                        state.label.rect.bottom = HEADER_HEIGHT - 30
                                    next_level = True
                                
                            if not next_level:
                                draw(window, state, maze)
                                pygame.display.update()
                                CLOCK.tick(FPS)

        # Update display
        pygame.display.update()
        CLOCK.tick(FPS)
    return 'menu'
