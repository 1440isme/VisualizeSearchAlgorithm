"""
Levels management for maze game
Provides level definitions with increasing difficulty
"""
import random
from typing import Callable, Dict, List, Tuple
import sys
import os

# Add the parent directory to sys.path to import constants
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from scr.constants import MAZE_WIDTH, MAZE_HEIGHT, CELL_SIZE

# Define level settings with progression
LEVELS = [
    {
        "id": 1,
        "name": "Tutorial",
        "description": "Simple maze - Learn the basics",
        "algorithm": "Randomised DFS",
        "time_limit": 30,
        "maze_size_factor": 0.4,  # 40% of maximum size
        "unlocked": True  # First level is always unlocked
    },
    {
        "id": 2,
        "name": "Beginner",
        "description": "A more complex path-finding challenge",
        "algorithm": "Randomised DFS",
        "time_limit": 60,
        "maze_size_factor": 0.55,  # 55% of maximum size
        "unlocked": True  # Mở khóa sẵn level 2
    },
    {
        "id": 3,
        "name": "Intermediate",
        "description": "More complex paths and labyrinths",
        "algorithm": "Randomised DFS",
        "time_limit": 80,
        "maze_size_factor": 0.7,  # 70% of maximum size
        "unlocked": False
    },
    {
        "id": 4,
        "name": "Advanced",
        "description": "Challenging maze with complex paths",
        "algorithm": "Randomised DFS",
        "time_limit": 130,
        "maze_size_factor": 0.85,  # 85% of maximum size
        "unlocked": False
    },
    {
        "id": 5,
        "name": "Expert",
        "description": "Complex and challenging labyrinth",
        "algorithm": "Randomised DFS",
        "time_limit": 150,
        "maze_size_factor": 1.0,  # 100% of maximum size (full size)
        "unlocked": False
    }
]

# Maximum maze dimensions (dynamically calculated based on constants)
MAX_MAZE_WIDTH = MAZE_WIDTH // CELL_SIZE
MAX_MAZE_HEIGHT = MAZE_HEIGHT // CELL_SIZE

# Make sure dimensions are odd (for maze generation)
if MAX_MAZE_WIDTH % 2 == 0:
    MAX_MAZE_WIDTH -= 1
if MAX_MAZE_HEIGHT % 2 == 0:
    MAX_MAZE_HEIGHT -= 1

class LevelManager:
    def __init__(self):
        self.levels = LEVELS
        self.current_level_id = 1
        self.max_unlocked_level = 1
        self.level_completed = {level["id"]: False for level in LEVELS}
    
    def get_current_level(self):
        """Get the current level data"""
        for level in self.levels:
            if level["id"] == self.current_level_id:
                return level
        return self.levels[0]  # Default to first level
    
    def set_current_level(self, level_id):
        """Set the current level by id"""
        if 1 <= level_id <= len(self.levels) and level_id <= self.max_unlocked_level:
            self.current_level_id = level_id
            return True
        return False
    
    def complete_level(self, level_id):
        """Mark a level as completed and unlock the next level"""
        self.level_completed[level_id] = True
        
        # Unlock the next level if there is one
        if level_id < len(self.levels):
            next_level = level_id + 1
            for level in self.levels:
                if level["id"] == next_level:
                    level["unlocked"] = True
                    
            # Update max unlocked level
            self.max_unlocked_level = max(self.max_unlocked_level, next_level)
    
    def get_level_progress(self):
        """Get overall game progress percentage"""
        completed_levels = sum(1 for level_id, completed in self.level_completed.items() if completed)
        return (completed_levels / len(self.levels)) * 100
    
    def get_maze_size_for_current_level(self):
        """Get the appropriate maze size for the current level"""
        current_level = self.get_current_level()
        size_factor = current_level.get("maze_size_factor", 1.0)
        
        width = int(MAX_MAZE_WIDTH * size_factor)
        height = int(MAX_MAZE_HEIGHT * size_factor)
        
        # Ensure minimum dimensions
        width = max(width, 10)
        height = max(height, 10)
        
        return width, height
        

    
    def is_near_start_or_goal(self, pos, width, height):
        row, col = pos
        
        # Start is typically at 1/4 of the width
        start_col = width // 4
        start_row = height // 2
        
        # Goal is typically at 3/4 of the width
        goal_col = width - width // 4 - 1
        goal_row = height // 2
        
        # Check if position is within 3 cells of start or goal
        start_dist = abs(row - start_row) + abs(col - start_col)
        goal_dist = abs(row - goal_row) + abs(col - goal_col)
        
        return start_dist < 3 or goal_dist < 3