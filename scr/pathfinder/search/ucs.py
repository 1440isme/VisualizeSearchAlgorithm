from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution

class UCS:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Tìm đường đi giữa hai điểm trong lưới bằng thuật toán Uniform Cost Search (UCS)

        Args:
            grid (Grid): Lưới các điểm

        Returns:
            Solution: Giải pháp tìm được
        """
        # Khởi tạo nút bắt đầu
        node = grid.get_node(pos=grid.start)

        # Khởi tạo hàng đợi ưu tiên và thêm nút bắt đầu vào
        frontier = PriorityQueueFrontier()
        frontier.add(node, priority=0)

        # Lưu trữ chi phí từ điểm bắt đầu đến mỗi nút đã duyệt
        cost_so_far = {grid.start: 0}

        explored = []  # Lưu trữ các nút đã duyệt

        while True:
            # Nếu frontier rỗng thì không tìm được lời giải
            if frontier.is_empty():
                return NoSolution([], explored)

            # Lấy nút từ frontier
            node = frontier.pop()
            if node.state not in explored:
                explored.append(node.state)

            # Nếu nút hiện tại là nút kết thúc thì trả về lời giải
            if node.state == grid.end:
                # Truy vết đường đi
                cells = []
                path_cost = 0
                temp = node

                while temp.parent is not None:
                    cells.append(temp.state)
                    path_cost += temp.cost
                    temp = temp.parent
                cells.append(grid.start)
                cells.reverse()

                return Solution(cells, explored, path_cost)

            # Mở rộng các nút kề
            for action, state in grid.get_neighbours(node.state).items():
                new_cost = cost_so_far[node.state] + grid.get_cost(state)

                if state not in cost_so_far or new_cost < cost_so_far[state]:
                    cost_so_far[state] = new_cost

                    # Tạo nút con
                    n = grid.get_node(pos=state)
                    n.parent = node
                    n.action = action

                    frontier.add(node=n, priority=new_cost)