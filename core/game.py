"""
[Thành viên 1] Bộ điều khiển ván đấu Caro (Game Controller).
Hỗ trợ 3 chế độ:
- Người - Người (Human vs Human)
- Người - AI (Human vs AI)
- AI - AI (AI vs AI)

Quản lý lượt đi, tính thời gian suy nghĩ của từng nước và kiểm tra giới hạn thời gian (Timeout limit).
"""

import time
from typing import Optional
from core.board import Board
from agents.base_agent import BaseAgent
from config import (
    PLAYER_X,
    PLAYER_O,
    PLAYER_SYMBOLS,
    DEFAULT_MOVE_TIME_LIMIT_SECONDS
)


class CaroGame:
    def __init__(
        self,
        agent_player_x: Optional[BaseAgent] = None,
        agent_player_o: Optional[BaseAgent] = None,
        board: Optional[Board] = None,
        move_time_limit_seconds: float = DEFAULT_MOVE_TIME_LIMIT_SECONDS,
        agent_x: Optional[BaseAgent] = None,
        agent_o: Optional[BaseAgent] = None
    ) -> None:
        """
        Khởi tạo ván đấu Caro.
        :param agent_player_x: Tác tử điều khiển quân X (hoặc None nếu do Người chơi bấm/nhập)
        :param agent_player_o: Tác tử điều khiển quân O (hoặc None nếu do Người chơi bấm/nhập)
        :param board: Bàn cờ (mặc định tạo mới bàn 5x5 thắng 4)
        :param move_time_limit_seconds: Thời gian tối đa cho phép mỗi nước đi (giây)
        """
        self.board: Board = board if board is not None else Board()
        self.agent_player_x: Optional[BaseAgent] = agent_player_x if agent_player_x is not None else agent_x
        self.agent_player_o: Optional[BaseAgent] = agent_player_o if agent_player_o is not None else agent_o
        self.move_time_limit_seconds: float = move_time_limit_seconds

        # Người chơi bắt đầu trước luôn là PLAYER_X
        self.current_turn_player: int = PLAYER_X

        # Danh sách lưu vết các nước đi: (player, (row, col), metrics_dict)
        self.move_history: list[tuple[int, tuple[int, int], dict]] = []

    def get_current_agent(self) -> Optional[BaseAgent]:
        """Trả về Agent đại diện cho lượt đi hiện tại (hoặc None nếu là Người)."""
        if self.current_turn_player == PLAYER_X:
            return self.agent_player_x
        return self.agent_player_o

    def play_step(
        self,
        human_selected_move: Optional[tuple[int, int]] = None
    ) -> tuple[bool, Optional[int], dict]:
        """
        Thực hiện một bước đi duy nhất trong ván đấu.
        
        :param human_selected_move: Tọa độ (row, col) do người chơi nhập (nếu lượt hiện tại là Người).
        :return: Tuple gồm:
            1. is_game_over (bool): Ván đấu đã kết thúc hay chưa.
            2. winner_result (Optional[int]): 1 (X thắng), -1 (O thắng), 0 (Hòa), None (Chưa kết thúc).
            3. step_summary (dict): Thông tin chi tiết về nước đi vừa thực hiện.
        """
        active_agent = self.get_current_agent()

        if active_agent is not None:
            # Lượt của Tác tử AI: Bắt đầu bấm giờ suy nghĩ
            start_timestamp = time.perf_counter()
            chosen_coordinate, calculation_metrics = active_agent.get_move(self.board)
            elapsed_calculation_time = time.perf_counter() - start_timestamp

            # Đảm bảo trường time_taken luôn chính xác
            if calculation_metrics.get("time_taken", 0.0) == 0.0:
                calculation_metrics["time_taken"] = elapsed_calculation_time

            # Đánh dấu cảnh báo nếu vượt quá thời gian quy định
            calculation_metrics["is_time_exceeded"] = (
                elapsed_calculation_time > self.move_time_limit_seconds
            )
        else:
            # Lượt của Người chơi
            chosen_coordinate = human_selected_move
            calculation_metrics = {
                "nodes_evaluated": 0,
                "time_taken": 0.0,
                "depth_reached": 0,
                "is_time_exceeded": False
            }

        # Kiểm tra tính hợp lệ của nước đi
        if chosen_coordinate is None:
            raise ValueError(f"Không thể thực hiện nước đi rỗng từ người chơi [{PLAYER_SYMBOLS[self.current_turn_player]}]")

        target_row, target_col = chosen_coordinate
        if not self.board.make_move(target_row, target_col, self.current_turn_player):
            raise ValueError(f"Nước đi ({target_row}, {target_col}) không hợp lệ trên bàn cờ!")

        # Ghi nhận vào lịch sử
        self.move_history.append((self.current_turn_player, chosen_coordinate, calculation_metrics))

        # Kiểm tra kết quả ván đấu
        winner_result = self.board.check_winner()
        is_game_over = (winner_result is not None)

        step_summary = {
            "player": self.current_turn_player,
            "player_symbol": PLAYER_SYMBOLS[self.current_turn_player],
            "move": chosen_coordinate,
            "metrics": calculation_metrics
        }

        # Nếu chưa kết thúc thì chuyển lượt cho đối thủ
        if not is_game_over:
            self.current_turn_player = -self.current_turn_player

        return is_game_over, winner_result, step_summary

    def reset_game(self) -> None:
        """Đặt lại trạng thái ván cờ về ban đầu."""
        self.board = Board(
            board_size=self.board.board_size,
            win_condition_count=self.board.win_condition_count
        )
        self.current_turn_player = PLAYER_X
        self.move_history.clear()
