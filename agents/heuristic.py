"""
[Thành viên 2] Hàm lượng giá trạng thái bàn cờ (Heuristic Evaluation Function).
Dựa trên việc đếm số chuỗi quân liên tiếp mở (trống 2 đầu) hoặc bị chặn (chặn 1 đầu).

Quy ước:
- Chuỗi mở 2 đầu (open): Tiềm năng thắng rất cao -> Điểm thưởng lớn.
- Chuỗi bị chặn 1 đầu (semi-open / blocked 1 end): Giá trị trung bình.
- Chuỗi bị chặn 2 đầu (dead): Không có cơ hội phát triển -> Điểm = 0.
- Chuỗi đạt đủ WIN_COUNT (4 quân liên tiếp): Điểm cực đại (thắng trận).
"""

from core.board import Board
from config import EMPTY, PLAYER_X, PLAYER_O, WIN_COUNT

# Bảng trọng số tham khảo cho bàn cờ 5x5 thắng 4
WEIGHTS = {
    "WIN_4": 100000,          # 4 quân liên tiếp -> Thắng ngay
    "OPEN_3": 5000,           # 3 quân mở 2 đầu -> Đối thủ không chặn kịp cả 2
    "BLOCKED_3": 500,         # 3 quân bị chặn 1 đầu
    "OPEN_2": 200,            # 2 quân mở 2 đầu
    "BLOCKED_2": 20,          # 2 quân bị chặn 1 đầu
    "OPEN_1": 10,             # 1 quân mở
}

# 4 hướng: ngang, dọc, chéo chính, chéo phụ
DIRECTIONS = [(0, 1), (1, 0), (1, 1), (1, -1)]


def _get_all_lines(board: Board) -> list[list[int]]:
    """
    Trả về tất cả các đường (hàng, cột, chéo chính, chéo phụ) trên bàn cờ,
    mỗi đường là một list giá trị ô theo thứ tự duyệt.
    Chỉ giữ các đường đủ dài (>= WIN_COUNT) vì đường ngắn hơn không thể thắng.
    """
    n = board.size
    lines = []
    for dr, dc in DIRECTIONS:
        for r in range(n):
            for c in range(n):
                # Chỉ bắt đầu đường tại ô mà ô liền trước nó nằm ngoài biên
                pr, pc = r - dr, c - dc
                if 0 <= pr < n and 0 <= pc < n:
                    continue
                line = []
                rr, cc = r, c
                while 0 <= rr < n and 0 <= cc < n:
                    line.append(board.grid[rr][cc])
                    rr += dr
                    cc += dc
                if len(line) >= WIN_COUNT:
                    lines.append(line)
    return lines


def _chain_score(count: int, open_ends: int) -> int:
    """Tra bảng điểm cho một chuỗi liên tiếp."""
    if count >= WIN_COUNT:
        return WEIGHTS["WIN_4"]
    if open_ends == 0:
        return 0  # chuỗi chết (bị chặn 2 đầu)
    if count == 3:
        return WEIGHTS["OPEN_3"] if open_ends == 2 else WEIGHTS["BLOCKED_3"]
    if count == 2:
        return WEIGHTS["OPEN_2"] if open_ends == 2 else WEIGHTS["BLOCKED_2"]
    if count == 1:
        return WEIGHTS["OPEN_1"]
    return 0


def _score_line(line: list[int], player: int) -> int:
    """
    Duyệt từng chuỗi liên tiếp cùng màu của `player` trên một đường,
    đếm số quân (count) và số đầu mở (open_ends) rồi cộng điểm.
    """
    total = 0
    n = len(line)
    i = 0
    while i < n:
        if line[i] != player:
            i += 1
            continue
        j = i
        while j < n and line[j] == player:
            j += 1
        count = j - i
        open_ends = 0
        if i - 1 >= 0 and line[i - 1] == EMPTY:
            open_ends += 1
        if j < n and line[j] == EMPTY:
            open_ends += 1
        total += _chain_score(count, open_ends)
        i = j
    return total


def evaluate_board(board: Board, player: int) -> int:
    """
    Tính điểm lượng giá toàn bộ bàn cờ theo góc nhìn của `player`.
    Điểm dương lớn: vị thế có lợi cho `player`.
    Điểm âm lớn: vị thế có lợi cho đối thủ (-player).

    :param board: Đối tượng bàn cờ hiện tại
    :param player: PLAYER_X (1) hoặc PLAYER_O (-1)
    :return: Điểm số nguyên (heuristic score)
    """
    opponent = -player

    # Kiểm tra trạng thái kết thúc trước
    winner = board.check_winner()
    if winner == player:
        return WEIGHTS["WIN_4"]
    elif winner == opponent:
        return -WEIGHTS["WIN_4"]
    elif winner == 0:
        return 0

    my_score = 0
    opp_score = 0
    for line in _get_all_lines(board):
        my_score += _score_line(line, player)
        opp_score += _score_line(line, opponent)

    return my_score - opp_score