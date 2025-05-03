from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import Solution, NoSolution

class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        # tạo nút xuất phát
        node = grid.get_node(pos = grid.start)

        # khởi tạo hàng đợi frontier
        frontier = QueueFrontier()
        frontier.add(node)

        # khởi tạo các trạng thái đã thăm
        explored_states = {}

        while True:
            # Nếu frontier rỗng thì không tìm được lời giải
            if frontier.is_empty():
                return NoSolution([], list(explored_states))

            # Lấy nút từ frontier
            node = frontier.remove()

            # Đánh dấu nút hiện tại là đã thăm
            explored_states[node.state] = True

            # Nếu nút hiện tại là nút kết thúc thì trả về lời giải
            if node.state == grid.end:
                
                # Truy vết đường đi
                path = []  # Tạo danh sách để lưu trữ các vị trí của đường đi.
                path_cost = 0
                current = node

                while current != grid.get_node(pos=grid.start):
                    path.append(current.state)
                    path_cost += grid.get_cost(current.state)
                    current = current.parent

                path.append(grid.start)
                path.reverse()

                return Solution(path, list(explored_states), path_cost=path_cost)
            
            # Mở rộng các nút kề
            for action, state in grid.get_neighbors(node.state).items():
                # Bỏ qua các ô đã duyệt hoặc nằm trong frontier
                if state in explored_states or frontier.contains_state(state):
                    continue
                
                # Tạo nút con
                new = grid.get_node(pos=state)
                new.parent = node
                new.action = action
                frontier.add(node=new)  # Thêm nút con vào frontier

