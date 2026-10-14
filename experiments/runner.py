"""
[Thành viên 3] Kịch bản chạy thực nghiệm tự động (Experiment Runner).
Yêu cầu theo đề bài:
1. Tổ chức tối thiểu 30 ván cho mỗi cặp tác tử.
2. Đổi bên đi trước (15 ván Agent 1 là X, 15 ván Agent 2 là X).
3. Cố định seed ngẫu nhiên để tái lập kết quả.
4. Thu thập số liệu: Tỉ lệ thắng/hòa/thua, thời gian trung bình mỗi nước, số nút duyệt, độ sâu đạt được.
5. Xuất kết quả ra file CSV để vẽ biểu đồ.
"""

import os
import sys
import random
import csv
import time

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Đảm bảo đường dẫn gốc của project được nạp vào sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.board import Board
from core.game import CaroGame
from agents.base_agent import BaseAgent
from config import PLAYER_X, PLAYER_O


def run_match_series(
    agent_a_class,
    agent_b_class,
    agent_a_kwargs: dict,
    agent_b_kwargs: dict,
    total_games: int = 30,
    base_seed: int = 42,
    output_csv: str = "experiments/results/match_results.csv"
):
    """
    Chạy chuỗi trận đấu giữa 2 loại Agent.
    - total_games // 2 ván đầu: Agent A đi trước (quân X)
    - total_games // 2 ván sau: Agent B đi trước (quân X)
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    results = []

    print(f"\n=== BẮT ĐẦU CHẠY THỬ NGHIỆM ({total_games} VÁN) ===")

    for game_idx in range(1, total_games + 1):
        # Cố định seed cho ván đấu
        current_seed = base_seed + game_idx
        random.seed(current_seed)

        # Đổi bên đi trước
        if game_idx <= total_games // 2:
            agent_x = agent_a_class(name="Agent_A", player_id=PLAYER_X, **agent_a_kwargs)
            agent_o = agent_b_class(name="Agent_B", player_id=PLAYER_O, **agent_b_kwargs)
            a_is_x = True
        else:
            agent_x = agent_b_class(name="Agent_B", player_id=PLAYER_X, **agent_b_kwargs)
            agent_o = agent_a_class(name="Agent_A", player_id=PLAYER_O, **agent_a_kwargs)
            a_is_x = False

        game = CaroGame(agent_x=agent_x, agent_o=agent_o)

        game_over = False
        winner = None

        while not game_over:
            game_over, winner, _ = game.play_step()

        # Tổng hợp số liệu ván đấu
        a_times = []
        b_times = []
        a_nodes = []
        b_nodes = []

        for p, _, metrics in game.move_history:
            if (p == PLAYER_X and a_is_x) or (p == PLAYER_O and not a_is_x):
                a_times.append(metrics.get("time_taken", 0.0))
                a_nodes.append(metrics.get("nodes_evaluated", 0))
            else:
                b_times.append(metrics.get("time_taken", 0.0))
                b_nodes.append(metrics.get("nodes_evaluated", 0))

        # Xác định người thắng theo tên Agent A / Agent B
        if winner == 0:
            result_str = "DRAW"
        elif (winner == PLAYER_X and a_is_x) or (winner == PLAYER_O and not a_is_x):
            result_str = "AGENT_A_WIN"
        else:
            result_str = "AGENT_B_WIN"

        row = {
            "game_idx": game_idx,
            "seed": current_seed,
            "a_first": a_is_x,
            "winner": result_str,
            "total_moves": len(game.move_history),
            "a_avg_time": sum(a_times) / max(len(a_times), 1),
            "b_avg_time": sum(b_times) / max(len(b_times), 1),
            "a_avg_nodes": sum(a_nodes) / max(len(a_nodes), 1),
            "b_avg_nodes": sum(b_nodes) / max(len(b_nodes), 1),
        }
        results.append(row)
        print(f"Ván {game_idx}/{total_games}: Kết quả = {result_str} | Số nước = {row['total_moves']}")

    # Ghi file CSV
    if results:
        with open(output_csv, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=results[0].keys())
            writer.writeheader()
            writer.writerows(results)
        print(f"\n[OK] Đã lưu kết quả thực nghiệm vào: {output_csv}")

    return results


if __name__ == "__main__":
    from agents.random_agent import RandomAgent

    # Thử nghiệm mẫu: Random vs Random
    run_match_series(
        agent_a_class=RandomAgent,
        agent_b_class=RandomAgent,
        agent_a_kwargs={},
        agent_b_kwargs={},
        total_games=30,
        base_seed=100
    )
