"""
Mô hình "frontirer" dùng để quản lý các nút trong quá trình tìm kiếm. Mô hình bao gồm một lớp cơ sở Frontirer và 3 lớp con kế thừa:
- StackFrontier: lớp con thể hiện một ngăn xếp
- QueueFrontier: lớp con thể hiện một hàng đợi
- PriorityQueueFrontier: lớp con thể hiện một hàng đợi ưu tiên
"""

from heapq import heappush, heappop
from .node import Node

class Frontier:
    def __init__ (self) -> None:
        self.frontier: list[Node] = [] # Danh sách các nút trong frontier, đây còn được gọi là type hinting

    def add(self, node:Node) -> None:
        """Thêm một nút mới vào frontier
        Args:
            node (Node): Nút trong mê cung, tham số node là một đối tượng thuộc lớp Node
        """
        self.frontier.append(node)

    def contains_state(self, state: tuple[int, int]) -> bool:
        """Kiểm tra xem trạng thái state có trong frontier không
        Args:
            state (tuple[int, int]): Trạng thái cần kiểm tra, state là một tuple gồm hai số nguyên, đại diện cho vị trí của một nút trong mê cung hoặc lưới.
        Returns:
            bool: True nếu trạng thái state có trong frontier, ngược lại trả về False
        """
        return any(node.state == state for node in self.frontier)
    
    def isEmpty(self) -> bool:
        """Kiểm tra frontier có rỗng không
        Returns:
            bool: True nếu frontier rỗng, ngược lại trả về False
        """
        return len(self.frontier) == 0
    
    def __repr__(self) -> str: # hàm __repr__ giúp cho việc in ra hoặc hiển thị đối tượng một cách rõ ràng trong quá trình phát triển, bằng cách cho biết tên của lớp đối tượng đó.
        """Trả về một chuỗi biểu diễn của frontier
        Returns:
            str: Chuỗi biểu diễn của frontier
        """
        return f"{self.__class__.__name__} ()"
    
    def __str__(self) -> str:
        """Trả về một chuỗi biểu diễn của frontier
        Returns:
            str: Chuỗi biểu diễn của frontier
        """
        return f"{self.__class__.__name__} => {self.frontier}"
    
class StackFrontier(Frontier):
    def remove(self) -> Node:
        """Loại bỏ phần tử từ ngăn xếp

        Raises:
            Exception: Ngăn xếp rỗng
        Returns:
            Node: Nút (ô trong ma trận)
        """    
        if self.isEmpty():
            return Exception("Frontier đang rỗng")
        else:
            return self.frontier.pop() # Loại bỏ phần tử cuối cùng của ngăn xếp
        
class QueueFrontier(Frontier):
    def remove(self) -> Node:
        """Loại bỏ phần tử từ hàng đợi

        Raises:
            Exception: Hàng đợi rỗng
        Returns:
            Node: Nút (ô trong ma trận)
        """    
        if self.isEmpty():
            return Exception("Frontier đang rỗng")
        else:
            return self.frontier.pop(0) # Loại bỏ phần tử đầu tiên của hàng đợi

class PriorityQueueFrontier(Frontier):
    def __init__ (self):
        self.frontier: list[tuple[int, Node]] = [] # Danh sách các nút trong frontier, mỗi nút được đánh số ưu tiên
    
    def add(self, node: Node, prior: int = 0) -> None:
        """Thêm một nút mới vào frontier
        
        Args:
            node (AStarNode): Nút trong mê cung, tham số node là một đối tượng thuộc lớp Node
            prior (int, optional): Ưu tiên của nút. Mặc định là 0
        """
        heappush(self.frontier, (prior, node))

    def get(self, state: tuple[int, int]) -> Node | None:
        """Lấy nút theo trạng thái, nếu không tìm thấy trả về None
        
        Args:
            state (tuple[int, int]): Trạng thái của nút cần lấy
        
        Returns:
            Node: Nút cần lấy
        """
        for _, node in self.frontier:
            if node.state == state:
                return node
        return None
    
    def pop(self) -> Node:
        """Loại bỏ một nút từ frontier

        Returns:
            AStarNode: Nút cần loại bỏ
        """    
        _, node = heappop(self.frontier)
        return node
        

    