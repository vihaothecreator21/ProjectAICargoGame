"""
[Thành viên 1] Điểm vào chính của chương trình Caro AI Arena (Bàn 5x5 - Thắng 4).
Hỗ trợ:
1. Chạy Giao diện đồ họa chuột trực quan (GUI - Tkinter).
2. Chạy Giao diện dòng lệnh (CLI Console) với 3 chế độ:
   - Người vs Người
   - Người vs AI (tùy chọn mức độ và bên đi trước)
   - AI vs AI (so sánh trực tiếp)
"""

import os
import sys
import time
from typing import Optional

# Cấu hình UTF-8 cho console Windows
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

from config import (
    BOARD_SIZE,
    WIN_COUNT,
    PLAYER_X,
    PLAYER_O,
    PLAYER_SYMBOLS
)
from core.board import Board
from core.game import CaroGame
from ui.cli import display_board, display_move_details, display_match_result
from agents.base_agent import BaseAgent
from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.minimax_agent import MinimaxAgent
from agents.alphabeta_agent import AlphaBetaAgent


def input_human_move(board: Board, current_player: int) -> tuple[int, int]:
    """Nhận và kiểm tra tọa độ nước đi từ bàn phím của người chơi."""
    player_symbol = PLAYER_SYMBOLS[current_player]
    while True:
        try:
            raw_input_string = input(
                f"Lượt của [{player_symbol}] - Nhập hàng và cột từ 0 đến {board.board_size - 1} (vd: 2 2): "
            ).strip()
            split_tokens = raw_input_string.split()
            if len(split_tokens) != 2:
                print("❌ Vui lòng nhập đúng 2 số nguyên cách nhau bằng khoảng trắng!")
                continue

            target_row_index = int(split_tokens[0])
            target_col_index = int(split_tokens[1])

            if board.is_valid_move(target_row_index, target_col_index):
                return (target_row_index, target_col_index)
            else:
                print(f"❌ Ô ({target_row_index}, {target_col_index}) không hợp lệ hoặc đã có quân cờ!")
        except ValueError:
            print("❌ Đầu vào không hợp lệ. Vui lòng nhập số nguyên!")


def create_agent_instance(
    agent_choice: str,
    player_id: int,
    agent_label: str = "",
    search_depth: int = 3
) -> BaseAgent:
    """Khởi tạo đối tượng Agent tương ứng với lựa chọn của người dùng."""
    if agent_choice == "1":
        return RandomAgent(name=f"RandomBot_{agent_label}", player_id=player_id)
    elif agent_choice == "2":
        return GreedyAgent(name=f"GreedyBot_{agent_label}", player_id=player_id)
    elif agent_choice == "3":
        return MinimaxAgent(name=f"Minimax_D{search_depth}_{agent_label}", player_id=player_id, max_depth=search_depth)
    elif agent_choice == "4":
        return AlphaBetaAgent(
            name=f"AlphaBeta_D{search_depth}_{agent_label}",
            player_id=player_id,
            max_depth=search_depth,
            use_move_ordering=True
        )
    else:
        # Mặc định an toàn
        return RandomAgent(name=f"RandomBot_{agent_label}", player_id=player_id)


def select_ai_menu(prompt_title: str) -> tuple[str, int]:
    """Menu phụ để chọn thuật toán AI và độ sâu tìm kiếm."""
    print(f"\n--- {prompt_title} ---")
    print("1. Random Agent (Ngẫu nhiên - Baseline 1)")
    print("2. Greedy Agent (Tham lam 1 bước - Baseline 2)")
    print("3. Minimax Agent (Duyệt chặn độ sâu)")
    print("4. Alpha-Beta Agent (Cắt tỉa + Move Ordering)")
    ai_choice = input("Chọn thuật toán AI (1-4, mặc định 4): ").strip()
    if ai_choice not in ["1", "2", "3", "4"]:
        ai_choice = "4"

    depth_value = 3
    if ai_choice in ["3", "4"]:
        raw_depth = input("Nhập độ sâu tìm kiếm (1-4, khuyến nghị 3): ").strip()
        if raw_depth.isdigit() and 1 <= int(raw_depth) <= 5:
            depth_value = int(raw_depth)

    return ai_choice, depth_value


def start_cli_game_session(game_mode_choice: int) -> None:
    """Khởi động và điều khiển một ván cờ trên giao diện dòng lệnh CLI."""
    board = Board(board_size=BOARD_SIZE, win_condition_count=WIN_COUNT)
    agent_for_player_x: Optional[BaseAgent] = None
    agent_for_player_o: Optional[BaseAgent] = None

    if game_mode_choice == 1:
        print("\n=== CHẾ ĐỘ 1: NGƯỜI VS NGƯỜI ===")
    elif game_mode_choice == 2:
        print("\n=== CHẾ ĐỘ 2: NGƯỜI VS AI ===")
        print("1. Người đi trước (quân X) - AI đi sau (quân O)")
        print("2. AI đi trước (quân X) - Người đi sau (quân O)")
        order_choice = input("Chọn lượt đi (1 hoặc 2, mặc định 1): ").strip()

        ai_choice, search_depth = select_ai_menu("Chọn đối thủ AI")

        if order_choice == "2":
            agent_for_player_x = create_agent_instance(ai_choice, PLAYER_X, "AI_X", search_depth)
            agent_for_player_o = None
        else:
            agent_for_player_x = None
            agent_for_player_o = create_agent_instance(ai_choice, PLAYER_O, "AI_O", search_depth)

    elif game_mode_choice == 3:
        print("\n=== CHẾ ĐỘ 3: AI VS AI ===")
        ai_choice_x, depth_x = select_ai_menu("Cấu hình AI thứ 1 (Quân X - Đi trước)")
        ai_choice_o, depth_o = select_ai_menu("Cấu hình AI thứ 2 (Quân O - Đi sau)")

        agent_for_player_x = create_agent_instance(ai_choice_x, PLAYER_X, "X", depth_x)
        agent_for_player_o = create_agent_instance(ai_choice_o, PLAYER_O, "O", depth_o)
    else:
        print("Lựa chọn chế độ không hợp lệ!")
        return

    game_controller = CaroGame(
        agent_player_x=agent_for_player_x,
        agent_player_o=agent_for_player_o,
        board=board
    )

    display_board(board)
    is_game_finished = False
    match_winner = None

    while not is_game_finished:
        active_agent = game_controller.get_current_agent()

        if active_agent is None:
            # Người chơi thực hiện nước đi
            human_move = input_human_move(board, game_controller.current_turn_player)
            is_game_finished, match_winner, step_summary = game_controller.play_step(human_selected_move=human_move)
        else:
            # AI thực hiện nước đi
            print(f"⏳ {active_agent.name} đang suy nghĩ...")
            is_game_finished, match_winner, step_summary = game_controller.play_step()
            time.sleep(0.2)  # Delay nhẹ để người xem theo dõi

        display_board(board)
        display_move_details(
            player_id=step_summary["player"],
            move_coordinate=step_summary["move"],
            metrics_data=step_summary["metrics"]
        )

    display_match_result(match_winner)


def main() -> None:
    """Hàm main điều hướng toàn bộ chương trình."""
    while True:
        print("\n" + "=" * 50)
        print("       HỆ THỐNG CARO AI ARENA (5x5 - THẮNG 4)       ")
        print("=" * 50)
        print("1. Khởi chạy Giao diện đồ họa (GUI Tkinter - Khuyên dùng)")
        print("2. Chế độ CLI: Người vs Người")
        print("3. Chế độ CLI: Người vs AI")
        print("4. Chế độ CLI: AI vs AI")
        print("5. Thoát chương trình")
        print("=" * 50)

        user_input_choice = input("Nhập lựa chọn của bạn (1-5): ").strip()

        if user_input_choice == "1":
            try:
                from ui.gui import run_gui_application
                print("\n[OK] Đang khởi chạy giao diện đồ họa GUI Tkinter...")
                run_gui_application()
            except Exception as gui_error:
                print(f"❌ Không thể mở GUI: {gui_error}")
        elif user_input_choice == "2":
            start_cli_game_session(game_mode_choice=1)
        elif user_input_choice == "3":
            start_cli_game_session(game_mode_choice=2)
        elif user_input_choice == "4":
            start_cli_game_session(game_mode_choice=3)
        elif user_input_choice == "5":
            print("\nCảm ơn bạn đã sử dụng Caro AI Arena. Tạm biệt!")
            break
        else:
            print("❌ Lựa chọn không hợp lệ. Vui lòng nhập từ 1 đến 5.")


if __name__ == "__main__":
    main()
