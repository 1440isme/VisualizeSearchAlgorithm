from ..models.grid import Grid
from ..models.solution import NoSolution, Solution
from ..models.node import Node
import heapq

class BeamSearch:
    @staticmethod
    def search(grid: Grid, beam_width: int = 10) -> Solution:
        start_node = grid.get_node(pos=grid.start)
        goal = grid.end

        frontier = [(BeamSearch.heuristic(grid.start, goal), start_node)]
        explored = []
        visited_set = set()

        while frontier:
            next_frontier = []

            # Duyệt các node trong frontier hiện tại
            for _, node in frontier:
                if node.state in visited_set:
                    continue
                visited_set.add(node.state)
                explored.append(node.state)

                if node.state == goal:
                    return BeamSearch.reconstruct_path(node, explored)

                for action, neighbor in grid.get_neighbors(node.state).items():
                    if neighbor not in visited_set:
                        child = grid.get_node(pos=neighbor)
                        child.parent = node
                        child.action = action
                        h = BeamSearch.heuristic(neighbor, goal)
                        heapq.heappush(next_frontier, (h, child))

            # Chỉ giữ lại `beam_width` node tốt nhất
            frontier = heapq.nsmallest(beam_width, next_frontier)

        return NoSolution([], explored)

    @staticmethod
    def heuristic(pos1, pos2):
        # Sử dụng khoảng cách Manhattan
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    @staticmethod
    def reconstruct_path(node, explored):
        path = []
        while node.parent is not None:
            path.append(node.state)
            node = node.parent
        path.append(node.state)
        path.reverse()
        return Solution(path, explored, path_cost=len(path) - 1)
