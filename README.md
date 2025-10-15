# Pikachu AI — README

## 1. Tổng quan dự án

Dự án là bộ thuật toán tìm đường và agent chơi trò "Pikachu" (ghép cặp ô). Mỗi thuật toán nằm trong một file riêng và được UI (UI.py) gọi để thực hiện tìm đường hoặc quyết định mở ô. Các thuật toán chính có trong repository:

- BFS (Breadth-First Search)
- DFS (Depth-First Search)
- A* (A_SAO.py)
- Greedy
- Hill Climbing (HILL_CLAMBING.py)
- Beam Search
- Backtracking (BK.py)
- Forward Checking Backtracking (Foward_Checking.py)
- MU_1_PHAN (local belief agent)
- MU_TOAN_PHAN (non-local belief agent)

## 2. Cấu trúc thư mục & file quan trọng

- `UI.py` — giao diện chính, danh sách thuật toán, gọi hàm tự động (Tu_Dong*, Tu_Dong_BFS*), vẽ bảng và animation.
- `BFS.py`, `DFS.py` — các trình duyệt đồ thị cơ bản với ràng buộc tối đa 2 lần rẽ.
- `A_SAO.py` — A* sử dụng heuristic Manhattan; lưu đường đi và cost list để vẽ.
- `Greedy.py` — thuật toán greedy dựa trên heuristic Manhattan (chỉ f = h).
- `HILL_CLAMBING.py` — hill climbing với điều kiện chỉ chấp nhận trạng thái không tăng heuristic; giới hạn số lần rẽ.
- `BEAM_SEARCH.py` — beam search giữ beam_width trạng thái tốt nhất theo f=h.
- `BK.py` — backtracking, kiểm tra ràng buộc hướng và số lần rẽ tối đa.
- `Foward_Checking.py` — backtracking có forward checking (loại trừ vị trí không hợp lệ trước khi mở rộng).
- `MU_1_PHAN.py`, `MU_TOAN_PHAN.py` — agent dùng niềm tin (belief) để suy đoán vị trí giống nhau rồi thử mở.
- Tài nguyên ảnh và âm thanh (các file .png, .jpg, .wav) được load bởi UI.

## 3. Hướng dẫn nhanh cách chạy

1. Chuẩn bị môi trường Python 3.8+
2. Cài thư viện:
   ```
   pip install numpy pygame psutil
   ```
3. Đảm bảo các file ảnh (vd: `bg_menu2.jpg`, `bg.png`, icons) ở cùng thư mục hoặc đường dẫn tương ứng.
4. Chạy:
   ```
   python UI.py
   ```
   Màn hình menu hiện, chọn thuật toán rồi PLAY để chạy tự động.

## 4. Mô tả chi tiết từng thuật toán

### BFS (Breadth-First Search)

Ý tưởng: Mở rộng theo lớp, đảm bảo tìm đường ngắn nhất về số bước (với ràng buộc tối đa 2 lần rẽ). Implement dùng deque. Khi mở node, kiểm tra ràng buộc: ô mới phải là ô trống (0) hoặc là ô mục tiêu có cùng giá trị; không cho quay ngược lại (kiểm tra hướng) và chỉ chấp nhận <=2 lần rẽ.

Đầu vào: trạng thái ban đầu `(value,(x,y),turn,dir)` và trạng thái đích. Trả về path (danh sách toạ độ).

### DFS (Depth-First Search)

Ý tưởng: Duyệt theo ngăn xếp, sử dụng cùng ràng buộc như BFS về hướng và số lần rẽ. DFS dễ rơi vào nhánh sâu; đã có giới hạn số lần lặp trong một số backtracking tùy file.

### A* (A_SAO.py)

Ý tưởng: Dùng hàm f = g + h. g được tính là cost di chuyển (ở đây cost mỗi bước = 1). h là heuristic Manhattan (có hàm Euclid sẵn nhưng không dùng). Visited lưu chi phí tốt nhất đã thấy cho trạng thái để cho phép relax nếu tìm thấy đường tốt hơn. Kết quả trả về cả path và list cost để UI hiển thị giá trị heuristic/g.

### Greedy

Ý tưởng: Lấy f = h (Manhattan). Không bảo đảm tối ưu, nhưng nhanh. Visited lưu h hiện tại để chỉ chấp nhận trạng thái nếu h tốt hơn.

### Hill Climbing

Ý tưởng: Chỉ chấp nhận các bước làm giảm hoặc không tăng giá trị heuristic (càng gần goal càng tốt). Sử dụng heap ưu tiên theo heuristic. Có biến lan_vo để giữ thứ tự ổn định.

### Beam Search

Ý tưởng: Mỗi vòng chỉ giữ `beam_width` trạng thái tốt nhất (theo h). Tạo candidate tiếp theo từ từng trạng thái, gom về beam nhỏ nhất để tiếp tục. Thích hợp giảm mức lan truyền trạng thái.

### Backtracking (BK.py)

Ý tưởng: Dùng đệ quy tìm đường, kiểm tra ràng buộc trước khi mở rộng (hướng, số lần rẽ, ô hợp lệ). Có hàm `_is_opposite` để ngăn quay lại trái với hướng trước đó. Có giới hạn đệ quy (lan_lap) để tránh quá sâu.

### Forward Checking Backtracking (Foward_Checking.py)

Ý tưởng: Trước khi sinh các neighbor sẽ lọc trước những ô có thể đi (forward checking) dựa trên giá trị hay ô trống. Lợi ích: giảm số nhánh không cần thiết.

### MU_TOAN_PHAN (Belief non-local)

Ý tưởng: Mô phỏng agent có niềm tin cho toàn bộ bảng. Niềm tin là tập giá trị có thể xuất hiện ở vị trí đó. Agent quan sát vùng (pham_vi) để cập nhật niềm tin; khi niềm tin cho thấy một loại có 2 hoặc nhiều ô khả dĩ, agent thử suy đoán cặp và kiểm tra xem có thể đi được (sử dụng BFS phiên bản trị belief). Nếu đi được thì ăn cặp (set thành 0).

### MU_1_PHAN (Local belief)

Ý tưởng: Agent có vị trí bắt đầu cụ thể, chỉ quan sát trong phạm vi nhất định và cập nhật niềm tin cục bộ. Khá hữu ích để mô phỏng agent di động khám phá bản đồ dần dần.

## 5. Giao diện người dùng (UI.py)

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

## 6. Tham số quan trọng và tuning

- Giới hạn số lần rẽ: 2 (một ràng buộc quan trọng của trò chơi Pikachu).
- Beam width: thay đổi trong BEAM_SEARCH để trade-off thời gian/khả năng tìm được đường.
- Pham_vi quan sát trong MU_*: mặc định 2, giảm để agent biết ít hơn, tăng để agent "thông minh" hơn.
- Giới hạn đệ quy/lan_lap trong backtracking để tránh timeout.

## 7. Lưu ý vận hành & debugging

- Chắc chắn các file ảnh/âm thanh tồn tại; thiếu file sẽ gây lỗi khi load.
- Các hàm dùng chỉ số cố định 12x12 — nếu thay đổi kích thước bảng phải chỉnh lại điều kiện 0..11.
- Trong một số nơi biến global (ví dụ `lan_vo`) được sử dụng; nếu gặp lỗi về global, xem cách khởi tạo/đặt lại giữa các lần chạy.
- Để log chi tiết, thêm print hoặc ghi ra file trong các hàm sinh trạng thái.

## 8. Tài liệu tham khảo nội bộ

Đọc trực tiếp từng file để xem chi tiết cài đặt. Các hàm vẽ (Ve_Simulation, Ve_Duong_Di, Ve_Duong_Di_1) cho phép debug trực quan.

---

*Phiên bản README: 1.0 — tạo bằng HTML để dễ mở trong trình duyệt. Nếu cần bản Markdown thuần, báo lại để chuyển đổi.*
