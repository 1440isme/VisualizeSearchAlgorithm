from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import Solution, NoSolution
from typing import List, Dict, Tuple

class AndOrSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        # Tạo nút xuất phát (OR node)
        start_node = grid.get_node(pos=grid.start)
        start_node.is_and = False  # Đánh dấu là OR node

        # Khởi tạo hàng đợi frontier (chứa các nút OR)
        frontier = QueueFrontier()
        frontier.add(start_node)

        # Khởi tạo các trạng thái đã thăm
        explored_states = set()

        # Lưu trữ cấu trúc cây AND-OR để truy vết
        and_or_tree = {}  # state -> {action: [child_states]}

        while True:
            # Nếu frontier rỗng thì không tìm được lời giải
            if frontier.is_empty():
                return NoSolution([], list(explored_states))

            # Lấy nút từ frontier
            node = frontier.remove()

            # Nếu trạng thái đã được thăm, bỏ qua
            if node.state in explored_states:
                continue

            # Đánh dấu trạng thái hiện tại là đã thăm
            explored_states.add(node.state)

            # Nếu nút hiện tại là mục tiêu, xây dựng lời giải
            if node.state == grid.end:
                path, path_cost = AndOrSearch._build_solution(grid, and_or_tree, node)
                return Solution(path, list(explored_states), path_cost=path_cost)

            # Xác định loại nút (AND hay OR)
            is_and_node = grid.is_and_node(node.state) if hasattr(grid, 'is_and_node') else False

            # Lấy các hàng xóm
            neighbors = grid.get_neighbors(node.state).items()

            if is_and_node:
                # AND node: Phải khám phá TẤT CẢ các hàng xóm
                child_states = []
                for action, state in neighbors:
                    if state in explored_states or frontier.contains_state(state):
                        continue
                    child_node = grid.get_node(pos=state)
                    child_node.parent = node
                    child_node.action = action
                    child_node.is_and = False  # Hàng xóm của AND node là OR node
                    frontier.add(child_node)
                    child_states.append(state)
                # Lưu vào cây AND-OR
                if child_states:
                    and_or_tree[node.state] = {action: child_states for action, _ in neighbors}
            else:
                # OR node: Chọn một hàng xóm để khám phá
                for action, state in neighbors:
                    if state in explored_states or frontier.contains_state(state):
                        continue
                    child_node = grid.get_node(pos=state)
                    child_node.parent = node
                    child_node.action = action
                    child_node.is_and = grid.is_and_node(state) if hasattr(grid, 'is_and_node') else False
                    frontier.add(child_node)
                    # Lưu vào cây AND-OR
                    and_or_tree[node.state] = and_or_tree.get(node.state, {})
                    and_or_tree[node.state][action] = [state]

    @staticmethod
    def _build_solution(grid: Grid, and_or_tree: Dict, goal_node) -> Tuple[List, int]:
        """
        Truy vết từ goal_node để xây dựng đường đi và tính chi phí.
        """
        path = []
        path_cost = 0
        current = goal_node

        # Truy vết ngược từ goal về start
        while current.state != grid.start:
            path.append(current.state)
            path_cost += grid.get_cost(current.state)
            current = current.parent

        path.append(grid.start)
        path.reverse()

        return path, path_cost