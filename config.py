"""
Cấu hình chuẩn cho bài toán Caro AI Arena (Bàn 5x5 - Thắng 4).
Tất cả các biến cấu hình và hằng số được định nghĩa tường minh, tránh giá trị ma thuật (magic numbers).
"""

# Kích thước bàn cờ chuẩn
BOARD_SIZE: int = 5

# Số quân liên tiếp tối thiểu theo hàng ngang, dọc hoặc chéo để chiến thắng
WIN_COUNT: int = 4

# Định danh trạng thái ô cờ
EMPTY_CELL: int = 0
PLAYER_X: int = 1   # Người đi trước (quân X)
PLAYER_O: int = -1  # Người đi sau (quân O)

# Tương thích ngược với tên ngắn
EMPTY = EMPTY_CELL

# Ký hiệu hiển thị trên giao diện
PLAYER_SYMBOLS: dict[int, str] = {
    EMPTY_CELL: ".",
    PLAYER_X: "X",
    PLAYER_O: "O"
}
SYMBOLS = PLAYER_SYMBOLS

# Giới hạn thời gian tối đa cho mỗi nước đi (đơn vị: giây)
# Đảm bảo giao diện luôn phản hồi theo mục 2.5.1
DEFAULT_MOVE_TIME_LIMIT_SECONDS: float = 5.0
