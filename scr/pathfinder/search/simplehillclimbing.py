from ..models.grid import Grid
from ..models.solution import Solution, NoSolution
from typing import List, Tuple

class SimpleHillClimbingSearch:
    @staticmethod
    def _manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Tính Manhattan distance giữa hai điểm."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def search(grid: Grid) -> Solution:
        # Tạo nút xuất phát
        current_node = grid.get_node(pos=grid.start)
        current_h = SimpleHillClimbingSearch._manhattan_distance(grid.start, grid.end)

        # Khởi tạo các trạng thái đã thăm
        explored_states = set([grid.start])

        # Lưu đường đi và chi phí
        path = [grid.start]
        path_cost = 0

        while True:
            # Nếu đạt mục tiêu, trả về lời giải
            if current_node.state == grid.end:
                return Solution(path, list(explored_states), path_cost=path_cost)

            # Lấy các hàng xóm
            neighbors = list(grid.get_neighbors(current_node.state).items())

            # Kiểm tra hàng xóm đầu tiên có tốt hơn không
            next_node = None
            next_action = None
            next_h = float('inf')

            for action, state in neighbors:
                if state in explored_states:
                    continue
                h = SimpleHillClimbingSearch._manhattan_distance(state, grid.end)
                if h < current_h:
                    next_h = h
                    next_node = grid.get_node(pos=state)
                    next_node.parent = current_node
                    next_node.action = action
                    next_action = action
                    break  # Chỉ lấy hàng xóm đầu tiên tốt hơn

            if next_node is None:
                return NoSolution(path, list(explored_states))

            # Cập nhật nút hiện tại
            current_node = next_node
            current_h = next_h
            explored_states.add(current_node.state)
            path.append(current_node.state)
            path_cost += grid.get_cost(current_node.state)