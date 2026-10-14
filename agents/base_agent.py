"""
Interface chuẩn cho tất cả các tác tử (Agent) trong trò chơi Caro.
Tất cả các Agent (Random, Greedy, Minimax, Alpha-Beta) BẮT BUỘC kế thừa lớp này.
"""

from abc import ABC, abstractmethod
from core.board import Board


class BaseAgent(ABC):
    def __init__(self, name: str, player_id: int):
        """
        Khởi tạo Agent.
        :param name: Tên định danh của Agent (vd: "RandomBot", "Minimax-D3", "AlphaBeta-D4")
        :param player_id: Ký hiệu quân cờ đại diện (PLAYER_X = 1 hoặc PLAYER_O = -1)
        """
        self.name = name
        self.player_id = player_id

    @abstractmethod
    def get_move(self, board: Board) -> tuple[tuple[int, int] | None, dict]:
        """
        Phương thức tính toán và trả về nước đi tiếp theo.

        :param board: Bản sao hoặc trạng thái hiện tại của bàn cờ
        :return: Tuple gồm 2 phần tử:
            1. (row, col): Tọa độ nước đi được chọn (hoặc None nếu hết ô đi)
            2. metrics: Dictionary chứa các số đo phục vụ thống kê & thực nghiệm:
               {
                   "nodes_evaluated": int,   # Tổng số nút (trạng thái) đã duyệt
                   "time_taken": float,      # Thời gian tính toán (giây)
                   "depth_reached": int      # Độ sâu tìm kiếm đã đạt được
               }
        """
        pass
