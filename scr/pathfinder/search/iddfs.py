from ..models.grid import Grid
from ..models.solution import NoSolution, Solution
from ..models.node import Node

class IterativeDeepeningSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """
        Tìm đường đi bằng thuật toán IDDFS (Iterative Deepening Depth-First Search)
        """
        max_depth = grid.width * grid.height  # đảm bảo thử đủ sâu (sử dụng width và height từ Grid)
        explored_total = set()

        for depth in range(1, max_depth + 1):
            visited = set()
            result = IterativeDeepeningSearch._dls(
                grid, grid.start, depth, visited, parent=None
            )
            explored_total.update(visited)

            if isinstance(result, Solution):
                result.explored = list(explored_total)
                return result

        return NoSolution([], list(explored_total))

    @staticmethod
    def _dls(grid: Grid, current, depth, visited, parent):
        visited.add(current)

        if current == grid.end:
            path = []
            node = parent or grid.get_node(pos=current)
            while node:
                path.append(node.state)
                node = node.parent
            path.reverse()
            return Solution(path, visited, path_cost=len(path)-1)

        if depth <= 0:
            return None

        for action, neighbor in grid.get_neighbours(current).items():
            if neighbor not in visited:
                node = grid.get_node(pos=neighbor)
                node.parent = grid.get_node(pos=current)
                node.action = action
                result = IterativeDeepeningSearch._dls(
                    grid, neighbor, depth - 1, visited, node
                )
                if result:
                    return result

        return None