import pygame

from .state import State
from .generate import MazeGenerator
from .animations import Animator
from .maze import Maze

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
    GRAY,
    HEADER_HEIGHT,
    BLUE_2,
    WHITE,
    WIDTH,
    HEIGHT,
    FPS,
    YELLOW,
    START,
    GOAL
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

# Generate maze button
generate_btn = Button(
    "Generate Maze", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False,
    surface=None,
)
generate_btn.rect.centery = top.centery
generate_btn.rect.left = 200

generate_menu = Menu(
    surface=None,
    button=generate_btn,
    children=[
        Button(
            surface=None,
            text="Recursive Division",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Prim's Algorithm",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Randomised DFS",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Basic Random Maze",
            x=generate_btn.rect.x - 40,
            y=generate_btn.rect.y + generate_btn.height * 2,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)

# Button instance for Clear button
clear_btn = Button(
    "Clear Walls", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False,
    surface=None,
)
clear_btn.rect.centery = top.centery
clear_btn.rect.right = WIDTH - 20

# Controls info
control_btn = Button(
    "Controls", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False,
    surface=None,
)
control_btn.rect.centery = top.centery
control_btn.rect.right = clear_btn.rect.left - 20


def initialize(window):
    """Initialize game mode by setting the surfaces"""
    # Set window as the surface for all UI elements
    title.surface = window
    back_btn.surface = window
    generate_btn.surface = window
    for child in generate_menu.children:
        child.surface = window
    generate_menu.surface = window
    clear_btn.surface = window
    control_btn.surface = window


def draw(window, state, maze):
    """Draw game mode interface"""
    # Fill white, draw top background and title text
    window.fill(WHITE)
    pygame.draw.rect(window, DARK_BLUE, top)
    title.draw()
    back_btn.draw()

    # Draw maze legend
    texts = {
        "Start Node": WHITE,
        "Target Node": WHITE,
        "Wall Node": DARK,
    }

    x = 50
    y = top.bottom + 20
    for text in texts:
        # Rectangle (Symbol)
        pygame.draw.rect(window, texts[text], (x, y, 30, 30))
        pygame.draw.rect(window, GRAY, (x, y, 30, 30), width=1)

        # Text (Meaning)
        text_surf = FONT_18.render(text, True, DARK)
        text_rect = text_surf.get_rect()
        text_rect.centery = y + 30 // 2

        window.blit(text_surf, (x + 30 + 10, text_rect.y))

        # Formating
        if text == "Wall Node":
            y += text_rect.height + 30  # Changed from get_height() to height
        else:
            x += 30 + 10 + text_surf.get_width() + 75

        # Draw images for start and target node
        if text == "Start Node":
            image_rect = START.get_rect(center=(65, top.bottom + 35))
            window.blit(START, image_rect)
        elif text == "Target Node":
            image_rect = GOAL.get_rect(center=(65, top.bottom + 35))
            window.blit(GOAL, image_rect)

    # Draw state labels
    state.label.draw()
    
    # Draw control instructions
    if state.show_controls:
        control_text = FONT_18.render("Use WASD or Arrow Keys to move", True, DARK)
        control_rect = control_text.get_rect()
        control_rect.center = (WIDTH // 2, top.bottom + 70)
        window.blit(control_text, control_rect)

    # Draw the maze
    maze.draw()

    # Handle buttons
    if control_btn.draw():
        state.show_controls = not state.show_controls
        state.need_update = True

    if clear_btn.draw() and not maze.animator.animating:
        maze.clear_board()
        state.done_visualising = False
        state.need_update = True

    if (generate_menu.draw() or generate_menu.clicked) \
            and not maze.animator.animating:
        state.overlay = True

        if generate_menu.selected:
            maze.clear_board()

            def callback():
                state.overlay = False
                state.need_update = True

            maze.generate_maze(
                algorithm=generate_menu.selected.text,
                after_generation=callback
            )

            algorithm = generate_menu.selected.text

            if "Random" in algorithm:
                new_text = "Generating maze randomly"
            else:
                new_text = f"Generating maze using {algorithm}"

            state.label = Label(
                new_text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False,
                surface=window,
            )
            state.label.rect.bottom = HEADER_HEIGHT - 10


def run_game_mode(window, state, maze, animator):
    """Run the game mode loop"""
    # Initialize UI elements with the window surface
    initialize(window)

    # Set initial UI state
    state.player_mode = True
    state.need_update = True
    state.show_controls = True  # Initially show controls
    state.label = Label(
        "Player Mode: Use WASD or Arrow Keys to move", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 10
    
    # Clear any visited cells
    maze.clear_visited()
    
    # Indicate when user clicks back button
    exit_to_menu = False
    
    # Variables to control movement speed
    move_delay = 100  # milliseconds between moves
    last_move_time = 0
    
    # Main loop
    while not exit_to_menu:
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
        
        # Check if we should exit to menu
        if exit_to_menu:
            break
        
        # Update game display
        if state.need_update:
            draw(window, state, maze)
            state.need_update = False
        
        # Handle player movement with delay to control speed
        current_time = pygame.time.get_ticks()
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
                    
                    # Check win condition
                    if new_pos_tuple == maze.goal:
                        state.label = Label(
                            "You reached the goal! Press any key to reset.",
                            "center", 0,
                            background_color=pygame.Color(*WHITE),
                            foreground_color=pygame.Color(*DARK),
                            padding=6, font_size=20, outline=False,
                            surface=window,
                        )
                        state.label.rect.bottom = HEADER_HEIGHT - 10
                        
                        # Wait for a key press to reset
                        reset_game = False
                        while not reset_game and not exit_to_menu:
                            for event in pygame.event.get():
                                if event.type == pygame.QUIT:
                                    pygame.quit()
                                    return None
                                if event.type == pygame.KEYDOWN:
                                    maze.reset_player_position()
                                    state.label = Label(
                                        "Player Mode: Use WASD or Arrow Keys to move", "center", 0,
                                        background_color=pygame.Color(*WHITE),
                                        foreground_color=pygame.Color(*DARK),
                                        padding=6, font_size=20, outline=False,
                                        surface=window,
                                    )
                                    state.label.rect.bottom = HEADER_HEIGHT - 10
                                    state.need_update = True
                                    reset_game = True
                                    
                                if event.type == pygame.MOUSEBUTTONDOWN:
                                    mouse_pos = pygame.mouse.get_pos()
                                    # Check for back button click during win screen
                                    if back_btn.rect.collidepoint(mouse_pos):
                                        exit_to_menu = True
                                        reset_game = True
                                        break
                            
                            # Keep updating display while waiting for reset
                            if not reset_game:
                                draw(window, state, maze)
                                pygame.display.update()
                                CLOCK.tick(FPS)

        # Update display
        pygame.display.update()
        CLOCK.tick(FPS)
    
    # Return to menu when exit_to_menu is True
    return "menu"