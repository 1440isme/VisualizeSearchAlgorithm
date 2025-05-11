from ..models.grid import Grid
from ..models.solution import Solution, NoSolution
from typing import List, Tuple, Dict

class BacktrackingCSPSearch:
    @staticmethod
    def _manhattan_distance(pos1: Tuple[int, int], pos2: Tuple[int, int]) -> int:
        """Tính Manhattan distance giữa hai điểm."""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def search(grid: Grid, max_steps: int = 1000) -> Solution:
        """Tìm đường đi sử dụng Backtracking CSP."""
        # Khởi tạo các trạng thái đã thăm toàn cục
        explored_states = set()

        # Lưu đường đi ban đầu
        path = [grid.start]
        path_cost = 0

        # Gọi hàm đệ quy để tìm đường đi
        result = BacktrackingCSPSearch._backtrack(grid, path, path_cost, explored_states, max_steps)

        if result is None:
            return NoSolution(path, list(explored_states))
        
        final_path, final_path_cost = result
        return Solution(final_path, list(explored_states), path_cost=final_path_cost)

    @staticmethod
    def _backtrack(grid: Grid, path: List[Tuple[int, int]], path_cost: int, 
                   explored_states: set, max_steps: int) -> Tuple[List[Tuple[int, int]], int] | None:
        """Hàm đệ quy Backtracking để tìm đường đi."""
        # Kiểm tra giới hạn bước
        if len(path) > max_steps:
            return None

        # Nếu ô hiện tại là mục tiêu, trả về đường đi và chi phí
        current_pos = path[-1]
        if current_pos == grid.end:
            return path, path_cost

        # Lấy các hàng xóm và sắp xếp theo heuristic
        neighbors = list(grid.get_neighbors(current_pos).items())
        neighbors.sort(key=lambda x: BacktrackingCSPSearch._manhattan_distance(x[1], grid.end))

        # Thử từng ô lân cận
        for action, next_pos in neighbors:
            # Kiểm tra ràng buộc: ô chưa được thăm trong đường đi hiện tại
            if next_pos in path:
                continue

            # Thêm ô vào đường đi và explored_states
            path.append(next_pos)
            explored_states.add(next_pos)
            next_cost = path_cost + grid.get_cost(next_pos)

            # Đệ quy để khám phá tiếp
            result = BacktrackingCSPSearch._backtrack(grid, path, next_cost, explored_states, max_steps)
            if result is not None:
                return result

            # Quay lui: xóa ô khỏi đường đi
            path.pop()
            # Không xóa explored_states để giữ thông tin cho trực quan hóa

        # Không tìm thấy giải pháp từ trạng thái hiện tại
        return None