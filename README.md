# Pikachu AI — README

## 1. Tổng quan dự án trò chơi 

Dự án trò chơi nối thú Pikachu là trò chơi tìm và nối hai hình giống nhau sao cho đường nối giữa 2 hình là 3 đoạn thẳng, tức 2 lần rẽ 
Các thuật toán dùng để tìm
- BFS
- DFS 
- A* 
- Greedy
- Hill Climbing 
- Beam Search
- Backtracking 
- Forward Checking Backtracking 
- MU_1_PHAN 
- MU_TOAN_PHAN 

## 2. Cấu trúc thư mục & file quan trọng

- `UI.py` — giao diện chính, danh sách thuật toán, gọi hàm tự động (Tu_Dong*, Tu_Dong_BFS*), vẽ bảng và animation.
- `BFS.py`, `DFS.py` — Hai file này sẽ thực hiện nhóm tìm kiếm không thông tin thực hai thuật toán BFS và DFS 
- `A_SAO.py` — A* sử dụng heuristic Manhattan và cost so với vị trí ban đầu để tính chi phí; lưu đường đi và cost list để vẽ.
- `Greedy.py` — thuật toán greedy dựa trên heuristic Manhattan (chỉ f = h).
- `HILL_CLAMBING.py` — hill climbing với điều kiện chỉ chấp nhận trạng thái không tăng heuristic; giới hạn số lần rẽ.
- `BEAM_SEARCH.py` — beam search giữ beam_width trạng thái tốt nhất theo f=h.
- `BK.py` — backtracking, kiểm tra ràng buộc hướng và số lần rẽ tối đa.
- `Foward_Checking.py` — backtracking có forward checking (loại trừ vị trí không hợp lệ trước khi mở rộng).
- `MU_1_PHAN.py`, `MU_TOAN_PHAN.py` — agent dùng niềm tin (belief) để suy đoán vị trí giống nhau rồi thử mở.
- Tài nguyên ảnh và âm thanh (các file .png, .jpg, .wav) được load bởi UI.
## 3. Mô tả chi tiết từng thuật toán

### BFS (Breadth-First Search)

Ý tưởng: Thuật toán BFS mở rộng các ô theo từng lớp để đảm bảo tìm được đường đi ngắn nhất giữa hai ô giống nhau. Mỗi trạng thái lưu giá trị,vị trí, số lần rẽ và hướng đi hiện tại. Khi mở rộng, chỉ xét các ô trống hoặc ô đích hợp lệ, không được quay ngược và số lần rẽ không vượt quá 2. BFS sử dụng hàng đợi để duyệt theo lớp, lưu cha để truy vết đường đi. Khi đạt trạng thái đích, thuật toán trả về danh sách tọa độ tạo thành đường nối hợp lệ hoặc trả về None

Đầu vào: trạng thái ban đầu `(value,(x,y),turn,dir)` và trạng thái đích. Trả về path (danh sách toạ độ).

### DFS (Depth-First Search)

Ý tưởng: Thuật toán DFS mở rộng các ô theo chiều sâu, đi càng xa càng tốt tức là duyệt 1 nhánh đến khi nào hết nhánh ta quay lại nhánh khác. Mỗi trạng thái lưu giá trị, vị trí, số lần rẽ và hướng đi hiện tại. Khi mở rộng, chỉ xét ô trống hoặc ô đích có cùng giá trị, không quay ngược tức là không đi hướng ngược lại và không vượt quá 2 lần rẽ. DFS sử dụng ngăn xếp để duyệt, lưu cha để truy vết đường đi sau khi tìm thấy đích. Kết quả là một đường nối hợp lệ giữa hai ô cùng giá trị, thỏa ràng buộc về số lần rẽ hoặc None nếu không tìm thấy
### A* (A_SAO.py)
Ý tưởng: Thuật toán A* mở rộng các ô theo thứ tự chi phí ước lượng nhỏ nhất để tìm đường đi tối ưu giữa hai ô giống nhau. Mỗi trạng thái lưu giá trị, vị trí, số lần rẽ và hướng đi. Hàm f = g + h được dùng, trong đó g là chi phí thực từ điểm đầu, h là giá trị heuristic khoảng cách Manhattan đến đích. Khi mở rộng, chỉ xét ô trống hoặc ô đích hợp lệ, không quay hướng ngược lại và rẽ tối đa 2 lần. A* sử dụng hàng đợi ưu tiên (heapq) để chọn trạng thái có chi phí nhỏ nhất, đảm bảo tìm được đường ngắn nhất và hợp lệ. Visited sẽ lưu trạng thái đã sinh ra đồng thời cũng xem trong đó có trạng thái mới nào đã có trong visited mà hàm f nhỏ hơn f trạng thái cũ đã có trong visited không, có ta ta cập nhật và cho vào hàng đợi ưu tiên
### Greedy

Ý tưởng: Giống thuật toán A_Sao nhưng f tính bằng heuristic

### Hill Climbing

Ý tưởng: Thuật toán Hill Climbing chọn bước đi heuristic nhỏ hơn hoặc bằng ở lân cận để tiến gần đích.Trạng thái gồm giá trị, vị trí, số lần rẽ và hướng; chỉ mở các ô trống hoặc ô đích hợp lệ, không quay ngược và rẽ ≤ 2 lần.Tại mỗi bước, duyệt 4 hướng, tính h (Manhattan) và chỉ nhận những nước đi có h <= h_hiện_tại. Dùng hàng đợi ưu tiên theo h để bốc nước đi tốt nhất trước, lưu parent để truy vết đường.Nếu đạt đích trả về đường đi; nếu không còn láng giềng cải thiện → kẹt cực trị cục bộ và dừng.

### Beam Search

Ý tưởng: Thuật toán Beam Search là phiên bản cải tiến của BFS, chỉ giữ lại một số lượng giới hạn các trạng thái “tốt nhất” (theo heuristic nhỏ nhất) tại mỗi bước mở rộng.
Mỗi trạng thái lưu vị trí, hướng đi và số lần rẽ, chỉ xét ô trống hoặc ô đích hợp lệ, không quay ngược và rẽ tối đa 2 lần.
Thuật toán đánh giá mỗi trạng thái bằng h = |x - x_goal| + |y - y_goal| và chọn ra beam_width trạng thái có h nhỏ nhất để tiếp tục mở rộng.
### Backtracking (BK.py)

Ý tưởng: Dùng đệ quy tìm đường, kiểm tra ràng buộc trước khi mở rộng (hướng, số lần rẽ, ô hợp lệ). Có hàm `_is_opposite` để ngăn quay lại trái với hướng trước đó. Có giới hạn đệ quy tức tập biến (lan_lap) để tránh quá sâu, 

### Forward Checking Backtracking (Foward_Checking.py)

Ý tưởng: Trước khi sinh các neighbor sẽ lọc trước những ô có thể đi (forward checking) dựa trên giá trị hay ô trống. Lợi ích: giảm số nhánh không cần thiết.

### MU_TOAN_PHAN (Belief non-local)

Ý tưởng: Mô phỏng agent có niềm tin cho toàn bộ bảng. Niềm tin là tập giá trị có thể xuất hiện ở vị trí đó. Agent quan sát vùng (pham_vi) để cập nhật niềm tin; khi niềm tin cho thấy một loại có 2 hoặc nhiều ô khả dĩ, agent thử suy đoán cặp và kiểm tra xem có thể đi được (sử dụng BFS phiên bản trị belief). Nếu đi được thì ăn cặp (set thành 0).

### MU_1_PHAN (Local belief)

Ý tưởng: Agent có vị trí bắt đầu cụ thể, chỉ quan sát trong phạm vi nhất định và cập nhật niềm tin cục bộ. Khá hữu ích để mô phỏng agent di động khám phá bản đồ dần dần.

## 4. Giao diện người dùng (UI.py)

UI đảm nhiệm:

- Tạo board 10x10 với border padding 1 hàng cột (ma_tran 12x12)
- Vẽ icon, highlight khi hover, vẽ grid.
- Menu chọn thuật toán, HISTORY (ghi file CSV) và OPTIONS.
- Hàm tự động hóa: `Tu_Dong`, `Tu_Dong_1`, `Tu_Dong_BFS_Non`, `Tu_Dong_BFS_1_P` tương ứng với cách gọi thuật toán khác nhau.
- Animation: phương thức `Ve_Simulation` trong các lớp thuật toán thêm các segment để UI vẽ đường giữa các ô khi thử nghiệm.
- Lưu lịch sử chạy (thời gian, bộ nhớ) vào `history.csv` khi pause hoặc hoàn thành level.

### Phím tắt và tương tác
- ESC: thoát game
- P: tạm dừng/resume và ghi lịch sử
- Trong menu: chọn OPTIONS để pick thuật toán, PLAY để chạy


