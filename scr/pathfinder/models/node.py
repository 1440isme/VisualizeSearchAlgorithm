"""
Đoạn code định nghĩa lớp Node.
Chứa các thông tin cần thiết để mô tả một ô trong lưới, hỗ trợ truy vết đường đi và so sánh giữa các nút
"""
#giúp cho việc sử dụng chú thích kiểu trong Python trở nên linh hoạt hơn, đặc biệt là trong các tình huống cần tham chiếu đến các lớp hoặc kiểu mà chưa được định nghĩa hoàn toàn.
from __future__ import annotations 

class Node:
    def __init__(self, value: str, state: tuple[int, int], cost: int, parent: Node | None = None, action: str | None = None) -> None:
        self.value = value # Giá trị của ô trong lưới
        self.state = state
        self.cost = cost # Chi phí để đến ô này
        self.parent = parent
        self.action = action
        self.estimated_distance = float("inf") # Khoảng cách ước lượng từ ô này đến đích, (A* search)
    
    # Phương thức __lt__ (less-than) sử dụng ss hai node. 
    # Nếu estimated_distance của node hiện tại bằng vô cùng thì so sánh state của hai node, ngược lại so sánh estimated_distance của hai node.
    def __lt__(self, other:Node) -> bool:
        if self.estimated_distance == float("inf"):
            return self.state < other.state
        return self.estimated_distance < other.estimated_distance
    
    def __repr__(self) -> str:
        """Trả về một chuỗi biểu diễn của node"""
        return f"Node({self.state!r}, Node(...), {self.action!r})"
        
