"""
[Thành viên 2] Alpha-Beta Pruning Agent kết hợp Move Ordering.
Thuật toán tìm kiếm đối kháng có cắt tỉa nhánh không triển vọng.
Hỗ trợ cờ bật/tắt Move Ordering để phục vụ đo lường số nút duyệt giảm đi bao nhiêu.
"""

import time
from agents.base_agent import BaseAgent
from agents.heuristic import evaluate_board
from core.board import Board


class AlphaBetaAgent(BaseAgent):
    def __init__(
        self,
        name: str = "AlphaBetaAgent",
        player_id: int = 1,
        max_depth: int = 4,
        use_move_ordering: bool = True
    ):
        super().__init__(name, player_id)
        self.max_depth = max_depth
        self.use_move_ordering = use_move_ordering
        self.nodes_evaluated = 0

    def order_moves(
        self,
        board: Board,
        moves: list[tuple[int, int]],
        player: int | None = None
    ) -> list[tuple[int, int]]:
        """
        [Move Ordering]: Sắp xếp thứ tự xét nước đi.
        Ưu tiên:
        1. Nước đi có điểm heuristic nhanh cao nhất (theo góc nhìn người sắp đánh).
        2. Hòa điểm thì ưu tiên ô gần tâm bàn cờ 5x5 (ô (2,2) là tâm).
        Danh sách `moves` nên là các ô lân cận (get_neighbor_moves).
        """
        mover = self.player_id if player is None else player
        center_r, center_c = board.size // 2, board.size // 2

        def move_priority(move):
            r, c = move
            board.make_move(r, c, mover)
            h = evaluate_board(board, mover)
            board.undo_move(r, c)
            dist_to_center = abs(r - center_r) + abs(c - center_c)
            return (-h, dist_to_center)

        return sorted(moves, key=move_priority)

    def _candidate_moves(self, board: Board, player: int) -> list[tuple[int, int]]:
        """Sinh nước đi con (lân cận) và sắp xếp nếu bật move ordering."""
        moves = board.get_neighbor_moves()
        if not moves:
            moves = board.get_valid_moves()
        if self.use_move_ordering:
            moves = self.order_moves(board, moves, player)
        return moves

    def get_move(self, board: Board) -> tuple[tuple[int, int] | None, dict]:
        start_time = time.perf_counter()
        self.nodes_evaluated = 0

        valid_moves = self._candidate_moves(board, self.player_id)
        if not valid_moves:
            return None, {"nodes_evaluated": 0, "time_taken": 0.0, "depth_reached": 0}

        best_score = float("-inf")
        best_move = valid_moves[0]
        alpha = float("-inf")
        beta = float("inf")

        for move in valid_moves:
            board.make_move(move[0], move[1], self.player_id)
            score = self._alphabeta(board, depth=self.max_depth - 1, alpha=alpha, beta=beta, is_maximizing=False)
            board.undo_move(move[0], move[1])
            if score > best_score:
                best_score = score
                best_move = move
            alpha = max(alpha, best_score)

        elapsed_time = time.perf_counter() - start_time
        metrics = {
            "nodes_evaluated": self.nodes_evaluated,
            "time_taken": elapsed_time,
            "depth_reached": self.max_depth,
            "use_move_ordering": self.use_move_ordering
        }
        return best_move, metrics

    def _alphabeta(self, board: Board, depth: int, alpha: float, beta: float, is_maximizing: bool) -> int:
        """Hàm đệ quy Alpha-Beta pruning."""
        self.nodes_evaluated += 1

        # Điều kiện dừng: có người thắng / hòa / hết độ sâu
        winner = board.check_winner()
        if winner is not None or depth == 0:
            score = evaluate_board(board, self.player_id)
            if winner == self.player_id:
                score += depth
            elif winner == -self.player_id:
                score -= depth
            return score

        current = self.player_id if is_maximizing else -self.player_id
        moves = self._candidate_moves(board, current)
        if not moves:
            return evaluate_board(board, self.player_id)

        if is_maximizing:
            best = float("-inf")
            for r, c in moves:
                board.make_move(r, c, current)
                score = self._alphabeta(board, depth - 1, alpha, beta, False)
                board.undo_move(r, c)
                best = max(best, score)
                alpha = max(alpha, best)
                if beta <= alpha:
                    break
            return best
        else:
            best = float("inf")
            for r, c in moves:
                board.make_move(r, c, current)
                score = self._alphabeta(board, depth - 1, alpha, beta, True)
                board.undo_move(r, c)
                best = min(best, score)
                beta = min(beta, best)
                if beta <= alpha:
                    break
            return best