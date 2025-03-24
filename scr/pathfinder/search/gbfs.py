from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution

class GBFS:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Tìm đường đi giữa hai điểm trong một lưới sử dụng thuật toán A* Search

        Args:
            grid (Grid): Lưới các điểm
            callback (Optional[Visualiser], optional): Hàm callback để trực quan hóa. Mặc định là None.

        Returns:
            Solution: Lời giải tìm được
        """
        # Khởi tạo nút bắt đầu 
        node = grid.get_node(pos=grid.start)

        # Khởi tạo hàng đợi ưu tiên PriorityQueueFrontier và thêm nút bắt đầu vào hàng đợi
        frontier = PriorityQueueFrontier()
        frontier.add(node, prior=GBFS.heuristic(grid.start, grid.end))

        # lưu trữ chi phí từ điểm bắt đầu đến mỗi nút đã duyệt (G-score)
        cost_so_far = {grid.start: 0}

        explored = [] # Lưu trữ các nút đã duyệt

        while True:
            # Nếu frontier rỗng thì không tìm được lời giải
            if frontier.isEmpty():
                return NoSolution([], list(explored))
            
            # Lấy nút từ frontier
            node = frontier.pop()
            if node.state not in explored:
                explored.append(node.state)

            # Nếu nút hiện tại là nút kết thúc thì trả về lời giải
            if node.state == grid.end:
                # Truy vết đường đi
                cells = []
                path_cost = 0
                tmp = node

                while tmp.parent is not None:
                    cells.append(tmp.state)
                    path_cost += tmp.cost
                    tmp = tmp.parent
                cells.append(grid.start)
                cells.reverse()

                return Solution(cells, list(explored), path_cost)
            
            # Mở rộng các nút kề
            for action, state in grid.get_neighbors(node.state).items():
                new_cost = cost_so_far[node.state] + grid.get_cost(state)

                if state not in cost_so_far or new_cost < cost_so_far[state]:
                    cost_so_far[state] = new_cost

                    # Tạo nút con
                    n = grid.get_node(pos=state)
                    n.parent = node
                    n.estimated_distance = GBFS.heuristic(state, grid.end)

                    if not n.action:
                        n.action = action
                    
                    frontier.add(node=n, prior=GBFS.heuristic(state, grid.end))

    @staticmethod
    def heuristic(state: tuple[int,int], goal: tuple[int,int]) -> int:
        """Hàm ước lượng khoảng cách từ một điểm đến điểm đích

        Args:
            state (tuple[int,int]): Vị trí hiện tại
            goal (tuple[int,int]): Vị trí đích

        Returns:
            int: Khoảng cách ước lượng
        """

        x1, y1 = state
        x2, y2 = goal

        return abs(x1 - x2) + abs(y1 - y2)