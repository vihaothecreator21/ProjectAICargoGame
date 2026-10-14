"""
[Thành viên 3] Script trực quan hóa dữ liệu (Plotting & Visualization).
Vẽ các biểu đồ phục vụ cho báo cáo và slide thuyết trình:
1. Biểu đồ tròn/cột: Tỉ lệ Thắng / Hòa / Thua giữa 2 tác tử.
2. Biểu đồ cột: So sánh thời gian trung bình mỗi nước đi.
3. Biểu đồ so sánh số nút duyệt (Nodes evaluated) giữa các thuật toán.
"""

import os
import sys

if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
import matplotlib.pyplot as plt


def plot_win_rate(csv_path: str, output_img: str = "experiments/results/win_rate.png"):
    """Vẽ biểu đồ tỉ lệ thắng/hòa/thua."""
    if not os.path.exists(csv_path):
        print(f"Chưa có file dữ liệu {csv_path}")
        return

    df = pd.read_csv(csv_path)
    counts = df["winner"].value_counts()

    plt.figure(figsize=(6, 6))
    counts.plot(kind="pie", autopct="%1.1f%%", startangle=140, colors=["#4CAF50", "#2196F3", "#FF9800"])
    plt.title("Tỉ lệ Thắng - Hòa - Thua (>= 30 ván)")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig(output_img)
    plt.close()
    print(f"[OK] Đã xuất biểu đồ: {output_img}")


def plot_nodes_and_time(csv_path: str, output_img: str = "experiments/results/nodes_time.png"):
    """Vẽ biểu đồ so sánh thời gian và số nút duyệt trung bình."""
    if not os.path.exists(csv_path):
        return

    df = pd.read_csv(csv_path)

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # So sánh thời gian
    axes[0].bar(["Agent A", "Agent B"], [df["a_avg_time"].mean(), df["b_avg_time"].mean()], color=["#4CAF50", "#2196F3"])
    axes[0].set_title("Thời gian trung bình mỗi nước (giây)")
    axes[0].set_ylabel("Giây")

    # So sánh số nút duyệt
    axes[1].bar(["Agent A", "Agent B"], [df["a_avg_nodes"].mean(), df["b_avg_nodes"].mean()], color=["#FF5722", "#9C27B0"])
    axes[1].set_title("Số nút duyệt trung bình mỗi nước")
    axes[1].set_ylabel("Số lượng nút")

    plt.tight_layout()
    plt.savefig(output_img)
    plt.close()
    print(f"[OK] Đã xuất biểu đồ: {output_img}")


if __name__ == "__main__":
    csv_file = "experiments/results/match_results.csv"
    plot_win_rate(csv_file)
    plot_nodes_and_time(csv_file)
