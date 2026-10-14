"""
[Thành viên 2] Minimax Agent có giới hạn độ sâu (Depth-limited Minimax).
Thuật toán tìm kiếm vét cạn có chặn độ sâu, không áp dụng cắt tỉa.
Dùng làm cơ sở (benchmark) để so sánh số nút duyệt với Alpha-Beta Pruning.
"""

import time
from agents.base_agent import BaseAgent
from agents.heuristic import evaluate_board
from core.board import Board


class MinimaxAgent(BaseAgent):
    def __init__(self, name: str = "MinimaxAgent", player_id: int = 1, max_depth: int = 3):
        super().__init__(name, player_id)
        self.max_depth = max_depth
        self.nodes_evaluated = 0

    def _candidate_moves(self, board: Board) -> list[tuple[int, int]]:
        """Dùng nước đi lân cận để giảm không gian tìm kiếm; fallback sang toàn bộ ô trống."""
        moves = board.get_neighbor_moves()
        if not moves:
            moves = board.get_valid_moves()
        return moves

    def get_move(self, board: Board) -> tuple[tuple[int, int] | None, dict]:
        start_time = time.perf_counter()
        self.nodes_evaluated = 0

        valid_moves = self._candidate_moves(board)
        if not valid_moves:
            return None, {"nodes_evaluated": 0, "time_taken": 0.0, "depth_reached": 0}

        best_score = float("-inf")
        best_move = valid_moves[0]

        for move in valid_moves:
            board.make_move(move[0], move[1], self.player_id)
            score = self._minimax(board, depth=self.max_depth - 1, is_maximizing=False)
            board.undo_move(move[0], move[1])
            if score > best_score:
                best_score = score
                best_move = move

        elapsed_time = time.perf_counter() - start_time
        metrics = {
            "nodes_evaluated": self.nodes_evaluated,
            "time_taken": elapsed_time,
            "depth_reached": self.max_depth
        }
        return best_move, metrics

    def _minimax(self, board: Board, depth: int, is_maximizing: bool) -> int:
        """Hàm đệ quy Minimax có giới hạn độ sâu."""
        self.nodes_evaluated += 1

        # Điều kiện dừng: có người thắng / hòa / hết độ sâu
        winner = board.check_winner()
        if winner is not None or depth == 0:
            score = evaluate_board(board, self.player_id)
            # Ưu tiên thắng sớm, thua muộn (depth còn lại càng lớn = càng sớm)
            if winner == self.player_id:
                score += depth
            elif winner == -self.player_id:
                score -= depth
            return score

        moves = self._candidate_moves(board)
        if not moves:
            return evaluate_board(board, self.player_id)

        if is_maximizing:
            best = float("-inf")
            for r, c in moves:
                board.make_move(r, c, self.player_id)
                score = self._minimax(board, depth - 1, False)
                board.undo_move(r, c)
                best = max(best, score)
            return best
        else:
            best = float("inf")
            for r, c in moves:
                board.make_move(r, c, -self.player_id)
                score = self._minimax(board, depth - 1, True)
                board.undo_move(r, c)
                best = min(best, score)
            return best