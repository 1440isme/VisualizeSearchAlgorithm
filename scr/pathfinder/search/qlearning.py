from ..models.grid import Grid
from ..models.solution import NoSolution, Solution
import numpy as np
import random

class QLearning:
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

    @staticmethod
    def search(grid: Grid, learning_rate=0.1, discount_factor=0.9, epsilon=0.1, episodes=50) -> Solution:
        """Tìm đường đi giữa hai điểm trong lưới bằng thuật toán Q-learning

        Args:
            grid (Grid): Lưới các điểm
            learning_rate (float): Tốc độ học
            discount_factor (float): Hệ số chiết khấu
            epsilon (float): Xác suất khám phá
            episodes (int): Số lượng tập huấn luyện

        Returns:
            Solution: Giải pháp tìm được
        """
        # Khởi tạo bảng Q với giá trị 0
        q_table = {}
        explored = []
        best_path = None
        best_path_length = float('inf')
        consecutive_successes = 0
        
        # Tính toán kích thước mê cung để điều chỉnh tham số
        maze_size = grid.width * grid.height
        max_steps = min(maze_size * 2, 1000)  # Giới hạn số bước tối đa
        
        # Huấn luyện Q-learning
        for episode in range(episodes):
            current_state = grid.start
            done = False
            path = [current_state]
            steps = 0
            visited = set([current_state])  # Theo dõi các trạng thái đã thăm
            
            while not done and steps < max_steps:
                steps += 1
                
                # Epsilon-greedy strategy với epsilon giảm dần
                current_epsilon = epsilon * (1 - episode/episodes)
                if random.random() < current_epsilon:
                    actions = list(grid.get_neighbors(current_state).keys())
                    if not actions:
                        break
                    action = random.choice(actions)
                else:
                    if current_state not in q_table:
                        q_table[current_state] = {a: 0 for a in grid.get_neighbors(current_state).keys()}
                    if not q_table[current_state]:
                        break
                    action = max(q_table[current_state].items(), key=lambda x: x[1])[0]
                
                next_state = grid.get_neighbors(current_state)[action]
                
                # Kiểm tra nếu đã thăm trạng thái này quá nhiều lần
                if next_state in visited and len(visited) > 2:
                    reward = -50  # Phạt nặng cho việc lặp lại trạng thái
                else:
                    visited.add(next_state)
                    path.append(next_state)
                    
                    # Tính toán phần thưởng với heuristic
                    current_dist = QLearning.heuristic(current_state, grid.end)
                    next_dist = QLearning.heuristic(next_state, grid.end)
                    
                    # Phần thưởng cơ bản
                    reward = -1
                    
                    # Thưởng thêm nếu tiến gần hơn đến đích
                    if next_dist < current_dist:
                        reward += 2
                    # Phạt nếu đi xa đích
                    elif next_dist > current_dist:
                        reward -= 2
                
                if next_state == grid.end:
                    reward = 100
                    done = True
                    consecutive_successes += 1
                    
                    # Cập nhật đường đi tốt nhất
                    if len(path) < best_path_length:
                        best_path = path.copy()
                        best_path_length = len(path)
                elif grid.get_node(next_state).value == "#":
                    reward = -100
                    break
                
                # Cập nhật bảng Q
                if current_state not in q_table:
                    q_table[current_state] = {a: 0 for a in grid.get_neighbors(current_state).keys()}
                if next_state not in q_table:
                    q_table[next_state] = {a: 0 for a in grid.get_neighbors(next_state).keys()}
                
                old_value = q_table[current_state][action]
                next_max = max(q_table[next_state].values()) if q_table[next_state] else 0
                new_value = (1 - learning_rate) * old_value + learning_rate * (reward + discount_factor * next_max)
                q_table[current_state][action] = new_value
                
                current_state = next_state
                if current_state not in explored:
                    explored.append(current_state)
            
            # Dừng sớm nếu đã tìm thấy đường đi tốt
            if best_path is not None:
                break
        
        # Sử dụng đường đi tốt nhất đã tìm được
        if best_path is not None:
            cells = best_path
            path_cost = sum(grid.get_cost(cell) for cell in cells[1:])
            return Solution(cells, explored, path_cost=path_cost)
        
        # Nếu không tìm thấy đường đi tốt nhất, thử tìm đường đi từ bảng Q
        current_state = grid.start
        cells = [current_state]
        path_cost = 0
        visited = set([current_state])
        
        while current_state != grid.end and len(cells) < max_steps:
            if current_state not in q_table or not q_table[current_state]:
                return NoSolution([], explored)
            
            # Chọn hành động tốt nhất dựa trên Q-value và heuristic
            actions = q_table[current_state]
            best_action = None
            best_value = float('-inf')
            
            for action, q_value in actions.items():
                next_state = grid.get_neighbors(current_state)[action]
                if next_state in visited:
                    continue
                    
                heuristic_value = -QLearning.heuristic(next_state, grid.end)
                total_value = q_value + 0.1 * heuristic_value
                
                if total_value > best_value:
                    best_value = total_value
                    best_action = action
            
            if best_action is None:
                return NoSolution([], explored)
                
            next_state = grid.get_neighbors(current_state)[best_action]
            visited.add(next_state)
            cells.append(next_state)
            path_cost += grid.get_cost(next_state)
            current_state = next_state
        
        if current_state != grid.end:
            return NoSolution([], explored)
            
        return Solution(cells, explored, path_cost=path_cost) 