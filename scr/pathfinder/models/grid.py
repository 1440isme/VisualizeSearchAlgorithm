"""
Biểu diễn một lưới (hoặc mê cung) với các ô được lưu dưới dạng các đối tượng Node.
Truy cập các ô trong lưới, lấy thông tin trọng số của ô và xác định các ô kề (hàng xóm) từ một vị trí nhất định.
"""
from scr.pathfinder.models.node import Node

class Grid:
    def __init__(self, grid: list[list[Node]], start: tuple[int, int], end: tuple[int, int]) -> None:
        self.grid: list[list[Node]] = grid
        self.start = start
        self.end = end

        #Tính toán kích thước lưới (grid)
        self.width = max(len(row) for row in grid)
        self.height = len(grid)

    def get_node(self, pos: tuple[int, int]) -> Node:
        """Lấy một node theo vị trí

        Args:
            pos (tuple[int, int]): Vị trí của ô trong lưới

        Returns:
            Node: Node tại vị trí đã cho
        """
        return self.grid[pos[0]][pos[1]]
    
    def get_cost(self, pos: tuple[int, int]) -> int:
        """Lấy trọng số của một ô trong lưới

        Args:
            pos (tuple[int, int]): Vị trí của ô trong lưới

        Returns:
            int: Trọng số của ô
        """
        return self.grid[pos[0]][pos[1]].cost
    
    def get_neighbors(self, pos: tuple[int, int]) -> dict[str, tuple[int,int]]:
        """Xác định các ô kề của một ô

        Args:
            pos (tuple[int, int]): Vị trí của ô trong lưới

        Returns:
            dict[str, tuple[int, int]]: Bản đồ từ hành động đến vị trí của ô kề

        """
        row, col = pos
        action_pos_mapper = {
            "up": (row - 1, col),
            "down": (row + 1, col),
            "left": (row, col - 1),
            "right": (row, col + 1),
        }

        # Xác định các ô kề hợp lệ
        possible_actions = {}
        for action, (r, c) in action_pos_mapper.items():
            if not (0 <= r < self.height and 0 <= c < self.width):
                continue

            if self.grid[r][c].value == "#":
                continue

            possible_actions[action] = (r, c)
        return possible_actions
    
    def is_and_node(self, pos: tuple[int, int]) -> bool:
        """
        Trả về True nếu node tại pos được đánh dấu là AND-node (thuộc tính `is_and` trên Node).
        """
        node = self.get_node(pos)
        return getattr(node, "is_and", False)

    def __repr__(self) -> str:
        return f"Grid([[...], ...], {self.start}, {self.end})"







