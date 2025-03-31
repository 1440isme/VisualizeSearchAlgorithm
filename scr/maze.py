from typing import Optional # chỉ định kiểu dữ liệu, đặc biệt các hàm có thể nhận giá trị null
import pygame

from .generate import GenerationCallback, MazeGenerator
from .animations import AnimatingNode, Animation, AnimationCallback, Animator
from .pathfinder.models.node import Node
from .pathfinder.models.solution import Solution
from .pathfinder.main import PathFinder
from .pathfinder.models.grid import Grid
from .pathfinder.models.search_types import Search

from .constants import (
    DARK_BLUE_2,
    GOAL,
    HEIGHT,
    MIN_SIZE,
    REMAINDER_H,
    REMAINDER_W,
    START,
    WEIGHT,
    CELL_SIZE,
    FONT_14,
    GRAY,
    GREEN_2,
    MAZE_HEIGHT,
    HEADER_HEIGHT,
    MAZE_WIDTH,
    BLUE_2,
    WIDTH,
    BLUE,
    DARK,
    WHITE,
    GREEN,
    YELLOW
)

# ================ Thiết kế lớp MazeNode ================
"""Kế thừa từ lớp Node, dùng để biểu diễn một ô trong mê cung"""
class MazeNode(Node):
    def __init__(
        self, 
        value: str,
        state: tuple[int, int],
        cost: int, 
        parent: Node | None = None, 
        action: str | None = None,
        color: tuple[int, int, int] = WHITE
    ) -> None:
        super().__init__(value, state, cost, parent, action) # gọi hàm khởi tạo của lớp cha 
        self.color = color


# ================ Thiết kế lớp Maze ================
"""Class này quản lý tạo mê cung, vẽ mê cung, giải mê cung, và trực quan hóa
Các chức năng sẽ của class:
    Quản lý lưới mê cung 2D
    Gán node bắt đầu và kết thúc
    Cho phép cập nhật từng ô
    Hỗ trợ vẽ mê cung ra mh
    Gọi thuật toán tạo và giải mê cung 
    Tổ chức các animation qua self.animator
"""

class Maze:
    def __init__(self, surface: pygame.surface.Surface) -> None:
        self.surface = surface
        self.animator: Animator
        self.generator: MazeGenerator

        self.width = MAZE_WIDTH // CELL_SIZE
        self.height = MAZE_HEIGHT // CELL_SIZE

        self.maze = [[MazeNode("1", (rowIdx, colIdx), 1)
                      for colIdx in range(self.width)]
                     for rowIdx in range(self.height)]
        
        # Ví trị bắt đầu của mũi tên và kết thúc của tâm 
        start_col = self.width // 4 # Bên mép trái
        goal_col = self.width - self.width // 4 - 1  # Bên mép phải 
        if start_col > goal_col: # điều kiện ở đây để tránh bug logic
            start_col, goal_col = goal_col, start_col

        # Đảm bảo lun đặt ở giữa mê cung
        self.start = (self.height // 2, start_col)
        self.goal = (self.height // 2, goal_col)

        self.maze[self.start[0]][self.start[1]].value = "A" # gán cho điểm bắt đầu là A
        self.maze[self.start[0]][self.start[1]].cost = 0
        self.maze[self.goal[0]][self.goal[1]].value = "B"
        self.maze[self.goal[0]][self.goal[1]].cost = 1

        # Tạo tọa độ màn hình cho mê cung
        self.coords = self._generate_coordinates()

        # Tốc độ
        self.speed = "Fast"

    def _generate_coordinates(self) -> list[list[tuple[int, int]]]:
        """ Hàm này tính tọa độ pixel
         Returns: 
            list[list[tuple[int, int]]]: ma trận tọa độ
        """

        coords: list[list[tuple[int, int]]] = []

        # Tạo tọa độ cho từng ô trong mê cung
        for i in range(self.height):
            row = []
            for j in range(self.width):
                # Tính tọa độ cho góc bên trái của ô 
                x = j * CELL_SIZE + (REMAINDER_W // 2) # Di chuyển sang phải j ô
                y = i * CELL_SIZE + (HEADER_HEIGHT) # Di chuyển xún i ô
                
                row.append((x, y))

            coords.append(row)

        return coords

    def get_cell_value (self, pos: tuple[int, int]) -> str:
        """ Lấy giá trị của ô
        Args: 
            pos: tuple[int, int]: Vị trí của ô
        Returns: 
            str: Giá trị của ô
        """
        return self.maze[pos[0]][pos[1]].value

    def get_node(self, pos: tuple[int, int]) -> MazeNode:
        """ Lấy node của ô
        Args: 
            pos: tuple[int, int]: Vị trí của ô
        Returns: 
            Node cần lấy
        """
        return self.maze[pos[0]][pos[1]]
    
    def set_cell(self, pos: tuple[int, int], value: str, forced: bool = False) -> None:
        """ Cập nhật giá trị ô trong mê cung
        Args: 
            pos (tuple[int, int]): vị trị
            value (str): giá trị
            forced (bool): biến này giúp bv cái ô đặc biệt ko bị thay đổi giá trị
        """
        if pos in (self.start, self.goal) and not forced: # ko cho ghi đè lên điểm A, B
            if value == "V": # cho phép đổi màu tạm thời nếu value là V (visited)
                self.maze[pos[0]][pos[1]].color = BLUE
            elif value == "*": # * (path) để làm animation 
                self.maze[pos[0]][pos[1]].color = YELLOW
        
        match value:
            case "A": # điểm bắt đầu; cập nhật self.start, reset cha
                color = WHITE
                cost = 0
                self.start = pos
                self.maze[pos[0]][pos[1]].parent = None
            case "B": # điểm kết thúc; cập nhật self.goal, reset cha
                color = WHITE
                cost = 1
                self.goal = pos
                self.maze[pos[0]][pos[1]].parent = None
            case "#": # tường; Không thể đi qua
                cost = -1
                color = DARK
            case "V": # Đã duyệt (visited); Hiện thị animation
                cost = self.maze[pos[0]][pos[1]].cost
                color = BLUE
            case "*": # nằm trong đường đi ngắn nhất; Hiện thị animation
                cost = self.maze[pos[0]][pos[1]].cost
                color = YELLOW
            case _: # mặc định; cho phép tạo mê cung có trọng số
                cost = int(value)
                color = WHITE

        self.maze[pos[0]][pos[1]].value = value
        self.maze[pos[0]][pos[1]].cost = cost
        self.maze[pos[0]][pos[1]].color = color

    
    def set_speed(self, speed_str: str) -> None:
        """Đặt tốc độ trực quan hóa
        Args: 
            speed_str (str): speed string
        """

        if not speed_str in ("Nhanh", "Vừa", "Chậm"):
            return
        
        self.speed = speed_str

    def clear_board(self) -> None:
        """Xóa các tường mê cung"""
        self.maze = [[MazeNode("1", (rowIdx, colIdx), 1)
                      for colIdx in range(self.width)]
                      for rowIdx in range(self.height)]
        
        # reset lại điểm bắt đầu và kết thúc
        self.set_cell(self.start, "A", forced=True)
        self.set_cell(self.goal, "B", forced=True)

    def clear_visited(self) -> None:
        """Xóa các node đã thăm"""
        for rowIdx in range(self.height):
            for colIdx in range(self.width):
                node = self.maze[rowIdx][colIdx]
                self.maze[rowIdx][colIdx] = MazeNode(
                    str(node.cost) if node.value in ("V", "*") else node.value,
                    (rowIdx, colIdx), 
                    node.cost
                )
                self.set_cell((rowIdx, colIdx), self.maze[rowIdx][colIdx].value)

        self.set_cell(self.start, "A", forced=True)
        self.set_cell(self.goal, "B", forced=True)

    
    def mouse_within_bounds (self, pos: tuple[int, int]) -> bool:
        """Kiểm tra xem con chuột có nằm bên trong mê cung hay ko 
        Args:
            pos: tuple[int, int]: vị trí của chuột
        Returns: 
            bool: Chuột có nằm bên trong ko 
        """
        return all((
            pos[0] > REMAINDER_W // 2, # nằm bên phải lề trái
            pos[0] < WIDTH - REMAINDER_W // 2, # nằm bên trái lề phải

            pos[1] > HEADER_HEIGHT, # nằm dưới phần header tiêu đề
            pos[1] < HEIGHT - REMAINDER_H # không vượt quá mê cung
        ))

    def get_cell_pos (self, pos: tuple[int, int]) -> tuple[int, int]:
        """ Lấy vị trí ổ từ con chuột

        Args:
            pos (tuple[int, int]): vị trí chuột

        Returns:
            tuple[int, int]: vị trí ô
        """
        x, y = pos

        return ((y - HEADER_HEIGHT) // CELL_SIZE,
                (x - REMAINDER_W // 2) // CELL_SIZE)
    
    def draw(self) -> None:
        """Vẽ mê cung"""
        nodes_to_animate = self.animator.nodes_to_animate # lấy các node đang trong quá trình animation

        # vẽ từng ô trên màn hình
        for i, row in enumerate(self.maze):
            for j, node in enumerate(row):
                # tính tọa độ của ô hiện tại trên màn hình
                x, y = self.coords[i][j]
                center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2)
                # nếu ko có animation tại ô đó -> vẽ ô bth với màu là node.color, rồi bỏ qua xử lí animation
                if not center in nodes_to_animate:
                    self._draw_rect((i, j), node.color)
                    continue
            # nếu có animation -> check dsach các AnimatingNode tại center
            for k in range(len(nodes_to_animate[center]) - 1, -1, -1):
                animating_node = nodes_to_animate[center][k]
                if animating_node.progress > 0: # đang diễn ra
                    self._draw_rect(
                        coords=(i, j),
                        color = animating_node.color,
                        node = animating_node
                    )
                    break
            else:
                self._draw_rect((i, j), node.color)

    def generate_maze(
        self, 
        algorithm: str,
        after_generation: Optional[GenerationCallback] = None
    ) -> None:
        """ Tạo mê cung bằng các thuật toán
        Args: 
            algorithm(str): Tên các thuật toán
        """

        match algorithm:
            case "Recursive Division":
                self._draw_walls_around() # vẽ tường bao quanh mê cung
                self.generator.recursive_division(
                    1, self.width - 2, 1, self.height - 2)
            case "Randomised DFS":
                self.generator.randomised_dfs()
            case "Prim's Algorithm":
                self.generator.randomised_prims_algorithm()
            case "Basic Weight Maze":
                self.generator.basic_weight_maze()
            case "Basic Random Maze":
                self.generator.basic_random_maze()
        # xử lí animation sau khi sinh mê cung xong
        # Lấy animation cuối trong toàn bộ các node cần animate -> gán cho một callback after_generation để thực hiện hành động khi animation kết thúc
        list(self.animator.nodes_to_animate.values())[-1][-1].after_animation = after_generation


    def _draw_walls_around(self) -> None:
        """Vẽ tường xung quanh mê cung"""

        # Tường trên (top horizontal wall)
        nodes_to_animate = []
        for i in range(self.width):
            x, y = self.coords[0][i]
            nodes_to_animate.append(
                AnimatingNode(
                    rect = pygame.Rect(0,0, MIN_SIZE, MIN_SIZE), # animation nhỏ rồi phóng to sau
                    center = (x + CELL_SIZE // 2, y + CELL_SIZE // 2), # để animate vào đúng vị trí
                    value = "#",
                    ticks = pygame.time.get_ticks(), # Trả về số mili-giây (ms) kể từ khi Pygame được khởi động -> đkhiển animation, tính tg, delay
                    color = DARK
                )
            )
        # thêm danh sách này vào animator
        self.animator.add_nodes_to_animate(nodes_to_animate)

        # Tường dưới (bottom horizontal wall)
        nodes_to_animate = []
        for i in range(self.width):
            x, y = self.coords[-1][i]
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)

        # Tường trái và phải (side walls)
        nodes_to_animate = []
        for i in range(self.height):
            x, y = self.coords[i][0] # xử lí cột bên trái
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

            x, y = self.coords[i][-1] # xử lí cột bên phải
            nodes_to_animate.append(
                AnimatingNode(
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    value="#",
                    ticks=pygame.time.get_ticks(),
                    color=DARK
                )
            )

        self.animator.add_nodes_to_animate(nodes_to_animate)
    
    def solve(self, algo_name: str,) -> Solution:
        """Giải mê cung với các thuật toán
        Args:
            algo_name(str): tên của thuật toán
        """
        mapper: dict[str, Search] = {
            "A* Search": Search.ASTAR_SEARCH,
            "Dijkstra's Search": Search.DIJKSTRAS_SEARCH,
            "Greedy Best First Search": Search.GREEDY_BEST_FIRST_SEARCH,
            "Breadth First Search": Search.BREADTH_FIRST_SEARCH,
            "Depth First Search": Search.DEPTH_FIRST_SEARCH,
        }

        # khởi tạo grid
        grid = Grid(self.maze, self.start, self.goal) # Chuyển mê cung self.maze thành đối tượng Grid – cấu trúc được PathFinder hiểu để làm việc.

        # Giải mê cung
        solution = PathFinder.find_path(
            grid=grid,
            search=mapper[algo_name.strip()],
        )

        return solution
    
    def visualize(
        self, 
        solution: Solution,
        after_animation: Optional[AnimationCallback] = None
    ) -> None:
        """Minh họa cách giả
        Args: 
            solution (Solution): Đối tượng được giả
            after_animation (Optional[AnimationCallback], optional): Được gọi sau khi animation xong, mặc định là None
        """

        # Tạo danh sách node đã duyệt (explored)
        nodes = []
        for cell in solution.explored:
            x,y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=pygame.Rect(0, 0, CELL_SIZE, CELL_SIZE),
                    ticks=pygame.time.get_ticks(),
                    value="V", 
                    color=WHITE,
                    colors=[YELLOW, DARK_BLUE_2, BLUE_2, GREEN_2, BLUE], # các màu sẽ chuyển dần trong animation
                    duration=1500, # animation kéo dài 1.5s -> animate của cái ô tròn xanh duyệt
                    animation=Animation.PATH_ANIMATION # loại animation đặc biệt đc định nghĩa sẵn 
                )
            )

        # gap: Khoảng thời gian (ms) giữa 2 node được animate -> điều chỉnh nhanh chậm
        match self.speed:
            case "Nhanh":
                gap = 5
            case "Vừa":
                gap = 30
            case "Chậm":
                gap = 1000
            case _:
                gap = 5

        self.animator.add_nodes_to_animate(nodes, gap=gap)

        # Nếu ko tìm thấy đường đi, path rỗng -> gắn after_animation cho node cuối và end
        if not solution.path:
            nodes[-1].after_animation = after_animation
            return
        
        # Vẽ đường đi ngắn nhất bằng màu vàng
        nodes = []
        for cell in solution.path:
            x, y = self.coords[cell[0]][cell[1]]
            nodes.append(
                AnimatingNode(
                    center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2),
                    rect=pygame.Rect(0, 0, MIN_SIZE, MIN_SIZE),
                    ticks=pygame.time.get_ticks(),
                    value="*", # đánh dấu là đường đi
                    color=YELLOW,
                    duration=1000,
                )
            )

        match gap:
            case 5:
                gap = 30
            case 30:
                gap = 50
            case 1000:
                gap = 50

        #  Thêm animation cho path và callback sau animation
        self.animator.add_nodes_to_animate(nodes, delay=600, gap=gap) # delay=600: đợi 0.6s sau khi explored xong mới vẽ path
        nodes[-1].after_animation = after_animation

    def _draw_rect(
        self, 
        coords: tuple[int, int],
        color: tuple[int, int, int] = BLUE,
        node: AnimatingNode | None = None
    ) -> None:
        """Tô màu ô hiện tại trong mê cung"""

        # Xác định vị trí trên màn hình 
        row, col = coords
        x, y = self.coords[row][col]

        # Không vẽ màu tối lên ô Start/Goal để tránh mất icon
        if coords in (self.start, self.goal) and color == DARK:
            return
        
        # Vẽ ô chính; Nếu là animation sẽ thay đổi kích thước/dạng ; Ngược lại vẽ ô cố định với sz = CELL_SIZE
        pygame.draw.rect(
            surface=self.surface,
            color=color,
            rect=node.rect if node else pygame.Rect(
                x, y, CELL_SIZE, CELL_SIZE)
        )

        # Vẽ viền (border)
        if color in (BLUE, WHITE, GREEN) or (node and node.color == YELLOW): # nếu ô là trắng, xanh, xanh lá hoặc animation đang màu vàng -> vẽ viền 
            pygame.draw.rect(
                surface=self.surface,
                color=GREEN if color == GREEN_2 else GRAY,
                rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE),
                width=1
            )

        # Vẽ icon nếu là ô có cost > 1
        if (n := self.maze[row][col]).cost > 1:
            image_rect = WEIGHT.get_rect(
                center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.surface.blit(WEIGHT, image_rect)

            text = FONT_14.render(
                str(n.cost if not node else node.value), True, GRAY)
            text_rect = text.get_rect()
            text_rect.center = image_rect.center
            self.surface.blit(text, text_rect)

        # Nếu là điểm bắt đầu
        elif (row, col) == self.start:
            image_rect = START.get_rect(
                center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.surface.blit(START, image_rect)

        # Nếu là điểm kết thúc
        elif (row, col) == self.goal:
            image_rect = GOAL.get_rect(
                center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
            self.surface.blit(GOAL, image_rect)

