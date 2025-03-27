from ..models.frontier import PriorityQueueFrontier
from ..models.grid import Grid
from ..models.solution import NoSolution, Solution


class DijkstrasSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Tìm đường đi giữa hai điểm trong lưới bằng thuật toán A* Search

        Args:
            grid (Grid): Lưới các điểm
            callback (Optional[Visualiser], optional): Hàm callback để trực quan hóa. Mặc định là None.

        Returns:
            Solution: Giải pháp tìm được
        """

        # Tạo Node cho ô nguồn
        node = grid.get_node(pos=grid.start)

        # Khởi tạo hàng đợi ưu tiên và thêm node vào
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        # Theo dõi điểm G (khoảng cách)
        distance = {grid.start: 0}

        explored = []

        while True:
            # Trả về đối tượng Solution rỗng nếu không có giải pháp
            if frontier.is_empty():
                return NoSolution([], explored)

            # Lấy node ra khỏi hàng đợi
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
            for action, state in grid.get_neighbours(node.state).items():
                cost = distance[node.state] + grid.get_cost(state)

                if state not in distance or cost < distance[state]:
                    distance[state] = cost

                    n = grid.get_node(pos=state)
                    n.parent = node

                    if not n.action:
                        n.action = action

                    frontier.add(
                        node=n,
                        priority=cost
                    )