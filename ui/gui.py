"""
[Thành viên 1] Giao diện đồ họa người dùng (GUI - Graphical User Interface) bằng Tkinter.
Cung cấp bàn cờ 5x5 tương tác chuột, hỗ trợ 3 chế độ:
- Người vs Người
- Người vs AI (người chơi chọn đi trước X hoặc đi sau O)
- AI vs AI (tự động đánh kèm delay quan sát)

Tích hợp đa luồng (threading) để giao diện luôn mượt mà, phản hồi ngay lập tức, không bao giờ bị đơ.
"""

import os
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional

# Đảm bảo đường dẫn gốc của project được nạp vào sys.path khi chạy trực tiếp file này
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import (
    BOARD_SIZE,
    WIN_COUNT,
    EMPTY_CELL,
    PLAYER_X,
    PLAYER_O,
    PLAYER_SYMBOLS
)
from core.board import Board
from core.game import CaroGame
from agents.base_agent import BaseAgent
from agents.random_agent import RandomAgent
from agents.greedy_agent import GreedyAgent
from agents.minimax_agent import MinimaxAgent
from agents.alphabeta_agent import AlphaBetaAgent


class CaroGUI:
    def __init__(self, root_window: tk.Tk) -> None:
        self.root_window = root_window
        self.root_window.title("Caro AI Arena - Bàn 5x5 Thắng 4")
        self.root_window.resizable(False, False)

        # Trạng thái game
        self.game_controller: Optional[CaroGame] = None
        self.is_game_running: bool = False
        self.is_ai_computing: bool = False

        # Cấu hình màu sắc giao diện
        self.color_background = "#F4F6F9"
        self.color_board_bg = "#FFFFFF"
        self.color_cell_default = "#E8ECEF"
        self.color_cell_hover = "#DDE2E6"
        self.color_player_x = "#1976D2"    # Xanh dương đậm
        self.color_player_o = "#D32F2F"    # Đỏ đậm
        self.color_last_move = "#FFF3CD"   # Vàng nhạt nổi bật nước vừa đi

        self.root_window.configure(bg=self.color_background)

        # Tạo cấu trúc giao diện
        self._setup_ui_layout()
        self.start_new_game()

    def _setup_ui_layout(self) -> None:
        """Thiết lập bố cục các khung điều khiển và bàn cờ."""
        main_container = tk.Frame(self.root_window, bg=self.color_background, padx=15, pady=15)
        main_container.pack()

        # Tiêu đề
        title_label = tk.Label(
            main_container,
            text="CARO AI ARENA (5x5 - THẮNG 4)",
            font=("Arial", 16, "bold"),
            bg=self.color_background,
            fg="#2C3E50"
        )
        title_label.pack(pady=(0, 10))

        # Khung điều khiển & tùy chọn
        control_frame = tk.LabelFrame(
            main_container,
            text=" Cấu hình trận đấu ",
            font=("Arial", 10, "bold"),
            bg=self.color_background,
            padx=10,
            pady=8
        )
        control_frame.pack(fill="x", pady=(0, 10))

        # Chọn chế độ chơi
        row_mode = tk.Frame(control_frame, bg=self.color_background)
        row_mode.pack(fill="x", pady=2)
        tk.Label(row_mode, text="Chế độ:", font=("Arial", 9), bg=self.color_background).pack(side="left")
        
        self.var_game_mode = tk.StringVar(value="Người vs AI (Người đi X)")
        self.combo_mode = ttk.Combobox(
            row_mode,
            textvariable=self.var_game_mode,
            values=[
                "Người vs Người",
                "Người vs AI (Người đi X)",
                "AI vs Người (Người đi O)",
                "AI vs AI"
            ],
            state="readonly",
            width=26
        )
        self.combo_mode.pack(side="right")
        self.combo_mode.bind("<<ComboboxSelected>>", lambda _: self.start_new_game())

        # Chọn loại AI
        row_ai = tk.Frame(control_frame, bg=self.color_background)
        row_ai.pack(fill="x", pady=2)
        tk.Label(row_ai, text="Thuật toán AI:", font=("Arial", 9), bg=self.color_background).pack(side="left")

        self.var_ai_type = tk.StringVar(value="Alpha-Beta (Có Move Ordering)")
        self.combo_ai = ttk.Combobox(
            row_ai,
            textvariable=self.var_ai_type,
            values=[
                "Random (Ngẫu nhiên)",
                "Greedy (Tham lam 1 bước)",
                "Minimax (Không cắt tỉa)",
                "Alpha-Beta (Có Move Ordering)"
            ],
            state="readonly",
            width=26
        )
        self.combo_ai.pack(side="right")

        # Độ sâu tìm kiếm (Depth)
        row_depth = tk.Frame(control_frame, bg=self.color_background)
        row_depth.pack(fill="x", pady=2)
        tk.Label(row_depth, text="Độ sâu tìm kiếm (Depth):", font=("Arial", 9), bg=self.color_background).pack(side="left")
        self.spin_depth = tk.Spinbox(row_depth, from_=1, to=5, width=5, justify="center")
        self.spin_depth.delete(0, "end")
        self.spin_depth.insert(0, "3")
        self.spin_depth.pack(side="right")

        # Nút Bắt đầu ván mới
        btn_frame = tk.Frame(control_frame, bg=self.color_background)
        btn_frame.pack(fill="x", pady=(6, 2))
        self.btn_restart = tk.Button(
            btn_frame,
            text="🔄 Bắt đầu ván mới",
            font=("Arial", 10, "bold"),
            bg="#28A745",
            fg="white",
            relief="raised",
            cursor="hand2",
            command=self.start_new_game
        )
        self.btn_restart.pack(fill="x")

        # Khung thông tin ván đấu
        self.status_label = tk.Label(
            main_container,
            text="Lượt đi: [X]",
            font=("Arial", 12, "bold"),
            bg=self.color_background,
            fg=self.color_player_x
        )
        self.status_label.pack(pady=4)

        self.metrics_label = tk.Label(
            main_container,
            text="Thời gian: 0.000s | Nút duyệt: 0",
            font=("Consolas", 9),
            bg=self.color_background,
            fg="#555555"
        )
        self.metrics_label.pack(pady=(0, 6))

        # Khung bàn cờ 5x5
        self.board_frame = tk.Frame(main_container, bg="#BDC3C7", padx=3, pady=3)
        self.board_frame.pack()

        self.cell_buttons: list[list[tk.Button]] = []
        for row_idx in range(BOARD_SIZE):
            row_button_list: list[tk.Button] = []
            for col_idx in range(BOARD_SIZE):
                btn = tk.Button(
                    self.board_frame,
                    text="",
                    font=("Arial", 18, "bold"),
                    width=4,
                    height=2,
                    bg=self.color_cell_default,
                    activebackground=self.color_cell_hover,
                    relief="groove",
                    cursor="hand2",
                    command=lambda r=row_idx, c=col_idx: self.handle_cell_click(r, c)
                )
                btn.grid(row=row_idx, column=col_idx, padx=2, pady=2)
                row_button_list.append(btn)
            self.cell_buttons.append(row_button_list)

    def _create_agent_by_selection(self, player_id: int, agent_label: str) -> BaseAgent:
        """Tạo tác tử AI theo cấu hình người dùng chọn trên giao diện."""
        selected_ai = self.var_ai_type.get()
        try:
            depth_value = int(self.spin_depth.get())
        except ValueError:
            depth_value = 3

        if "Random" in selected_ai:
            return RandomAgent(name=f"RandomBot_{agent_label}", player_id=player_id)
        elif "Greedy" in selected_ai:
            return GreedyAgent(name=f"GreedyBot_{agent_label}", player_id=player_id)
        elif "Minimax" in selected_ai:
            return MinimaxAgent(name=f"Minimax_D{depth_value}_{agent_label}", player_id=player_id, max_depth=depth_value)
        else:
            return AlphaBetaAgent(
                name=f"AlphaBeta_D{depth_value}_{agent_label}",
                player_id=player_id,
                max_depth=depth_value,
                use_move_ordering=True
            )

    def start_new_game(self) -> None:
        """Khởi động ván cờ mới theo cấu hình đã chọn."""
        mode_text = self.var_game_mode.get()
        agent_x: Optional[BaseAgent] = None
        agent_o: Optional[BaseAgent] = None

        if mode_text == "Người vs Người":
            agent_x = None
            agent_o = None
        elif mode_text == "Người vs AI (Người đi X)":
            agent_x = None
            agent_o = self._create_agent_by_selection(player_id=PLAYER_O, agent_label="O")
        elif mode_text == "AI vs Người (Người đi O)":
            agent_x = self._create_agent_by_selection(player_id=PLAYER_X, agent_label="X")
            agent_o = None
        elif mode_text == "AI vs AI":
            agent_x = self._create_agent_by_selection(player_id=PLAYER_X, agent_label="X")
            agent_o = self._create_agent_by_selection(player_id=PLAYER_O, agent_label="O")

        self.game_controller = CaroGame(agent_player_x=agent_x, agent_player_o=agent_o)
        self.is_game_running = True
        self.is_ai_computing = False

        # Xóa trắng bàn cờ trên GUI
        for row_idx in range(BOARD_SIZE):
            for col_idx in range(BOARD_SIZE):
                self.cell_buttons[row_idx][col_idx].configure(
                    text="",
                    bg=self.color_cell_default,
                    state="normal"
                )

        self._update_status_display()

        # Nếu quân đi đầu (X) là AI thì kích hoạt AI suy nghĩ
        if self.game_controller.get_current_agent() is not None:
            self._trigger_ai_move_async()

    def _update_status_display(self) -> None:
        """Cập nhật nhãn thông tin lượt đi và người chơi."""
        if not self.is_game_running or self.game_controller is None:
            return

        current_player = self.game_controller.current_turn_player
        player_symbol = PLAYER_SYMBOLS[current_player]
        color = self.color_player_x if current_player == PLAYER_X else self.color_player_o

        active_agent = self.game_controller.get_current_agent()
        role_description = f"AI ({active_agent.name})" if active_agent else "Người chơi"

        self.status_label.configure(
            text=f"Lượt đi: [{player_symbol}] - {role_description}",
            fg=color
        )

    def handle_cell_click(self, target_row: int, target_col: int) -> None:
        """Xử lý khi người dùng click chuột vào ô bàn cờ."""
        if not self.is_game_running or self.is_ai_computing or self.game_controller is None:
            return

        # Chỉ xử lý click nếu lượt này là của Người chơi
        if self.game_controller.get_current_agent() is not None:
            return

        if not self.game_controller.board.is_valid_move(target_row, target_col):
            return

        # Thực hiện nước đi của người chơi
        is_over, winner, step_info = self.game_controller.play_step(human_selected_move=(target_row, target_col))
        self._refresh_board_cells(last_row=target_row, last_col=target_col)
        self._display_step_metrics(step_info["metrics"])

        if is_over:
            self._finish_game(winner)
            return

        self._update_status_display()

        # Nếu lượt kế tiếp là AI thì kích hoạt
        if self.game_controller.get_current_agent() is not None:
            self._trigger_ai_move_async()

    def _trigger_ai_move_async(self) -> None:
        """Chạy bước tính toán của AI trên luồng riêng để tránh đơ giao diện."""
        if not self.is_game_running or self.is_ai_computing:
            return

        self.is_ai_computing = True
        self.status_label.configure(text="AI đang suy nghĩ...", fg="#E67E22")
        self.root_window.update()

        thread = threading.Thread(target=self._ai_worker_process, daemon=True)
        thread.start()

    def _ai_worker_process(self) -> None:
        """Tiến trình nền tính toán nước đi của AI."""
        time.sleep(0.15)  # Nghỉ nhẹ để giao diện hiển thị mượt
        if self.game_controller is None:
            return

        try:
            is_over, winner, step_info = self.game_controller.play_step()
            # Đẩy cập nhật về luồng chính UI của Tkinter
            self.root_window.after(0, self._handle_ai_step_completed, is_over, winner, step_info)
        except Exception as error_msg:
            print(f"Lỗi khi AI thực hiện nước đi: {error_msg}")
            self.is_ai_computing = False

    def _handle_ai_step_completed(self, is_over: bool, winner: Optional[int], step_info: dict) -> None:
        """Xử lý kết quả trả về từ luồng AI."""
        self.is_ai_computing = False
        target_row, target_col = step_info["move"]

        self._refresh_board_cells(last_row=target_row, last_col=target_col)
        self._display_step_metrics(step_info["metrics"])

        if is_over:
            self._finish_game(winner)
            return

        self._update_status_display()

        # Nếu tiếp tục là lượt AI (chế độ AI vs AI) thì tự động gọi tiếp
        if self.game_controller and self.game_controller.get_current_agent() is not None:
            self._trigger_ai_move_async()

    def _refresh_board_cells(self, last_row: int, last_col: int) -> None:
        """Cập nhật ký tự và màu sắc cho các ô trên bàn cờ."""
        if self.game_controller is None:
            return

        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                cell_value = self.game_controller.board.grid[r][c]
                btn = self.cell_buttons[r][c]

                if cell_value == PLAYER_X:
                    btn.configure(
                        text="X",
                        fg=self.color_player_x,
                        bg=self.color_last_move if (r == last_row and c == last_col) else self.color_board_bg
                    )
                elif cell_value == PLAYER_O:
                    btn.configure(
                        text="O",
                        fg=self.color_player_o,
                        bg=self.color_last_move if (r == last_row and c == last_col) else self.color_board_bg
                    )
                else:
                    btn.configure(text="", bg=self.color_cell_default)

    def _display_step_metrics(self, metrics: dict) -> None:
        """Hiển thị thời gian và số nút duyệt của nước đi gần nhất."""
        time_taken = metrics.get("time_taken", 0.0)
        nodes_count = metrics.get("nodes_evaluated", 0)
        is_exceeded = metrics.get("is_time_exceeded", False)

        warning_text = " [VƯỢT GIỚI HẠN!]" if is_exceeded else ""
        self.metrics_label.configure(
            text=f"Thời gian: {time_taken:.4f}s | Số nút duyệt: {nodes_count:,}{warning_text}"
        )

    def _finish_game(self, winner: Optional[int]) -> None:
        """Xử lý khi ván đấu kết thúc."""
        self.is_game_running = False

        # Vô hiệu hóa các nút bàn cờ
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                self.cell_buttons[r][c].configure(state="disabled")

        if winner == PLAYER_X:
            message = "Quân X chiến thắng!"
            self.status_label.configure(text=f"🏆 {message}", fg=self.color_player_x)
        elif winner == PLAYER_O:
            message = "Quân O chiến thắng!"
            self.status_label.configure(text=f"🏆 {message}", fg=self.color_player_o)
        else:
            message = "Hai bên hòa cờ!"
            self.status_label.configure(text=f"🤝 {message}", fg="#6C757D")

        messagebox.showinfo("Kết quả trận đấu", message)


def run_gui_application() -> None:
    """Khởi động ứng dụng giao diện đồ họa GUI."""
    root = tk.Tk()
    app = CaroGUI(root)
    root.mainloop()


if __name__ == "__main__":
    run_gui_application()
