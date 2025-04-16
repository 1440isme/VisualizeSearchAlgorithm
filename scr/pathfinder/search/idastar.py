from ..models.grid import Grid
from ..models.solution import NoSolution, Solution
from ..models.node import Node
import heapq

class IterativeDeepeningAStar:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """
        Tìm đường đi bằng thuật toán IDA* (Iterative Deepening A*)
        """
        def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
            return abs(a[0] - b[0]) + abs(a[1] - b[1])  # khoảng cách Manhattan

        start = grid.start
        goal = grid.end
        threshold = heuristic(start, goal)
        explored_total = set()

        while True:
            temp, result, visited = IterativeDeepeningAStar._ida_star(grid, start, goal, 0, threshold, [], set(), heuristic, parent=None)
            explored_total.update(visited)

            if isinstance(result, Solution):
                result.explored = list(explored_total)
                return result
            if temp == float('inf'):
                break
            threshold = temp

        return NoSolution([], list(explored_total))

    @staticmethod
    def _ida_star(grid: Grid, current, goal, g, threshold, path, visited, heuristic, parent):
        f = g + heuristic(current, goal)
        if f > threshold:
            return f, None, visited

        visited.add(current)

        if current == goal:
            full_path = [node.state for node in path] + [goal]
            return f, Solution(full_path, visited, path_cost=len(full_path)-1), visited

        min_cost = float('inf')
        for action, neighbor in grid.get_neighbours(current).items():
            if neighbor not in visited:
                node = grid.get_node(pos=neighbor)
                node.parent = grid.get_node(pos=current) if parent is None else parent
                node.action = action
                path.append(node)

                temp, result, visited = IterativeDeepeningAStar._ida_star(
                    grid, neighbor, goal, g + grid.get_cost(neighbor), threshold, path, visited, heuristic, node
                )
                if isinstance(result, Solution):
                    return temp, result, visited
                if temp < min_cost:
                    min_cost = temp

                path.pop()

        return min_cost, None, visited
