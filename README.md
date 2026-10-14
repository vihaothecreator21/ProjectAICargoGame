AI Caro Arena (5x5 - Thắng 4)

Dự án môn Trí tuệ Nhân tạo: Xây dựng trò chơi Caro 5x5 người-máy và khảo sát các tác tử **Minimax**, **Alpha-Beta Pruning**, **Heuristic** và **Move Ordering**.

---

 Cấu trúc thư mục

```text
Project_AI_Caro/
├── config.py                 # Cấu hình hằng số (5x5, thắng 4)
├── main.py                   # Menu chạy ứng dụng (GUI / CLI)
├── requirements.txt          # Thư viện (matplotlib, pandas, numpy)
├── README.md                 # Hướng dẫn dự án
├── docs/                     # Tài liệu thuyết minh kỹ thuật
├── core/                     # Game Engine & Bàn cờ (Thành viên 1)
├── agents/                   # Interface & Các tác tử AI (Thành viên 1, 2, 3)
└── experiments/              # Thực nghiệm & Biểu đồ (Thành viên 3)
 Phân công công việcThành viênNhiệm vụCác file chínhTrạng tháiThành viên 1Game Engine, Logic & Giao diệnconfig.py, core/, ui/, main.pyHoàn tất 100%Thành viên 2AI Core (Heuristic, Minimax, Alpha-Beta)heuristic.py, minimax_agent.py, alphabeta_agent.pyĐang thực hiệnThành viên 3Baseline Greedy & Thực nghiệmgreedy_agent.py, runner.py, plot.pyĐang thực hiện🚀 Hướng dẫn nhanhBash# 1. Cài đặt thư viện phụ thuộc
pip install -r requirements.txt

# 2. Chạy ứng dụng (Menu chọn GUI / CLI)
python main.py

# 3. Chạy thực nghiệm đấu tự động (30 ván)
python experiments/runner.py

# 4. Xuất biểu đồ phân tích số liệu
python experiments/plot.py
