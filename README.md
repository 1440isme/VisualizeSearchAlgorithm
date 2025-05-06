# VisualizeSearchAlgorithm

Ứng dụng trực quan hóa các thuật toán tìm đường trong mê cung với giao diện hiện đại, được phát triển bằng Python và Pygame.

## Mô tả

Đây là ứng dụng trực quan hóa các thuật toán tìm đường mê cung, cho phép người dùng thấy được cách thức hoạt động của các thuật toán AI cơ bản. Ứng dụng cung cấp hai chế độ chính:

1. **Chế độ trực quan hóa (Visualization Mode)**: Hiển thị quy trình tìm kiếm của mỗi thuật toán
2. **Chế độ trò chơi (Game Mode)**: Cho phép người chơi tự di chuyển trong mê cung với các cấp độ khó tăng dần

## Tính năng

### Chế độ trực quan hóa

- Trực quan hóa 9 thuật toán tìm đường khác nhau:
  - A* Search (A*)
  - Dijkstra's Search (DS)
  - Breadth First Search (BFS)
  - Depth First Search (DFS)
  - Greedy Best First Search (GBFS)
  - Uniform Cost Search (UCS)
  - Iterative Deepening DFS (IDDFS)
  - Iterative Deepening A* (IDA*)
  - Beam Search (BEAM)
- Điều chỉnh tốc độ trực quan hóa (Fast, Medium, Slow)
- So sánh hiệu suất giữa các thuật toán
- Tạo mê cung bằng nhiều thuật toán khác nhau:
  - Recursive Division
  - Prim's Algorithm
  - Randomised DFS
  - Basic Random Maze
  - Basic Weight Maze
- Tùy chỉnh vị trí điểm bắt đầu và điểm đích
- Thêm tường và các ô có trọng số khác nhau

### Chế độ trò chơi

- 5 cấp độ với độ khó tăng dần
- Điều khiển nhân vật với các phím WASD hoặc phím mũi tên
- Giới hạn thời gian cho mỗi cấp độ
- Tự động tạo mê cung thử thách
- Tính năng tự động giải mê cung (Auto Solve)

## Cài đặt

1. Cần cài đặt Python 3.x
2. Cài đặt các thư viện phụ thuộc:

```
pip install pygame
```

## Chạy ứng dụng

```
python run.pyw
```

Tùy chọn: Có thể thay đổi kích thước ô mê cung bằng cách sử dụng tham số `--cell-size`:

```
python run.pyw --cell-size:20
```

## Hướng dẫn sử dụng

### Menu chính

- Chọn **Visualization Mode** để trực quan hóa thuật toán
- Chọn **Game Mode** để chơi trò chơi mê cung

### Chế độ trực quan hóa

1. Chọn thuật toán từ menu **Algorithms**
2. Chọn tốc độ trực quan hóa từ menu **Fast**
3. Nhấn nút **VISUALISE** để bắt đầu trực quan hóa
4. Sử dụng nút **Run All** để so sánh các thuật toán
5. Nhấn nút **Generate Maze** để tạo mê cung mới
6. Nhấn nút **?** để xem chú thích các ký hiệu

### Chế độ trò chơi

1. Di chuyển bằng phím WASD hoặc phím mũi tên
2. Tìm đường đến đích trước khi hết thời gian
3. Sử dụng **Challenging Map** để tạo mê cung khó hơn
4. Sử dụng **Auto Solve** để xem giải pháp
5. Sau khi hoàn thành 5 level, nhấn Space để quay lại level 1

## Các thuật toán tìm đường

### A\* Search

Kết hợp chi phí đường đi thực tế (g) và heuristic (h) để tìm đường đi ngắn nhất.

### Dijkstra's Search

Thuật toán tìm đường đi ngắn nhất, không sử dụng heuristic.

### Breadth First Search

Tìm kiếm theo chiều rộng, đảm bảo tìm được đường đi ngắn nhất trong mê cung không có trọng số.

### Depth First Search

Tìm kiếm theo chiều sâu, không đảm bảo đường đi ngắn nhất nhưng thường tiêu tốn ít bộ nhớ.

### Greedy Best First Search

Chỉ dựa vào heuristic để tìm đường đi, không xem xét chi phí thực tế.

### Uniform Cost Search

Mở rộng các nút có chi phí thực tế thấp nhất, đảm bảo tìm được đường đi tối ưu.

### Iterative Deepening DFS

Kết hợp chiều sâu giới hạn và tăng dần giới hạn, đảm bảo tìm được đường đi ngắn nhất với ít bộ nhớ.

### Iterative Deepening A\*

Kết hợp IDDFS với A\*, cải thiện hiệu suất không gian.

### Beam Search

Giới hạn số nút khám phá trong mỗi bước, giúp tăng tốc độ tìm kiếm.

## Thuật toán tạo mê cung

### Recursive Division

Đệ quy chia không gian thành các khu vực nhỏ hơn và tạo tường giữa chúng.

### Prim's Algorithm

Thuật toán tạo cây khung nhỏ nhất ngẫu nhiên để tạo mê cung.

### Randomised DFS

Sử dụng DFS với lựa chọn ngẫu nhiên để tạo mê cung.

### Basic Random Maze

Tạo mê cung hoàn toàn ngẫu nhiên.

### Basic Weight Maze

Tạo mê cung với các ô có trọng số khác nhau.
