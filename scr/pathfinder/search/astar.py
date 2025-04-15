from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class AStarSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Tìm đường đi giữa hai điểm trong lưới bằng thuật toán Tìm kiếm A*

        Args:
            grid (Grid): Lưới các điểm
            callback (Optional[Visualiser], optional): Hàm gọi lại để 
            trực quan hóa. Mặc định là None.

        Returns:
            Solution: Giải pháp tìm được
        """
        # Tạo nút cho ô nguồn
        node = grid.get_node(pos=grid.start)

        # Khởi tạo Frontier dạng PriorityQueue và thêm nút vào đó
        frontier = PriorityQueueFrontier()
        frontier.add(
            node,
            priority=AStarSearch.heuristic(grid.start, grid.end)
        )

        # Theo dõi điểm G (khoảng cách từ điểm bắt đầu)
        g_score = {grid.start: 0}
        f_score = {grid.start: AStarSearch.heuristic(grid.start, grid.end)}

        # Theo dõi các nút đã khám phá
        explored = []

        while True:
            # Trả về đối tượng Solution rỗng nếu không có giải pháp
            if frontier.is_empty():
                return NoSolution([], explored)

            # Lấy nút ra khỏi frontier
            node = frontier.pop()
            if node.state not in explored:
                explored.append(node.state)

            # Nếu đã đến điểm đích
            if node.state == grid.end:

                # Tạo đường đi và trả về đối tượng Solution
                cells = []
                path_cost = 0

                temp = node
                while temp.parent != None:
                    cells.append(temp.state)
                    path_cost += temp.cost
                    temp = temp.parent

                cells.append(grid.start)
                cells.reverse()

                return Solution(cells, explored, path_cost=path_cost)

            # Xác định các hành động có thể thực hiện
            for action, state in grid.get_neighbors(node.state).items():
                cost = g_score[node.state] + grid.get_cost(state)

                if state not in g_score or cost < g_score[state]:
                    g_score[state] = cost
                    f_score[state] = cost + \
                        AStarSearch.heuristic(state, grid.end)

                    n = grid.get_node(pos=state)
                    n.parent = node
                    n.estimated_distance = f_score[state] - cost

                    if not n.action:
                        n.action = action

                    frontier.add(
                        node=n,
                        priority=f_score[state]
                    )

    @staticmethod
    def heuristic(state: tuple[int, int], goal: tuple[int, int]) -> int:
        """Hàm heuristic để ước lượng khoảng cách còn lại

        Args:
            state (tuple[int, int]): Điểm ban đầu
            goal (tuple[int, int]): Điểm đích

        Returns:
            int: Khoảng cách
        """
        x1, y1 = state
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)
