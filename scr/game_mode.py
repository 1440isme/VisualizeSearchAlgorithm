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
    ACCENT_ERROR,
    GREEN
    
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

# Add a new button for auto solving
auto_solve_btn = Button(
    "Auto Solve", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False,
    surface=None,
)
auto_solve_btn.rect.centery = top.centery
auto_solve_btn.rect.left = challenging_map_btn.rect.right + 20

# Create level manager
level_manager = LevelManager()

def initialize(window):
    """Initialize game mode by setting the surfaces"""
    # Set window as the surface for all UI elements
    title.surface = window
    back_btn.surface = window
    challenging_map_btn.surface = window
    auto_solve_btn.surface = window  # Add the new button



def draw(window, state, maze):
    """Draw game mode interface"""
    # Fill white, draw top background and title text
    window.fill(WHITE)
    pygame.draw.rect(window, DARK_BLUE, top)
    title.draw()
    back_btn.draw()
    challenging_map_btn.draw()  # Just draw the button, don't handle click here
    auto_solve_btn.draw()  # Just draw the button, don't handle click here

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
    
    # Draw the solution path if it exists AND we're not generating a new map
    if hasattr(state, 'solution_path') and state.showing_solution and state.solution_path and not state.overlay:
        # Lọc ra các tọa độ hợp lệ từ solution_path
        valid_path = []
        for cell in state.solution_path:
            # Kiểm tra xem cell có nằm trong kích thước mê cung không
            if 0 <= cell[0] < maze.height and 0 <= cell[1] < maze.width:
                valid_path.append(cell)
            else:
                print(f"Warning: Invalid cell in solution path: {cell}")
        
        # Cập nhật solution_path với chỉ các tọa độ hợp lệ
        state.solution_path = valid_path
        
        # Vẽ đường đi theo cách của visualize mode
        for cell in state.solution_path:
            # Skip drawing on START/GOAL
            if cell != maze.start and cell != maze.goal:
                # Đánh dấu ô là đường đi với "*"
                row, col = cell
                maze.set_cell((row, col), "*")
        
        # Đảm bảo START và GOAL được vẽ đúng
        maze.set_cell(maze.start, "A", forced=True)
        maze.set_cell(maze.goal, "B", forced=True)
    
    # Xoay và vẽ hình ảnh START theo hướng hiện tại
    from .constants import START, CELL_SIZE
    
    # Lấy vị trí hiện tại của người chơi (START)
    start_row, start_col = maze.start
    start_x, start_y = maze.coords[start_row][start_col]
    
    # Vẽ một hình chữ nhật màu nền lên ô START trước khi vẽ hình tam giác
    start_row, start_col = maze.start
    start_x, start_y = maze.coords[start_row][start_col]

    # Vẽ một hình chữ nhật với màu nền tương tự ô trống để "xóa" hình ảnh gốc
    # Lấy màu nền từ cell trắng
    pygame.draw.rect(window, WHITE, (start_x, start_y, CELL_SIZE, CELL_SIZE))

    # Vẽ đường viền của ô (nếu cần)
    pygame.draw.rect(window, DARK, (start_x, start_y, CELL_SIZE, CELL_SIZE), 1)

    # Sau đó vẽ hình ảnh đã xoay
    rotated_start = pygame.transform.rotate(START, state.player_direction)
    rect = rotated_start.get_rect(center=(start_x + CELL_SIZE//2, start_y + CELL_SIZE//2))
    window.blit(rotated_start, rect)
    
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
    wait_label = FONT_BOLD_20.render(waiting_text, True, ACCENT_ERROR)
    wait_rect = wait_label.get_rect(center=(WIDTH//2, HEIGHT//2-50))
    window.blit(wait_label, wait_rect)
    pygame.display.update()

    # Define callback after maze generation
    def after_generation():
        # Reset solution path
        if hasattr(state, 'solution_path'):
            state.solution_path = []
            state.showing_solution = False

        # Mark level as loaded
        state.level_loaded = True
        state.overlay = False
        state.need_update = True

        # Đặt start và goal ngẫu nhiên
        randomize_start_goal(maze)
        
        # Update wall positions after generating maze and placing start/goal
        maze.update_wall_positions()

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
    state.game_completed = False  # Add this flag
    state.label = Label(
        "Player Mode: Use WASD or Arrow Keys to move", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 30
    
    # Thêm hướng di chuyển ban đầu (0 = phải, 90 = lên, 180 = trái, 270 = xuống)
    state.player_direction = 0  # Mặc định hướng sang phải
    
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
        
        # Update timer if level has time limit - Di chuyển ra ngoài phần xử lý di chuyển
        current_level = level_manager.get_current_level()
        if hasattr(state, 'time_remaining') and state.time_remaining is not None:
            elapsed = (current_time - state.level_start_time) / 1000  # Convert to seconds
            state.time_remaining = current_level["time_limit"] - elapsed
            state.need_update = True  # Thêm dòng này để cập nhật hiển thị liên tục
            
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
                    
                    # Đặt start và goal ngẫu nhiên TRƯỚC khi tạo map
                    randomize_start_goal(maze)
                    
                    # Generate the challenging map immediately
                    def callback():
                        # Reset solution path if exists
                        if hasattr(state, 'solution_path'):
                            state.solution_path = []
                            state.showing_solution = False
                        
                        # Reset thời gian của level nếu level có giới hạn thời gian
                        current_level = level_manager.get_current_level()
                        if current_level["time_limit"] > 0:
                            state.time_remaining = current_level["time_limit"]
                            state.level_start_time = pygame.time.get_ticks()
                        
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
                
                # Handle auto solve button click
                if auto_solve_btn.rect.collidepoint(mouse_pos) and not maze.animator.animating:
                    print("Auto Solve button clicked!")
                    
                    # Find the best algorithm for shortest path
                    # Breadth First Search guarantees shortest path in unweighted graphs
                    solution = maze.solve("Breadth First Search")
                    
                    # Store the solution path in the state for visualization
                    state.solution_path = solution.path
                    
                    # Set a flag to indicate that the solution is being displayed
                    state.showing_solution = True
                    
                    # Update the label
                    state.label = Label(
                        "Auto Solve: Follow the yellow path!", "center", 0,
                        background_color=pygame.Color(*WHITE),
                        foreground_color=pygame.Color(*DARK),
                        padding=6, font_size=20, outline=False,
                        surface=window,
                    )
                    state.label.rect.bottom = HEADER_HEIGHT - 30
                    
                    # Đánh dấu ô trên đường đi với "*"
                    for cell in state.solution_path:
                        if cell != maze.start and cell != maze.goal:
                            row, col = cell
                            maze.set_cell((row, col), "*")
                    
                    # Đảm bảo START và GOAL được vẽ đúng
                    maze.set_cell(maze.start, "A", forced=True)
                    maze.set_cell(maze.goal, "B", forced=True)
                    
                    # Cập nhật và hiển thị màn hình ngay lập tức
                    state.need_update = True
                    draw(window, state, maze)
                    pygame.display.update()
        
        # Check if we should exit to menu
        if exit_to_menu:
            break
        
        # Update game display
        if state.need_update:
            draw(window, state, maze)
            state.need_update = False
        
        # Handle player movement with delay to control speed
        if current_time - last_move_time >= move_delay and not getattr(state, 'game_completed', False):
            keys = pygame.key.get_pressed()
            current_pos = maze.start  # Current player position is the start point
            new_pos = list(current_pos)
            moved = False

            # Move with WASD or arrow keys
            if keys[pygame.K_w] or keys[pygame.K_UP]:
                new_pos[0] -= 1  # Up
                state.player_direction = 90  # Hướng lên
                moved = True
            elif keys[pygame.K_s] or keys[pygame.K_DOWN]:
                new_pos[0] += 1  # Down
                state.player_direction = 270  # Hướng xuống
                moved = True
            elif keys[pygame.K_a] or keys[pygame.K_LEFT]:
                new_pos[1] -= 1  # Left
                state.player_direction = 180  # Hướng trái
                moved = True
            elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
                new_pos[1] += 1  # Right
                state.player_direction = 0  # Hướng phải
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
                    
                    # Update in the movement handling section, after maze.move_player()
                    if hasattr(state, 'solution_path') and state.showing_solution:
                        # Remove the position from solution path if player has moved there
                        if new_pos_tuple in state.solution_path:
                            # Đánh dấu ô đã đi qua bằng cách đổi nó về ô trống "1"
                            maze.set_cell(new_pos_tuple, "1")
                            # Keep track in solution_path too for consistency
                            state.solution_path.remove(new_pos_tuple)
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
                                        # Đặt cờ để khóa di chuyển
                                        state.game_completed = True
                                        
                                        # Hiển thị thông báo chúc mừng
                                        state.label = Label(
                                            "Congratulations! You completed all levels!", "center", 0,
                                            background_color=pygame.Color(*WHITE),
                                            foreground_color=pygame.Color(*DARK),
                                            padding=6, font_size=20, outline=False,
                                            surface=window,
                                        )
                                        state.label.rect.bottom = HEADER_HEIGHT - 30
                                        
                                        # Thêm hướng dẫn quay lại level 1
                                        restart_text = FONT_BOLD_20.render("Press SPACE to restart from Level 1", True, BLUE)
                                        restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
                                        window.blit(restart_text, restart_rect)
                                        pygame.display.update()
                                        
                                        # Chờ người chơi nhấn SPACE để quay lại level 1
                                        waiting_for_restart = True
                                        while waiting_for_restart:
                                            for event in pygame.event.get():
                                                if event.type == pygame.QUIT:
                                                    pygame.quit()
                                                    return None
                                                if event.type == pygame.KEYDOWN:
                                                    if event.key == pygame.K_SPACE:
                                                        # Reset về level 1
                                                        level_manager.set_current_level(1)
                                                        load_level(window, state, maze)
                                                        state.game_completed = False  # Bỏ khóa di chuyển
                                                        waiting_for_restart = False
                                                        
                                                if event.type == pygame.MOUSEBUTTONDOWN:
                                                    mouse_pos = pygame.mouse.get_pos()
                                                    if back_btn.rect.collidepoint(mouse_pos):
                                                        exit_to_menu = True
                                                        waiting_for_restart = False
                                            
                                            # Tiếp tục cập nhật màn hình trong khi chờ
                                            draw(window, state, maze)
                                            pygame.display.update()
                                            CLOCK.tick(FPS)
                                    next_level = True
                                
                            if not next_level:
                                draw(window, state, maze)
                                pygame.display.update()
                                CLOCK.tick(FPS)

        # Update display
        pygame.display.update()
        CLOCK.tick(FPS)
    return 'menu'

# Thêm hàm để đặt start và goal ngẫu nhiên
def randomize_start_goal(maze):
    """Randomly place start and goal positions on the maze"""
    import random
    
    # Lấy các vị trí hợp lệ (các ô trống) trong mê cung
    valid_positions = []
    for row in range(maze.height):
        for col in range(maze.width):
            if maze.maze[row][col].value == "1":  # Ô trống
                valid_positions.append((row, col))
    
    # Đảm bảo có đủ ô trống để đặt start và goal
    if len(valid_positions) < 2:
        return False  # Không đủ ô trống
    
    # Chọn ngẫu nhiên vị trí start và goal
    # Đảm bảo khoảng cách giữa chúng đủ xa (ít nhất 1/2 kích thước mê cung)
    min_distance = ((maze.width ** 2 + maze.height ** 2) ** 0.5) / 2
    
    attempts = 100  # Giới hạn số lần thử để tránh vòng lặp vô hạn
    while attempts > 0:
        start_pos = random.choice(valid_positions)
        goal_pos = random.choice(valid_positions)
        
        # Tính khoảng cách Manhattan giữa start và goal
        distance = abs(start_pos[0] - goal_pos[0]) + abs(start_pos[1] - goal_pos[1])
        
        # Nếu khoảng cách đủ xa, sử dụng các vị trí này
        if distance >= min_distance and start_pos != goal_pos:
            # Cập nhật start và goal
            maze.set_cell(start_pos, "A", forced=True)
            maze.set_cell(goal_pos, "B", forced=True)
            
            # Cập nhật các thuộc tính internal
            maze.start = start_pos
            maze.goal = goal_pos
            return True
            
        attempts -= 1
    
    # Nếu không tìm được vị trí thích hợp sau nhiều lần thử
    # Chọn 2 vị trí ngẫu nhiên khác nhau
    remaining_attempts = 10
    while remaining_attempts > 0:
        start_pos = random.choice(valid_positions)
        goal_pos = random.choice(valid_positions)
        
        if start_pos != goal_pos:
            # Cập nhật start và goal
            maze.set_cell(start_pos, "A", forced=True)
            maze.set_cell(goal_pos, "B", forced=True)
            
            # Cập nhật các thuộc tính internal
            maze.start = start_pos
            maze.goal = goal_pos
            return True
            
        remaining_attempts -= 1
    
    return False  # Thất bại trong việc đặt start và goal


