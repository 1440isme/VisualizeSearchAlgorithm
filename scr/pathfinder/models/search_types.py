from enum import Enum


class Search(Enum):
    """Enum for search algorithms"""

    ASTAR_SEARCH = "A*"
    BREADTH_FIRST_SEARCH = "BFS"
    GREEDY_BEST_FIRST_SEARCH = "GBFS"
    DEPTH_FIRST_SEARCH = "DFS"
    UNIFORM_COST_SEARCH = "UCS"
    BEAM_SEARCH = "BEAM"
    AND_OR_SEARCH = "AND-OR"
    BACKTRACKING_SEARCH = "BACKTRACKING"
    QLEARNING_SEARCH = "Q-LEARNING"
