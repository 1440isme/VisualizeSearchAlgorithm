"""
Lớp Solution đại diện cho một lời giải (solution) cho bài toán tìm đường
"""

class Solution:
    def __init__(self, path: list[tuple[int,int]], explored: list[tuple[int,int]], time: float = 0, path_cost: int = 0) -> None:
        self.path = path #Lưu lại đường đi
        self.path_cost = path_cost # Lưu lại chi phí của đường đi
        self.path_length = len(path) # Độ dài đường đi, tính bằng số phần tử trong path 
        self.explored = explored # Lưu lại các ô đã duyệt
        self.explored_length = len(explored) # Độ dài của explored, tính bằng số phần tử trong explored
        self.time = time # Thời gian thực thi để tìm ra lời giải

    def __repr__(self) -> str:
        return (f"Solution([{self.path[0]}, ..., {self.path[-1]}],"
                f" {'{...}'}, {self.time})")
    
class NoSolution(Solution):
    """Lớp NoSolution kế thừa từ lớp Solution và được sử dụng để biểu diễn trường hợp không tìm được đường đi (lời giải rỗng)."""
    
    def __repr__(self) -> str:
        explored = list(self.explored)
        return (f"NoSolution([], {'{'}{explored[0]}, {explored[1]},"
                f" ...{'}'}, {self.time})")