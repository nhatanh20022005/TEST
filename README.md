<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Pikachu AI — README</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;line-height:1.5;color:#222;background:#fff;padding:24px}
h1,h2,h3{color:#0b5;}
code, pre{background:#f4f4f4;padding:6px;border-radius:4px}
section{margin-bottom:20px}
.table{border-collapse:collapse;width:100%}
.table th,.table td{border:1px solid #ddd;padding:8px}
</style>
</head>
<body>
<h1>Pikachu AI — Tài liệu chi tiết</h1>

<section>
<h2>1. Tổng quan dự án</h2>
<p>Dự án là bộ thuật toán tìm đường và agent chơi trò "Pikachu" (ghép cặp ô). Mỗi thuật toán nằm trong một file riêng và được UI (UI.py) gọi để thực hiện tìm đường hoặc quyết định mở ô. Các thuật toán chính có trong repository:</p>
<ul>
<li>BFS (Breadth-First Search)</li>
<li>DFS (Depth-First Search)</li>
<li>A* (A_SAO.py)</li>
<li>Greedy</li>
<li>Hill Climbing (HILL_CLAMBING.py)</li>
<li>Beam Search</li>
<li>Backtracking (BK.py)</li>
<li>Forward Checking Backtracking (Foward_Checking.py)</li>
<li>MU_1_PHAN (local belief agent)</li>
<li>MU_TOAN_PHAN (non-local belief agent)</li>
</ul>
</section>

<section>
<h2>2. Cấu trúc thư mục & file quan trọng</h2>
<ul>
<li><code>UI.py</code> — giao diện chính, danh sách thuật toán, gọi hàm tự động (Tu_Dong*, Tu_Dong_BFS*), vẽ bảng và animation.</li>
<li><code>BFS.py</code>, <code>DFS.py</code> — các trình duyệt đồ thị cơ bản với ràng buộc tối đa 2 lần rẽ.</li>
<li><code>A_SAO.py</code> — A* sử dụng heuristic Manhattan; lưu đường đi và cost list để vẽ.</li>
<li><code>Greedy.py</code> — thuật toán greedy dựa trên heuristic Manhattan (chỉ f = h).</li>
<li><code>HILL_CLAMBING.py</code> — hill climbing với điều kiện chỉ chấp nhận trạng thái không tăng heuristic; giới hạn số lần rẽ.</li>
<li><code>BEAM_SEARCH.py</code> — beam search giữ beam_width trạng thái tốt nhất theo f=h.</li>
<li><code>BK.py</code> — backtracking, kiểm tra ràng buộc hướng và số lần rẽ tối đa.</li>
<li><code>Foward_Checking.py</code> — backtracking có forward checking (loại trừ vị trí không hợp lệ trước khi mở rộng).</li>
<li><code>MU_1_PHAN.py</code>, <code>MU_TOAN_PHAN.py</code> — agent dùng niềm tin (belief) để suy đoán vị trí giống nhau rồi thử mở.</li>
<li>Tài nguyên ảnh và âm thanh (các file .png, .jpg, .wav) được load bởi UI.</li>
</ul>
</section>

<section>
<h2>3. Hướng dẫn nhanh cách chạy</h2>
<ol>
<li>Chuẩn bị môi trường Python 3.8+</li>
<li>Cài thư viện:
<pre><code>pip install numpy pygame psutil</code></pre>
</li>
<li>Đảm bảo các file ảnh (vd: <code>bg_menu2.jpg</code>, <code>bg.png</code>, icons) ở cùng thư mục hoặc đường dẫn tương ứng.</li>
<li>Chạy:
<pre><code>python UI.py</code></pre>
Màn hình menu hiện, chọn thuật toán rồi PLAY để chạy tự động.</li>
</ol>
</section>

<section>
<h2>4. Mô tả chi tiết từng thuật toán</h2>

<h3>BFS (Breadth-First Search)</h3>
<p>Ý tưởng: Mở rộng theo lớp, đảm bảo tìm đường ngắn nhất về số bước (với ràng buộc tối đa 2 lần rẽ). Implement dùng deque. Khi mở node, kiểm tra ràng buộc: ô mới phải là ô trống (0) hoặc là ô mục tiêu có cùng giá trị; không cho quay ngược lại (kiểm tra hướng) và chỉ chấp nhận <=2 lần rẽ.</p>
<p>Đầu vào: trạng thái ban đầu <code>(value,(x,y),turn,dir)</code> và trạng thái đích. Trả về path (danh sách toạ độ).</p>

<h3>DFS (Depth-First Search)</h3>
<p>Ý tưởng: Duyệt theo ngăn xếp, sử dụng cùng ràng buộc như BFS về hướng và số lần rẽ. DFS dễ rơi vào nhánh sâu; đã có giới hạn số lần lặp trong một số backtracking tùy file.</p>

<h3>A* (A_SAO.py)</h3>
<p>Ý tưởng: Dùng hàm f = g + h. g được tính là cost di chuyển (ở đây cost mỗi bước = 1). h là heuristic Manhattan (có hàm Euclid sẵn nhưng không dùng). Visited lưu chi phí tốt nhất đã thấy cho trạng thái để cho phép relax nếu tìm thấy đường tốt hơn. Kết quả trả về cả path và list cost để UI hiển thị giá trị heuristic/g.</p>

<h3>Greedy</h3>
<p>Ý tưởng: Lấy f = h (Manhattan). Không bảo đảm tối ưu, nhưng nhanh. Visited lưu h hiện tại để chỉ chấp nhận trạng thái nếu h tốt hơn.</p>

<h3>Hill Climbing</h3>
<p>Ý tưởng: Chỉ chấp nhận các bước làm giảm hoặc không tăng giá trị heuristic (càng gần goal càng tốt). Sử dụng heap ưu tiên theo heuristic. Có biến lan_vo để giữ thứ tự ổn định.</p>

<h3>Beam Search</h3>
<p>Ý tưởng: Mỗi vòng chỉ giữ <code>beam_width</code> trạng thái tốt nhất (theo h). Tạo candidate tiếp theo từ từng trạng thái, gom về beam nhỏ nhất để tiếp tục. Thích hợp giảm mức lan truyền trạng thái.</p>

<h3>Backtracking (BK.py)</h3>
<p>Ý tưởng: Dùng đệ quy tìm đường, kiểm tra ràng buộc trước khi mở rộng (hướng, số lần rẽ, ô hợp lệ). Có hàm <code>_is_opposite</code> để ngăn quay lại trái với hướng trước đó. Có giới hạn đệ quy (lan_lap) để tránh quá sâu.</p>

<h3>Forward Checking Backtracking (Foward_Checking.py)</h3>
<p>Ý tưởng: Trước khi sinh các neighbor sẽ lọc trước những ô có thể đi (forward checking) dựa trên giá trị hay ô trống. Lợi ích: giảm số nhánh không cần thiết.</p>

<h3>MU_TOAN_PHAN (Belief non-local)</h3>
<p>Ý tưởng: Mô phỏng agent có niềm tin cho toàn bộ bảng. Niềm tin là tập giá trị có thể xuất hiện ở vị trí đó. Agent quan sát vùng (pham_vi) để cập nhật niềm tin; khi niềm tin cho thấy một loại có 2 hoặc nhiều ô khả dĩ, agent thử suy đoán cặp và kiểm tra xem có thể đi được (sử dụng BFS phiên bản trị belief). Nếu đi được thì ăn cặp (set thành 0).</p>

<h3>MU_1_PHAN (Local belief)</h3>
<p>Ý tưởng: Agent có vị trí bắt đầu cụ thể, chỉ quan sát trong phạm vi nhất định và cập nhật niềm tin cục bộ. Khá hữu ích để mô phỏng agent di động khám phá bản đồ dần dần.</p>

</section>

<section>
<h2>5. Giao diện người dùng (UI.py)</h2>
<p>UI đảm nhiệm:</p>
<ul>
<li>Tạo board 10x10 với border padding 1 hàng cột (ma_tran 12x12)</li>
<li>Vẽ icon, highlight khi hover, vẽ grid.</li>
<li>Menu chọn thuật toán, HISTORY (ghi file CSV) và OPTIONS.</li>
<li>Hàm tự động hóa: <code>Tu_Dong</code>, <code>Tu_Dong_1</code>, <code>Tu_Dong_BFS_Non</code>, <code>Tu_Dong_BFS_1_P</code> tương ứng với cách gọi thuật toán khác nhau.</li>
<li>Animation: phương thức <code>Ve_Simulation</code> trong các lớp thuật toán thêm các segment để UI vẽ đường giữa các ô khi thử nghiệm.</li>
<li>Lưu lịch sử chạy (thời gian, bộ nhớ) vào <code>history.csv</code> khi pause hoặc hoàn thành level.</li>
</ul>

<h3>Phím tắt và tương tác</h3>
<ul>
<li>ESC: thoát game</li>
<li>P: tạm dừng/resume và ghi lịch sử</li>
<li>Trong menu: chọn OPTIONS để pick thuật toán, PLAY để chạy</li>
</ul>
</section>

<section>
<h2>6. Tham số quan trọng và tuning</h2>
<ul>
<li>Giới hạn số lần rẽ: 2 (một ràng buộc quan trọng của trò chơi Pikachu).</li>
<li>Beam width: thay đổi trong BEAM_SEARCH để trade-off thời gian/khả năng tìm được đường.</li>
<li>Pham_vi quan sát trong MU_*: mặc định 2, giảm để agent biết ít hơn, tăng để agent "thông minh" hơn.</li>
<li>Giới hạn đệ quy/lan_lap trong backtracking để tránh timeout.</li>
</ul>
</section>

<section>
<h2>7. Lưu ý vận hành & debugging</h2>
<ul>
<li>Chắc chắn các file ảnh/âm thanh tồn tại; thiếu file sẽ gây lỗi khi load.</li>
<li>Các hàm dùng chỉ số cố định 12x12 — nếu thay đổi kích thước bảng phải chỉnh lại điều kiện 0..11.</li>
<li>Trong một số nơi biến global (ví dụ <code>lan_vo</code>) được sử dụng; nếu gặp lỗi về global, xem cách khởi tạo/đặt lại giữa các lần chạy.</li>
<li>Để log chi tiết, thêm print hoặc ghi ra file trong các hàm sinh trạng thái.</li>
</ul>
</section>

<section>
<h2>8. Tài liệu tham khảo nội bộ</h2>
<p>Đọc trực tiếp từng file để xem chi tiết cài đặt. Các hàm vẽ (Ve_Simulation, Ve_Duong_Di, Ve_Duong_Di_1) cho phép debug trực quan.</p>
</section>

<footer>
<p>Phiên bản README: 1.0 — tạo bằng HTML để dễ mở trong trình duyệt. Nếu cần bản Markdown thuần, báo lại để chuyển đổi.</p>
</footer>
</body>
</html>
