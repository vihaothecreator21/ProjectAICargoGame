"""
[Thành viên 1] Random Agent - Baseline đi ngẫu nhiên trên bàn cờ Caro.
Chọn ngẫu nhiên một trong số các ô cờ còn trống trên bàn cờ.
Hỗ trợ thiết lập seed ngẫu nhiên để tái lập kết quả thực nghiệm.
"""

import random
import time
from typing import Optional
from agents.base_agent import BaseAgent
from core.board import Board


class RandomAgent(BaseAgent):
    def __init__(
        self,
        name: str = "RandomAgent",
        player_id: int = 1,
        random_seed: Optional[int] = None
    ) -> None:
        super().__init__(name=name, player_id=player_id)
        self.random_generator = random.Random(random_seed)

    def get_move(self, board: Board) -> tuple[Optional[tuple[int, int]], dict]:
        """
        Lựa chọn ngẫu nhiên một nước đi hợp lệ.
        Trả về tọa độ (row, col) và số liệu đo lường.
        """
        start_timestamp = time.perf_counter()

        available_valid_moves = board.get_valid_moves()
        if not available_valid_moves:
            return None, {
                "nodes_evaluated": 0,
                "time_taken": 0.0,
                "depth_reached": 0
            }

        selected_move_coordinate = self.random_generator.choice(available_valid_moves)
        elapsed_calculation_time = time.perf_counter() - start_timestamp

        metrics_dictionary = {
            "nodes_evaluated": 1,
            "time_taken": elapsed_calculation_time,
            "depth_reached": 0
        }
        return selected_move_coordinate, metrics_dictionary
