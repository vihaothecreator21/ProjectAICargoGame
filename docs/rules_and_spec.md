# BÁO CÁO KỸ THUẬT: LOGIC TRÒ CHƠI CARO (5x5 - THẮNG 4) VÀ MÔ HÌNH HÓA
Tài liệu kỹ thuật do Thành viên 1 xây dựng - Dùng cho Báo cáo và Thuyết trình (Mục 2.5.1)

---

## 1. Cấu hình bài toán
- Kích thước không gian bàn cờ (Board size): Bàn 5x5 (tổng cộng 25 ô cờ).
- Điều kiện chiến thắng (Win condition): Một người chơi tạo được 4 quân cờ liên tiếp cùng loại (theo hàng ngang, cột dọc, đường chéo chính hoặc đường chéo phụ).
- Ký hiệu người chơi:
  - PLAYER_X (giá trị 1): Người đi trước (quân X).
  - PLAYER_O (giá trị -1): Người đi sau (quân O).
  - EMPTY_CELL (giá trị 0): Ô cờ chưa có quân đánh.

---

## 2. Quy định Luật biên (Boundary Rules)
- Biên cứng (Hard Boundary):
  - Bàn cờ phẳng có biên xác định trong hệ tọa độ: hàng từ 0 đến 4, cột từ 0 đến 4.
  - Các ô nằm ngoài phạm vi này bị xem là biên chặn hoàn toàn.
  - Không áp dụng luật cuộn vòng (No wrap-around): Quân cờ ở cột 4 và cột 0 của hàng tiếp theo không bao giờ được tính là liền kề nhau.
  - Chuỗi quân cờ nằm sát biên chỉ có thể phát triển về phía đối diện còn lại (tính là chuỗi bị chặn 1 đầu).

---

## 3. Biểu diễn trạng thái bàn cờ (State Representation)
- Cấu trúc dữ liệu: Ma trận 2 chiều số nguyên kích thước 5x5:
  grid: danh sách 5 hàng, mỗi hàng 5 phần tử số nguyên.
- Không gian trạng thái (State Space):
  - Mỗi ô có 3 trạng thái: Trống (0), X (1), O (-1).
  - Số trạng thái tối đa trên lý thuyết xấp xỉ 3 mũ 25 (khoảng 847 tỷ trạng thái).
  - Nhờ giới hạn bàn cờ 5x5 và luật thắng 4, độ sâu trung bình của một ván cờ ngắn hơn rất nhiều so với cờ Caro 15x15 hay 19x19 thông thường. Điều này giúp thuật toán Minimax và Alpha-Beta có thể tìm kiếm sâu (độ sâu từ 3 đến 5) chỉ trong thời gian vài phần trăm giây.

---

## 4. Thuật toán kiểm tra điều kiện thắng (Win Check Algorithm)
- Phương pháp: Quét 4 hướng độc lập từ mỗi ô trên bàn cờ:
  1. Hàng ngang: bước nhảy (0, 1)
  2. Cột dọc: bước nhảy (1, 0)
  3. Đường chéo chính: bước nhảy (1, 1)
  4. Đường chéo phụ: bước nhảy (1, -1)
- Độ phức tạp: Khoảng vài chục phép kiểm tra cho mỗi lượt đi trên bàn 5x5, đảm bảo thời gian chạy cực nhanh (dưới 0.0001 giây), giao diện không bao giờ bị trễ.

---

## 5. Hướng dẫn sử dụng giao diện
- Giao diện dòng lệnh (CLI): Chạy lệnh "python main.py", chọn các chế độ tương tác qua bàn phím.
- Giao diện đồ họa (GUI Tkinter): Chạy lựa chọn 1 trong "main.py" hoặc chạy trực tiếp "python ui/gui.py". Giao diện hỗ trợ click chuột trực tiếp, hiển thị lượt đi, thời gian suy nghĩ của AI, số nút đã duyệt và chạy đa luồng mượt mà.
