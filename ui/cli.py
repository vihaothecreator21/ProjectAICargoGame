"""
[Thành viên 1] Giao diện dòng lệnh (CLI - Command Line Interface).
Hiển thị bàn cờ Caro 5x5, lượt đi hiện tại, kết quả trận đấu,
thời gian suy nghĩ và số lượng nút trạng thái đã duyệt.
"""

import os
import sys
from typing import Optional

# Đảm bảo đường dẫn gốc của project được nạp vào sys.path khi chạy trực tiếp file này
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.board import Board
from config import (
    PLAYER_SYMBOLS,
    PLAYER_X,
    PLAYER_O
)


def display_board(board: Board) -> None:
    """In bàn cờ 5x5 ra màn hình console trực quan kèm chỉ số hàng và cột."""
    column_header = "    " + "   ".join(str(col_idx) for col_idx in range(board.board_size))
    horizontal_separator = "  +" + "---+" * board.board_size

    print("\n" + column_header)
    print(horizontal_separator)

    for row_idx in range(board.board_size):
        row_content = f"{row_idx} |"
        for col_idx in range(board.board_size):
            cell_value = board.grid[row_idx][col_idx]
            symbol = PLAYER_SYMBOLS[cell_value]
            row_content += f" {symbol} |"
        print(row_content)
        print(horizontal_separator)
    print()


# Alias tương thích ngược
print_board = display_board


def display_move_details(
    player_id: int,
    move_coordinate: tuple[int, int],
    metrics_data: dict
) -> None:
    """Hiển thị chi tiết nước đi, thời gian tính toán và số nút duyệt của AI."""
    player_symbol = PLAYER_SYMBOLS[player_id]
    target_row, target_col = move_coordinate
    time_taken_seconds = metrics_data.get("time_taken", 0.0)
    nodes_evaluated_count = metrics_data.get("nodes_evaluated", 0)
    is_time_exceeded = metrics_data.get("is_time_exceeded", False)

    time_exceeded_warning = " [CẢNH BÁO: Vượt quá giới hạn thời gian!]" if is_time_exceeded else ""

    if nodes_evaluated_count > 0:
        print(
            f"[{player_symbol}] đánh ô ({target_row}, {target_col}) | "
            f"Thời gian: {time_taken_seconds:.4f}s | "
            f"Số nút duyệt: {nodes_evaluated_count:,}{time_exceeded_warning}"
        )
    else:
        print(f"[{player_symbol}] đánh ô ({target_row}, {target_col})")


print_move_info = display_move_details


def display_match_result(winner_player_id: Optional[int]) -> None:
    """Hiển thị thông báo kết quả chung cuộc của ván đấu."""
    print("=" * 45)
    if winner_player_id == PLAYER_X:
        print("🏆 KẾT QUẢ: QUÂN X (PLAYER_X) CHIẾN THẮNG!")
    elif winner_player_id == PLAYER_O:
        print("🏆 KẾT QUẢ: QUÂN O (PLAYER_O) CHIẾN THẮNG!")
    elif winner_player_id == 0:
        print("🤝 KẾT QUẢ: HAI BÊN HÒA CỜ (BÀN ĐẦY Ô)!")
    else:
        print("Trận đấu chưa có kết quả kết thúc.")
    print("=" * 45)


print_game_result = display_match_result
