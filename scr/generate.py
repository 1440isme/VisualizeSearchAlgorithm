import random
from typing import Any, Callable
import pygame

from .animations import AnimatingNode, Animation, Animator
from .constants import CELL_SIZE, DARK, GREEN_2, BLUE_2, MIN_SIZE, WHITE


GenerationCallback = Callable[[], None]


class MazeGenerator:

    def __init__(self, animator: Animator) -> None:
        from .maze import Maze

        self.animator = animator
        self.maze: Maze = animator.maze
        self.width = self.maze.width
        self.height = self.maze.height


    def _is_valid_cell(self, pos: tuple[int, int]) -> bool:
        """Check if the provided coords are valid

        Args:
            pos (tuple[int, int]): Cell pos

        Returns:
            bool: Whether the cell exists
        """
        rowIdx, colIdx = pos

        return 0 <= rowIdx < self.maze.height \
            and 0 <= colIdx < self.maze.width

    def _should_preserve_cell(self, pos: tuple[int, int]) -> bool:
        """Kiểm tra xem ô có phải là điểm xuất phát hoặc điểm đích không

        Args:
            pos (tuple[int, int]): Vị trí ô cần kiểm tra

        Returns:
            bool: True nếu ô cần được bảo vệ, False nếu không
        """
        return pos == self.maze.start or pos == self.maze.goal

    def _get_two_step_neighbors(
        self,
        maze: list[list[Any]],
        cell: tuple[int, int],
        value: str = ""
    ) -> list[tuple[int, int]]:
        """Get neighbors of a cell which are two steps away

        Args:
            cell (tuple[int, int]): Cell pos
            value (str): A string representing the neighbor type. `#` for a wall

        Returns:
            list[tuple[int, int]]: List of neighbors
        """
        neighbors = [(cell[0] + 2, cell[1]),
                     (cell[0] - 2, cell[1]),
                     (cell[0], cell[1] + 2),
                     (cell[0], cell[1] - 2)]

        if value == "#":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] == "#"]
        elif value == "1":
            return [neighbor for neighbor in neighbors
                    if self._is_valid_cell(neighbor)
                    and maze[neighbor[0]][neighbor[1]] != "#"]

        return [neighbor for neighbor in neighbors
                if self._is_valid_cell(neighbor)]

    

    def basic_weight_maze(self) -> None:
        """Generate a basic weight maze
        """
        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                # Bỏ qua điểm xuất phát và kết thúc
                if self._should_preserve_cell((colIdx, rowIdx)):
                    continue
                    
                if random.randint(1, 10) < 8:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value="9", #Giá trị của weight
                        color=WHITE,
                        animation=Animation.WEIGHT_ANIMATION
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)
    def randomised_dfs(self) -> None:
        """Generate maze by randomised dfs
        """
        # For animating nodes
        nodes_to_animate = []

        # Vẽ tường ở khắp mọi nơi ngoại trừ điểm xuất phát và kết thúc
        for rowIdx in range(self.maze.height):
            for colIdx in range(self.width):
                if not self._should_preserve_cell((rowIdx, colIdx)):
                    self.maze.set_cell((rowIdx, colIdx), "#")

        stack = [self.maze.start]

        visited = set()
        visited.add(self.maze.start)

        while stack:
            # Pop one cell from the stack
            curr = stack.pop()

            # Get unvisited two step neighbors of current cell
            neighbors = self._get_two_step_neighbors(self.maze.maze, curr)
            unvisited_neighbors = [neighbor for neighbor in neighbors
                                   if neighbor not in visited]

            # If the cell has unvisited neighbors, push it to the stack
            # Choose one neighbor and break wall between the neighbor
            # and the current cell. Also set the neighbor to type "1"
            if unvisited_neighbors:
                next = random.choice(unvisited_neighbors)
                stack.append(curr)
                # **THÊM**: carve the path in the grid
                # Set the neighbour cell to empty
                self.maze.set_cell(next, "1")
                # Compute the wall between and carve it
                wall = ((curr[0] + next[0]) // 2, (curr[1] + next[1]) // 2)
                self.maze.set_cell(wall, "1")

                x, y = self.maze.coords[next[0]][next[1]]
                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=BLUE_2
                    )
                )

                rowIdx = (curr[0] + next[0]) // 2
                colIdx = (curr[1] + next[1]) // 2
                x, y = self.maze.coords[rowIdx][colIdx]

                nodes_to_animate.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        value="1",
                        ticks=pygame.time.get_ticks(),
                        color=GREEN_2,
                    )
                )

                # Add the neighbor to the visited set and push it
                # to the stack
                visited.add(next)
                stack.append(next)

        # Add animating nodes for animation
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)
        
    def basic_random_maze(self) -> None:
        """Generate a basic random maze with wall density from level settings
        """
        # Lấy thông tin wall_density từ level hiện tại
        try:
            from .levels import LevelManager
            level_manager = LevelManager()
            current_level = level_manager.get_current_level()
            wall_density = current_level.get("wall_density", 0.3)  # Mặc định là 0.3 nếu không có cấu hình
        except (ImportError, AttributeError):
            wall_density = 0.3  # Giá trị mặc định
            
        # Chuyển đổi wall_density thành tỷ lệ cụ thể cho phép ngẫu nhiên (1-10)
        # Ví dụ: wall_density = 0.3 => threshold = 7 (3 trong 10 ô sẽ là tường)
        # wall_density = 1.0 => threshold = 5 (5 trong 10 ô sẽ là tường)
        if wall_density <= 0.2:
            threshold = 8  # 20% là tường
        elif wall_density <= 0.4:
            threshold = 7  # 30% là tường
        elif wall_density <= 0.6:
            threshold = 6  # 40% là tường
        elif wall_density <= 0.8:
            threshold = 5  # 50% là tường
        elif wall_density <= 1.0:
            threshold = 4  # 60% là tường
        elif wall_density <= 1.2:
            threshold = 3  # 70% là tường
        else:
            threshold = 2  # 80% là tường
            
        print(f"Generating maze with wall density: {wall_density}, threshold: {threshold}")
            
        nodes = []
        for rowIdx in range(self.maze.width):
            for colIdx in range(self.maze.height):
                # Bỏ qua điểm xuất phát và kết thúc
                if self._should_preserve_cell((colIdx, rowIdx)):
                    continue
                
                # Sử dụng threshold dựa trên wall_density để quyết định có tạo tường hay không
                if random.randint(1, 10) < threshold:
                    continue

                x, y = self.maze.coords[colIdx][rowIdx]
                nodes.append(
                    AnimatingNode(
                        rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                        center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                        ticks=pygame.time.get_ticks(),
                        value="#",
                        color=DARK
                    )
                )

        self.maze.animator.add_nodes_to_animate(nodes, gap=2)

    def recursive_division(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int
    ) -> None:
        """Generate maze by recursive division algorithm

        Args:
            x1 (int): Grid row start
            x2 (int): Grid row end
            y1 (int): Grid column start
            y2 (int): Grid column end
        """
        width = x2 - x1
        height = y2 - y1

        # Base case:
        if width < 1 or height < 1:
            return

        # Whether to draw horizontally or vertically
        horizontal = True if height > width else (
            False if width != height else random.choice((True, False)))

        # Arguments for reursive calls
        args_list: list[tuple[int, int, int, int]] = []

        # Divide the maze and add new grids' properties to args_list
        if horizontal:
            y = self._draw_line(x1, x2, y1, y2, horizontal=True)
            args_list.extend([(x1, x2, y1, y - 1), (x1, x2, y + 1, y2)])
        else:
            x = self._draw_line(x1, x2, y1, y2)
            args_list.extend([(x1, x - 1, y1, y2), (x + 1, x2, y1, y2)])

        # Divide the two grids
        for args in args_list:
            self.recursive_division(*args)

    def _draw_line(
        self,
        x1: int,
        x2: int,
        y1: int,
        y2: int,
        horizontal: bool = False
    ) -> int:
        """Draw walls horizontally or vertically

        Args:
            x1 (int): Grid row start
            x2 (int): Grid row end
            y1 (int): Grid column start
            y2 (int): Grid column end
            horizontal (bool, optional): Horizontal or vertical. Defaults to False.

        Returns:
            int: X or Y coordinate of wall line
        """

        # Handle horizontal division
        if horizontal:
            x1, y1 = y1, x1
            x2, y2 = y2, x2

        # Walls at even places
        if x1 % 2 != 0:
            x1 += 1
        wall = random.randrange(x1, x2, 2)

        # Holes at odd places
        if y1 % 2 == 0:
            y1 += 1
        hole = random.randrange(y1, y2, 2)

        # Coordinates
        hole_coords = (hole, wall) if not horizontal else (wall, hole)
        wall_coords = [-1, wall] if not horizontal else [wall, -1]

        # Draw walls
        nodes_to_animate = []
        for i in range(y1, y2 + 1):
            wall_coords[horizontal] = i
            if hole_coords == tuple(wall_coords) or self._should_preserve_cell((wall_coords[0], wall_coords[1])):
                continue

            # Create a rectangle
            rect = pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE)

            # Set the starting position of the rectangle
            x, y = self.maze.coords[wall_coords[0]][wall_coords[1]]
            rect.center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            nodes_to_animate.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=rect,
                    ticks=pygame.time.get_ticks(),
                    value="#",
                    color=DARK
                )
            )
        self.maze.animator.add_nodes_to_animate(nodes_to_animate)

        return wall