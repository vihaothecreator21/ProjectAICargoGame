"""
[Thành viên 3] Greedy Agent - Baseline tham lam 1 bước.
Nhiệm vụ của Thành viên 3:
- Đánh giá tất cả các nước đi hợp lệ ở độ sâu 1.
- Ưu tiên:
  1. Nếu có nước đi thắng ngay -> chọn ngay.
  2. Nếu đối thủ có nước đi thắng ngay ở lượt sau -> chọn nước chặn ngay.
  3. Nếu không, chọn nước đi có điểm lượng giá Heuristic cao nhất.
"""

import time
from agents.base_agent import BaseAgent
from core.board import Board


class GreedyAgent(BaseAgent):
    def __init__(self, name: str = "GreedyAgent", player_id: int = 1):
        super().__init__(name, player_id)

    def get_move(self, board: Board) -> tuple[tuple[int, int] | None, dict]:
        start_time = time.perf_counter()
        nodes_evaluated = 0

        valid_moves = board.get_valid_moves()
        if not valid_moves:
            return None, {"nodes_evaluated": 0, "time_taken": 0.0, "depth_reached": 1}

        # TODO [Thành viên 3]: Cài đặt logic tham lam 1 bước:
        # 1. Duyệt qua từng nước đi trong valid_moves.
        # 2. Thử đi nước đó và kiểm tra check_winner() hoặc tính điểm heuristic.
        # 3. Chọn nước đi tốt nhất.

        # Tạm thời trả về nước đầu tiên làm mẫu
        chosen_move = valid_moves[0]
        nodes_evaluated = len(valid_moves)
        elapsed_time = time.perf_counter() - start_time

        metrics = {
            "nodes_evaluated": nodes_evaluated,
            "time_taken": elapsed_time,
            "depth_reached": 1
        }
        return chosen_move, metrics
