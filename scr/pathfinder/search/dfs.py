from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Tìm đường đi giữa hai điểm trong lưới bằng thuật toán Tìm kiếm Theo Chiều Sâu

        Args:
            grid (Grid): Lưới các điểm
            callback (Optional[Visualiser], optional): Hàm gọi lại để 
            trực quan hóa. Mặc định là None.

        Returns:
            Solution: Giải pháp tìm được
        """
        # Tạo nút cho ô nguồn
        node = grid.get_node(pos=grid.start)

        # Khởi tạo Frontier và thêm nút vào đó
        frontier = StackFrontier()
        frontier.add(node)

        # Theo dõi các vị trí đã khám phá
        explored_states = {}

        while True:
            # Trả về đối tượng Solution rỗng nếu không có giải pháp
            if frontier.is_empty():
                return NoSolution([], list(explored_states))

            # Lấy nút ra khỏi frontier
            node = frontier.remove()

            # Thêm vị trí của nút hiện tại vào tập đã khám phá
            explored_states[node.state] = True

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

                return Solution(
                    cells, list(explored_states), path_cost=path_cost)

            # Xác định các hành động có thể thực hiện
            for action, state in grid.get_neighbors(node.state).items():
                if state in explored_states or frontier.contains_state(state):
                    continue

                new = grid.get_node(pos=state)
                new.parent = node
                new.action = action

                frontier.add(node=new)
