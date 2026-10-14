"""
[Thành viên 1] Quản lý trạng thái bàn cờ Caro (Board State Representation) và luật chơi.

Quy định cấu hình & luật:
- Kích thước bàn cờ: 5x5
- Điều kiện thắng: Đạt 4 quân liên tiếp (ngang, dọc, chéo chính, chéo phụ).
- Luật biên (Boundary Rule): Bàn cờ phẳng có biên cứng. Các chuỗi vượt ra ngoài biên
  bị coi là bị chặn hoàn toàn (không tính cuộn vòng qua mép đối diện).
"""

from typing import Optional
from config import (
    BOARD_SIZE,
    WIN_COUNT,
    EMPTY_CELL,
    PLAYER_X,
    PLAYER_O
)


class Board:
    def __init__(self, board_size: int = BOARD_SIZE, win_condition_count: int = WIN_COUNT) -> None:
        """
        Khởi tạo bàn cờ Caro.
        :param board_size: Chiều rộng và chiều cao của bàn cờ (mặc định 5).
        :param win_condition_count: Số quân cờ liên tiếp cần đạt để thắng (mặc định 4).
        """
        self.board_size: int = board_size
        self.win_condition_count: int = win_condition_count
        
        # Ma trận 2 chiều biểu diễn bàn cờ (mặc định toàn bộ là EMPTY_CELL = 0)
        self.grid: list[list[int]] = [
            [EMPTY_CELL for _ in range(self.board_size)]
            for _ in range(self.board_size)
        ]
        
        # Tọa độ nước đi gần nhất: tuple (row, col) hoặc None
        self.last_move: Optional[tuple[int, int]] = None

    # Tương thích với thuộc tính cũ nếu code khác truy cập
    @property
    def size(self) -> int:
        return self.board_size

    @property
    def win_count(self) -> int:
        return self.win_condition_count

    def is_within_bounds(self, row_index: int, column_index: int) -> bool:
        """Kiểm tra tọa độ (row_index, column_index) có nằm trong biên bàn cờ hay không."""
        return 0 <= row_index < self.board_size and 0 <= column_index < self.board_size

    def is_empty_cell(self, row_index: int, column_index: int) -> bool:
        """Kiểm tra ô tại (row_index, column_index) có còn trống hay không."""
        return (
            self.is_within_bounds(row_index, column_index)
            and self.grid[row_index][column_index] == EMPTY_CELL
        )

    def is_valid_move(self, row_index: int, column_index: int) -> bool:
        """
        Kiểm tra tính hợp lệ của một nước đi.
        Nước đi hợp lệ phải nằm trong biên bàn cờ và ô đó phải đang trống.
        """
        return self.is_empty_cell(row_index, column_index)

    def get_valid_moves(self) -> list[tuple[int, int]]:
        """Trả về danh sách tất cả các ô hợp lệ (còn trống) trên toàn bàn cờ."""
        valid_moves: list[tuple[int, int]] = []
        for row_index in range(self.board_size):
            for column_index in range(self.board_size):
                if self.grid[row_index][column_index] == EMPTY_CELL:
                    valid_moves.append((row_index, column_index))
        return valid_moves

    def get_neighbor_moves(self, search_distance: int = 1) -> list[tuple[int, int]]:
        """
        Lấy danh sách các ô trống nằm trong bán kính search_distance xung quanh các quân cờ đã đánh.
        Hỗ trợ Thành viên 2 tối ưu Move Ordering và Thành viên 3 cài đặt Greedy.
        Nếu bàn cờ hoàn toàn trống, trả về ô chính giữa tâm bàn cờ.
        """
        occupied_cells = [
            (r, c)
            for r in range(self.board_size)
            for c in range(self.board_size)
            if self.grid[r][c] != EMPTY_CELL
        ]

        if not occupied_cells:
            center_coordinate = self.board_size // 2
            return [(center_coordinate, center_coordinate)]

        neighbor_candidates: set[tuple[int, int]] = set()
        for occupied_row, occupied_col in occupied_cells:
            for delta_row in range(-search_distance, search_distance + 1):
                for delta_col in range(-search_distance, search_distance + 1):
                    neighbor_row = occupied_row + delta_row
                    neighbor_col = occupied_col + delta_col
                    if self.is_empty_cell(neighbor_row, neighbor_col):
                        neighbor_candidates.add((neighbor_row, neighbor_col))

        return list(neighbor_candidates)

    def make_move(self, row_index: int, column_index: int, player_piece: int) -> bool:
        """
        Đánh một quân cờ của player_piece (PLAYER_X = 1 hoặc PLAYER_O = -1) vào ô (row_index, column_index).
        Trả về True nếu đánh thành công, False nếu nước đi không hợp lệ.
        """
        if not self.is_valid_move(row_index, column_index):
            return False

        self.grid[row_index][column_index] = player_piece
        self.last_move = (row_index, column_index)
        return True

    def undo_move(self, row_index: int, column_index: int) -> None:
        """
        Hoàn tác (rút lại) nước đi tại ô (row_index, column_index) để phục vụ thuật toán tìm kiếm Minimax.
        """
        if self.is_within_bounds(row_index, column_index):
            self.grid[row_index][column_index] = EMPTY_CELL
            self.last_move = None

    def is_full(self) -> bool:
        """Kiểm tra bàn cờ đã kín quân cờ (không còn ô trống nào) hay chưa."""
        for row_index in range(self.board_size):
            for column_index in range(self.board_size):
                if self.grid[row_index][column_index] == EMPTY_CELL:
                    return False
        return True

    def check_winner(self) -> Optional[int]:
        """
        Kiểm tra trạng thái kết thúc của ván đấu theo luật 5x5 thắng 4 và luật biên.
        
        Trả về:
            - PLAYER_X (1): Quân X chiến thắng (có 4 quân liên tiếp).
            - PLAYER_O (-1): Quân O chiến thắng (có 4 quân liên tiếp).
            - 0: Trận đấu hòa (bàn cờ đầy quân mà không có ai thắng).
            - None: Trận đấu vẫn đang tiếp diễn.
        """
        # 4 hướng xét: (ngang, dọc, chéo chính xuống phải, chéo phụ lên phải)
        search_directions: list[tuple[int, int]] = [
            (0, 1),   # Hàng ngang sang phải
            (1, 0),   # Cột dọc xuống dưới
            (1, 1),   # Đường chéo chính xuống phải
            (1, -1),  # Đường chéo phụ xuống trái
        ]

        for row_index in range(self.board_size):
            for column_index in range(self.board_size):
                current_piece = self.grid[row_index][column_index]
                if current_piece == EMPTY_CELL:
                    continue

                for step_row, step_col in search_directions:
                    consecutive_count = 0
                    for step_multiplier in range(self.win_condition_count):
                        target_row = row_index + step_multiplier * step_row
                        target_col = column_index + step_multiplier * step_col

                        # Kiểm tra luật biên: nếu vượt ngoài biên cứng thì đứt chuỗi
                        if (
                            self.is_within_bounds(target_row, target_col)
                            and self.grid[target_row][target_col] == current_piece
                        ):
                            consecutive_count += 1
                        else:
                            break

                    if consecutive_count == self.win_condition_count:
                        return current_piece

        # Nếu chưa ai thắng nhưng bàn cờ đã đầy ô -> Hòa
        if self.is_full():
            return 0

        # Trận đấu vẫn chưa kết thúc
        return None

    def clone(self) -> "Board":
        """Tạo bản sao sâu (deep copy) độc lập của trạng thái bàn cờ hiện tại."""
        cloned_board = Board(
            board_size=self.board_size,
            win_condition_count=self.win_condition_count
        )
        cloned_board.grid = [row[:] for row in self.grid]
        cloned_board.last_move = self.last_move
        return cloned_board
