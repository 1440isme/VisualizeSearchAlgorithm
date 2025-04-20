import pygame

from .state import State
from .generate import MazeGenerator
from .animations import Animation, Animator, AnimatingNode
from .maze import Maze, WEIGHT

from .widgets import (
    Alignment,
    Button,
    Label,
    Menu,
    Orientation,
    Popup,
    Table,
    TableCell
)

from .constants import (
    BLUE,
    CELL_SIZE,
    CLOCK,
    DARK,
    DARK_BLUE,
    FONT_18,
    GRAY,
    GREEN,
    GREEN_2,
    HEADER_HEIGHT,
    BLUE_2,
    MIN_SIZE,
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
    "                       ", 20, 0,
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

# ? button for legends
legends_btn = Button(
    "?", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    padding=8, font_size=20, outline=False,
    surface=None,
)
legends_btn.rect.bottom = HEADER_HEIGHT - 10
legends_btn.rect.right = WIDTH - 20


# Algorithms list
algorithm_btn = Button(
    surface=None,
    text="Algorithms",
    x=title.width + 70,
    y=0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False
)
algorithm_btn.rect.centery = top.centery


algo_menu = Menu(
    surface=None,
    button=algorithm_btn,
    children=[
        Button(
            surface=None,
            text="A* Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Dijkstra's Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Greedy Best First Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Breadth First Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Depth First Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Uniform Cost Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Iterative Deepening DFS",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Iterative Deepening A*",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Beam Search",
            x=algorithm_btn.rect.x - 40,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)

speed_btn = Button(
    surface=None,
    text="Speed",
    x=algorithm_btn.rect.right + 40,
    y=0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False
)
speed_btn.rect.centery = top.centery
speed_btn.rect.y -= 15


speed_menu = Menu(
    surface=None,
    button=speed_btn,
    children=[
        Button(
            surface=None,
            text="Fast",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Medium",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Slow",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)

# Button instance for VISUALISE button
visualise_btn = Button(
    "VISUALISE", "center", 0,
    background_color=pygame.Color(*GREEN),
    foreground_color=pygame.Color(*WHITE),
    padding=6, font_size=20, outline=False,
    surface=None,
)
visualise_btn.rect.centery = top.centery

#
compare_btn = Button(
    "Run All    ", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False,
    surface=None,
)
compare_btn.rect.centery = top.centery
compare_btn.rect.left = visualise_btn.rect.right + 50

comapre_menu = Menu(
    surface=None,
    button=compare_btn,
    children=[
        Button(
            surface=None,
            text="Current Maze",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
        Button(
            surface=None,
            text="Different Mazes",
            x=0,
            y=0,
            background_color=pygame.Color(*DARK_BLUE),
            foreground_color=pygame.Color(*WHITE),
            font_size=20, outline=False
        ),
    ]
)

generate_btn = Button(
    "Generate Maze", 0, 0,
    background_color=pygame.Color(*DARK_BLUE),
    foreground_color=pygame.Color(*WHITE),
    font_size=20, outline=False,
    surface=None,
)
generate_btn.rect.centery = top.centery
generate_btn.rect.left = compare_btn.rect.right + 50


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
        Button(
            surface=None,
            text="Basic Weight Maze",
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


def initialize(window):
    """Initialize visualization mode by setting the surfaces"""
    # Set window as the surface for all UI elements
    title.surface = window
    algorithm_btn.surface = window
    for child in algo_menu.children:
        child.surface = window
    algo_menu.surface = window
    
    speed_btn.surface = window
    for child in speed_menu.children:
        child.surface = window
    speed_menu.surface = window
    
    visualise_btn.surface = window
    compare_btn.surface = window
    for child in comapre_menu.children:
        child.surface = window
    comapre_menu.surface = window
    
    generate_btn.surface = window
    for child in generate_menu.children:
        child.surface = window
    generate_menu.surface = window
    
    clear_btn.surface = window
    back_btn.surface = window
    legends_btn.surface = window


def draw(window, state, maze):
    """Draw visualization mode interface"""
    # Fill white, draw top background and title text
    window.fill(WHITE)
    pygame.draw.rect(window, DARK_BLUE, top)
    title.draw()
    back_btn.draw()
    legends_btn.draw()

    # Draw state labels
    state.label.draw()
    state.speed_label.draw()

    maze.draw()

    # Handle buttons
    if (algo_menu.draw() or algo_menu.clicked) \
            and not maze.animator.animating:
        state.overlay = True
        if algo_menu.selected:
            state.label = Label(
                algo_menu.selected.text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False,
                surface=window,
            )
            state.label.rect.bottom = HEADER_HEIGHT - 10

            if state.done_visualising:
                text = state.label.text.split(" takes")[0]
                instant_algorithm(maze, text)

            state.overlay = False
            
    # Handle legends button click
    if legends_btn.draw() and not maze.animator.animating:
        state.overlay = True
        # Create and display legends popup
        show_legends_popup(window, state)
        
    if (speed_menu.draw() or speed_menu.clicked) \
            and not maze.animator.animating:
        state.overlay = True

        if speed_menu.selected:
            state.speed_label = Label(
                surface=window,
                text=speed_menu.selected.text,
                font_size=16,
                x=speed_btn.rect.x,
                y=speed_btn.rect.bottom,
                foreground_color=pygame.Color(*WHITE),
                background_color=pygame.Color(*BLUE_2),
            )
            state.speed_label.rect.centerx = speed_btn.rect.centerx
            maze.set_speed(speed_menu.selected.text)
            state.overlay = False

    if visualise_btn.draw() \
        and not state.label.text.startswith("Choose") \
            and not maze.animator.animating:
        state.overlay = True

        text = state.label.text.split(" took")[0]
        text = text.split("Running ")[-1]
        idx = [algo_menu.children.index(btn)
               for btn in algo_menu.children if btn.text == text][0]
        run_single(idx, maze, state, window)

    if clear_btn.draw() and not maze.animator.animating:
        maze.clear_board()
        state.done_visualising = False
        state.need_update = True

    if (comapre_menu.draw() or comapre_menu.clicked) \
            and not maze.animator.animating:
        state.overlay = True

        if comapre_menu.selected \
                and comapre_menu.selected.text == "Current Maze":
            state.results = {}
            run_all(0, maze, state, window)
        elif comapre_menu.selected \
                and comapre_menu.selected.text == "Different Mazes":
            state.run_all_mazes = True
            state.results = {}
            run_all(0, maze, state, window)

    if (generate_menu.draw() or generate_menu.clicked) \
            and not maze.animator.animating:
        state.overlay = True

        if generate_menu.selected:
            maze.clear_board()
            text = state.label.text

            def callback():
                state.overlay = False
                state.label = Label(
                    f"{text}", "center", 0,
                    background_color=pygame.Color(*WHITE),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=window,
                )
                state.label.rect.bottom = HEADER_HEIGHT - 10

            maze.generate_maze(
                algorithm=generate_menu.selected.text,
                after_generation=callback
            )

            algorithm = generate_menu.selected.text

            if "Weight" in algorithm:
                new_text = "Generating basic weight maze"
            elif "Basic Random" in algorithm:
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

    if state.results_popup:
        state.overlay = True
        if state.results_popup.draw():
            state.results_popup = None
            state.overlay = False


def instant_algorithm(maze: Maze, algo_name: str):
    """Find path without animation

    Args:
        maze (Maze): Maze
        algo_name (str): Algorithm name
    """
    # Check if an algorithm has been selected
    if algo_name == "Choose an algorithm" or not algo_name:
        return
        
    maze.clear_visited()

    solution = maze.solve(algo_name=algo_name)
    print("DEBUG - Algo name:", algo_name)

    path = solution.path
    explored = solution.explored

    # Mark explored nodes as blue
    for i, j in explored:
        if (i, j) in (maze.start, maze.goal):
            continue

        maze.set_cell((i, j), "V")

    # Mark optimal path nodes as yellow
    for i, j in path:
        if (i, j) in (maze.start, maze.goal):
            continue

        maze.set_cell((i, j), "*")


def get_pressed() -> tuple[bool, int | None]:
    """Return pressed key if number

    Returns:
        tuple[bool, int | None]: Whether a num key was pressed,
                                 the key if found
    """
    keys = [pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5,
            pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]

    pressed = pygame.key.get_pressed()
    for key in keys:
        if pressed[key]:
            return True, key

    return False, None


def run_single(idx: int, maze: Maze, state: State, window) -> None:
    """Run a single algorithm on one maze

    Args:
        idx (int): Algorithm index
        maze (Maze): The maze to solve
        state (State): Application state
        window: The window surface
    """
    maze.clear_visited()
    text = algo_menu.children[idx].text
    solution = maze.solve(text)

    def callback():
        state.done_visualising = True
        state.label = Label(
            f"{text} took {solution.explored_length} steps in "
            f"{solution.time:.2f}ms", "center", 0,
            background_color=pygame.Color(*WHITE),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=20, outline=False,
            surface=window,
        )
        state.label.rect.bottom = HEADER_HEIGHT - 10
        state.overlay = False

    maze.visualize(solution=solution, after_animation=callback)

    state.label = Label(
        f"Running {text}", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 10


def run_all(algo_idx: int, maze: Maze, state: State, window, maze_idx: int = -1) -> None:
    """Run all the algorithms on current or all mazes

    Args:
        algo_idx (int): Algorithm index
        maze (Maze): The maze to solve
        state (State): Application state
        window: The window surface
        maze_idx (int, optional): Maze index. Defaults to -1.
    """
    maze.clear_visited()
    text = algo_menu.children[algo_idx].text

    def callback():
        if algo_idx + 1 < len(algo_menu.children):
            run_all(algo_idx + 1, maze, state, window, maze_idx)
        elif state.run_all_mazes \
                and maze_idx + 1 < len(generate_menu.children):
            maze.clear_board()

            def after_generation():
                run_all(0, maze, state, window, maze_idx + 1)

            maze.generate_maze(
                algorithm=generate_menu.children[maze_idx + 1].text,
                after_generation=after_generation
            )

            algorithm = generate_menu.children[maze_idx + 1].text

            if "Weight" in algorithm:
                new_text = "Generating basic weight maze"
            elif "Basic Random" in algorithm:
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
        else:
            state.label = Label(
                text, "center", 0,
                background_color=pygame.Color(*WHITE),
                foreground_color=pygame.Color(*DARK),
                padding=6, font_size=20, outline=False,
                surface=window,
            )
            state.label.rect.bottom = HEADER_HEIGHT - 10

            results = list(state.results.items())

            if state.run_all_mazes:
                for result in results:
                    result[1]["path_length"] //= maze_idx + 2
                    result[1]["path_cost"] //= maze_idx + 2
                    result[1]["explored_length"] //= maze_idx + 2
                    result[1]["time"] /= maze_idx + 2

            results.sort(key=lambda item: item[1]["time"])

            show_results(results, window, state)
            state.run_all_mazes = False
            state.overlay = False

    solution = maze.solve(text)

    if text not in state.results:
        state.results[text] = vars(solution)
    else:
        state.results[text]["explored_length"] += solution.explored_length
        state.results[text]["path_length"] += solution.path_length
        state.results[text]["path_cost"] += solution.path_cost
        state.results[text]["time"] += solution.time

    maze.visualize(solution=solution, after_animation=callback)

    state.label = Label(
        f"Running {text}", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 10


def show_results(results: list[tuple[str, dict[str, float]]], window, state) -> None:
    """Display results

    Args:
        results (list[tuple[str, dict[str, float]]]): Result data
        window: The window surface
        state (State): Application state
    """
    children: list[list[TableCell]] = []
    children.append([
        TableCell(
            child=Label(
                    "Algorithm", 0, 0,
                    background_color=pygame.Color(*DARK_BLUE),
                    foreground_color=pygame.Color(*WHITE),
                    padding=6, font_size=20, outline=False,
                    surface=window,
                    ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Steps Explored", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=window,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Path Length", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=window,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Path Cost", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=window,
            ),
            color=DARK_BLUE,
        ),
        TableCell(
            child=Label(
                "Time Taken", 0, 0,
                background_color=pygame.Color(*DARK_BLUE),
                foreground_color=pygame.Color(*WHITE),
                padding=6, font_size=20, outline=False,
                surface=window,
            ),
            color=DARK_BLUE,
        ),
    ])

    # Use different colors for better visual distinction between algorithms
    # First two algorithms get GREEN_2 (best performers), next two get YELLOW, rest get GRAY
    colors = [GREEN_2, GREEN_2, YELLOW, YELLOW]
    colors.extend([GRAY] * (len(results) - 4))  # Ensure we have enough colors for all algorithms

    for i, result in enumerate(results):
        children.append([
            TableCell(
                child=Label(
                        f"{i + 1}. {result[0]}", 0, 0,
                        background_color=pygame.Color(*colors[i]),
                        foreground_color=pygame.Color(*DARK),
                        padding=6, font_size=20, outline=False,
                        surface=window,
                        ),
                color=colors[i],
                align=Alignment.LEFT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['explored_length']}", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=window,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['path_length']}", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=window,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['path_cost']}", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=window,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
            TableCell(
                child=Label(
                    f"{result[1]['time']:.2f}ms", 0, 0,
                    background_color=pygame.Color(*colors[i]),
                    foreground_color=pygame.Color(*DARK),
                    padding=6, font_size=20, outline=False,
                    surface=window,
                ),
                color=colors[i],
                align=Alignment.RIGHT
            ),
        ])

    popup = Popup(
        window,
        0,
        0,
        padding=20,
        color=DARK,
        orientation=Orientation.VERTICAL,
        x_align=Alignment.CENTER,
        y_align=Alignment.CENTER,
        children=[
            Label(
                "COMPARISON RESULTS", 0, 0,
                background_color=pygame.Color(*DARK),
                foreground_color=pygame.Color(*WHITE),
                padding=10, font_size=20, outline=False,
                surface=window,
            ),
            Table(
                x=0,
                y=0,
                rows=len(children),  # Dynamic row count based on number of algorithms
                columns=5,
                padding=20,
                color=DARK,
                children=children,
            )
        ],
    )

    popup.update_center(window.get_rect().center)
    popup.set_surface(window)
    state.results_popup = popup


def show_legends_popup(window, state) -> None:
    """Display legends popup

    Args:
        window: The window surface
        state (State): Application state
    """
    children = [
        Label(
            "LEGENDS", 0, 0,
            background_color=pygame.Color(*DARK),
            foreground_color=pygame.Color(*WHITE),
            padding=10, font_size=20, bold=True,
            surface=window,
        ),
        Label(
            ">: Start Node", 0, 0,
            background_color=pygame.Color(*WHITE),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=18, outline=False,
            surface=window,
        ),
        Label(
            "O: Goal Node", 0, 0,
            background_color=pygame.Color(*WHITE),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=18, outline=False,
            surface=window,
        ),
        Label(
            "   Wall Node ", 0, 0,
            background_color=pygame.Color(*DARK),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=18, outline=False,
            surface=window,
        ),
        Label(
            " Visited Node", 0, 0,
            background_color=pygame.Color(*BLUE),
            foreground_color=pygame.Color(*WHITE),
            padding=6, font_size=18, outline=False,
            surface=window,
        ),
        Label(
            " Path Node  ", 0, 0,
            background_color=pygame.Color(*YELLOW),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=18, outline=False,
            surface=window,
        ),
        Label(
            "2-9: Weighted Nodes", 0, 0,
            background_color=pygame.Color(*GRAY),
            foreground_color=pygame.Color(*DARK),
            padding=6, font_size=18, outline=False,
            surface=window,
        ),
    ]

    popup = Popup(
        window,
        0,
        0,
        padding=20,
        color=DARK,
        orientation=Orientation.VERTICAL,
        x_align=Alignment.CENTER,
        y_align=Alignment.CENTER,
        children=children,
    )

    popup.update_center(window.get_rect().center)
    popup.set_surface(window)
    state.results_popup = popup


def run_visualize_mode(window, state, maze, animator):
    """Run the visualization mode loop"""
    # Initialize UI elements with the window surface
    initialize(window)

    # Set initial UI state
    state.player_mode = False
    state.need_update = True
    state.label = Label(
        "Choose an algorithm", "center", 0,
        background_color=pygame.Color(*WHITE),
        foreground_color=pygame.Color(*DARK),
        padding=6, font_size=20, outline=False,
        surface=window,
    )
    state.label.rect.bottom = HEADER_HEIGHT - 10

    state.speed_label = Label(
        surface=window,
        text="Fast",
        font_size=16,
        x=speed_btn.rect.x,
        y=speed_btn.rect.bottom,
        foreground_color=pygame.Color(*WHITE),
        background_color=pygame.Color(*BLUE_2),
    )
    state.speed_label.rect.centerx = speed_btn.rect.centerx

    # Track mouse state
    mouse_is_down = False
    dragging = False
    cell_under_mouse = (-1, -1)
    cell_value = ""
    
    # Indicate when user clicks back button
    exit_to_menu = False
    
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
                
                # Other mouse handling
                if state.overlay:
                    continue

                state.need_update = True
                pos = pygame.mouse.get_pos()

                if not maze.mouse_within_bounds(pos):
                    continue

                mouse_is_down = True

                row, col = maze.get_cell_pos(pos)
                if (value := maze.get_cell_value((row, col))) in ("A", "B"):
                    dragging = True
                    cell_under_mouse = (row, col)
                    cell_value = value

            if event.type == pygame.MOUSEBUTTONUP:
                mouse_is_down = False
                animator.animating = False
                draw_weighted_nodes = False

                if dragging:
                    dragging = False

                    pos = pygame.mouse.get_pos()
                    if not maze.mouse_within_bounds(pos):
                        continue

                    row, col = maze.get_cell_pos(pos)
                    if maze.get_cell_value((row, col)) in ("A", "B") or state.done_visualising:
                        continue

                    maze.set_cell((row, col), cell_value)
                    maze.set_cell(cell_under_mouse, "1")

                cell_under_mouse = (-1, -1)
        
        # Check if we should exit to menu
        if exit_to_menu:
            break
            
        # Main visualization interface
        if state.need_update:
            draw(window, state, maze)

        # Get pressed keys for weighted nodes
        draw_weighted_nodes, key = get_pressed()

        # Draw walls | weighted nodes
        # This should not run when animating solution
        if mouse_is_down and not dragging:
            pos = pygame.mouse.get_pos()

            if maze.mouse_within_bounds(pos):
                row, col = maze.get_cell_pos(pos)

                if cell_under_mouse != (row, col):
                    if maze.get_cell_value((row, col)) in ("1", "V", "*"):
                        rect = pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE)
                        x, y = maze.coords[row][col]

                        if draw_weighted_nodes and key:
                            animator.add_nodes_to_animate([
                                AnimatingNode(
                                    rect=rect,
                                    center=(x + CELL_SIZE // 2,
                                            y + CELL_SIZE // 2),
                                    ticks=pygame.time.get_ticks(),
                                    value=str(key % 50 + 2),
                                    animation=Animation.WEIGHT_ANIMATION,
                                    color=WHITE,
                                    duration=50,
                                )
                            ])
                        else:
                            animator.add_nodes_to_animate([
                                AnimatingNode(
                                    rect=rect,
                                    center=(x + CELL_SIZE // 2,
                                            y + CELL_SIZE // 2),
                                    ticks=pygame.time.get_ticks(),
                                    value="#",
                                    color=DARK
                                )
                            ])

                    elif maze.get_cell_value((row, col)) not in ("A", "B"):
                        maze.set_cell((row, col), "1")

                    cell_under_mouse = (row, col)

        # Animate nodes
        if animator.nodes_to_animate and state.need_update:
            animator.animating = True
            animator.animate_nodes()
        else:
            animator.animating = False

        # Handle moving start and target nodes
        if dragging and not state.done_visualising and not animator.animating:
            x, y = pygame.mouse.get_pos()
            if cell_value == "A":
                window.blit(START, (x - 10, y - 10))
            else:
                window.blit(GOAL, (x - 10, y - 10))

        # Instantly find path if dragging post visualisation
        if dragging and state.done_visualising and not animator.animating:
            x, y = pygame.mouse.get_pos()

            if maze.mouse_within_bounds((x, y)):
                row, col = maze.get_cell_pos((x, y))
                x, y = maze.coords[row][col]

                if cell_under_mouse != (row, col):
                    maze.set_cell((row, col), cell_value)
                    maze.set_cell(cell_under_mouse, "1")

                    text = state.label.text.split(" took")[0]
                    instant_algorithm(maze, text)
                    cell_under_mouse = (row, col)

        # Update display
        pygame.display.update()
        CLOCK.tick(FPS)
    
    # Return to menu when exit_to_menu is True
    return "menu"