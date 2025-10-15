
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

HISTORY_FILE = "history.csv"

def Mo_Giao_Dien_Lich_Su():
    root = tk.Tk()
    root.title("📜 Lịch sử chạy thuật toán Pikachu")
    root.geometry("900x600")
    root.configure(bg="#e9eff6")

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#bfd6ec")
    style.configure("Treeview", font=("Segoe UI", 10), rowheight=25)

    tk.Label(root, text="LỊCH SỬ THUẬT TOÁN", font=("Arial", 18, "bold"),
             bg="#e9eff6", fg="#1a4b7a").pack(pady=10)

    # Đọc dữ liệu
    try:
        df = pd.read_csv(HISTORY_FILE)
    except FileNotFoundError:
        messagebox.showinfo("Thông báo", "Chưa có lịch sử nào được ghi!")
        root.destroy()
        return

    frame = ttk.Frame(root)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    cols = list(df.columns)
    tree = ttk.Treeview(frame, columns=cols, show="headings")
    for col in cols:
        tree.heading(col, text=col)
        tree.column(col, width=130, anchor=tk.CENTER)

    for _, row in df.iterrows():
        tree.insert("", tk.END, values=list(row))

    vsb = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
    tree.configure(yscroll=vsb.set)
    vsb.pack(side="right", fill="y")
    tree.pack(fill=tk.BOTH, expand=True)

    def So_Sanh():
        import numpy as np
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

        # đọc dữ liệu
        try:
            df = pd.read_csv(HISTORY_FILE)
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không đọc được file lịch sử: {e}")
            return

        # --- Tự động tìm tên cột (hỗ trợ biến thể và BOM) ---
        cols = list(df.columns)
        def find_col(possible_names):
            for c in cols:
                cn = c.strip().lower()
                for nm in possible_names:
                    if nm in cn:
                        return c
            return None

        algo_col = find_col(["thuật", "thuat", "algorithm", "algo", "thuật toán"])
        level_col = find_col(["level", "cấp", "cap", "lev"])
        time_col  = find_col(["thời gian", "thoi gian", "time"])
        mem_col   = find_col(["bộ nhớ", "bo nho", "memory", "mem"])

        if not algo_col or not level_col or not time_col or not mem_col:
            messagebox.showerror("Lỗi", f"File lịch sử thiếu cột cần thiết.\nTìm được cột: algo={algo_col}, level={level_col}, time={time_col}, mem={mem_col}")
            print("Columns in CSV:", cols)
            return

        # Chuẩn hoá dataframe: strip strings, làm lowercase cho thuật toán
        df = df.copy()
        # remove leading/trailing spaces in headers already handled by find_col returning actual column name

        # Chuẩn hóa thuật toán (loại khoảng trắng thừa)
        df[algo_col] = df[algo_col].astype(str).str.strip()

        # Chuyển Level về số nguyên, loại bỏ hàng có Level không hợp lệ
        df[level_col] = pd.to_numeric(df[level_col], errors="coerce")
        df = df.dropna(subset=[level_col])
        df[level_col] = df[level_col].astype(int)

        # Chuyển time và mem sang số (nếu có lỗi, đặt NaN)
        df[time_col] = pd.to_numeric(df[time_col], errors="coerce")
        df[mem_col]  = pd.to_numeric(df[mem_col], errors="coerce")

        # --- nhóm theo thuật toán ---
        REQUIRED_LEVELS = list(range(1, 7))  # 1..6

        algos_ok = []
        avg_times = []
        avg_mems = []

        grouped = df.groupby(algo_col)

        debug_lines = []
        for algo, sub in grouped:
            # loại bỏ khoảng trắng thừa trong tên thuật toán
            algo_norm = algo.strip()

            # tính mean cho từng level (nếu có duplicate cho cùng level thì lấy mean)
            per_level = sub.groupby(level_col).agg({
                time_col: "mean",
                mem_col: "mean"
            }).sort_index()

            present_levels = list(per_level.index.astype(int))
            debug_lines.append(f"{algo_norm}: levels present = {present_levels}")

            # kiểm tra đủ các level 1..6
            if not set(REQUIRED_LEVELS).issubset(set(present_levels)):
                # không đủ, bỏ qua
                continue

            # lấy mean của 6 level (mean of per-level means)
            times_for_6 = per_level.loc[REQUIRED_LEVELS, time_col].values
            mems_for_6  = per_level.loc[REQUIRED_LEVELS, mem_col].values

            avg_time = float(np.nanmean(times_for_6))
            avg_mem  = float(np.nanmean(mems_for_6))

            algos_ok.append(algo_norm)
            avg_times.append(round(avg_time, 3))
            avg_mems.append(round(avg_mem, 3))

        # In debug ra console (giúp bạn biết thuật toán nào thiếu level nào)
        print("=== Debug: levels present per algorithm ===")
        for ln in debug_lines:
            print(ln)

        if len(algos_ok) == 0:
            message = "Chưa có thuật toán nào hoàn thành đủ 6 level!\n\n"
            message += "Thông tin chi tiết đã được in ra console (terminal) để kiểm tra các level hiện có mỗi thuật toán."
            messagebox.showinfo("Thông báo", message)
            return

        # tạo DataFrame tóm tắt
        summary = pd.DataFrame({
            "Thuật toán": algos_ok,
            "AVG_TIME": avg_times,
            "AVG_MEMORY": avg_mems
        }).set_index("Thuật toán")

        # Hiển thị popup mới với bảng tóm tắt và biểu đồ
        win = tk.Toplevel(root)
        win.title("So sánh trung bình (thuật toán đã hoàn thành 6 level)")
        win.geometry("900x600")
        win.configure(bg="#eef2f5")

        # show table (đầy đủ 3 cột: Thuật toán | AVG_TIME | AVG_MEMORY)
        frame_top = ttk.Frame(win)
        frame_top.pack(fill=tk.BOTH, expand=False, padx=10, pady=6)

        tbl = ttk.Treeview(frame_top, columns=["Algo", "AVG_TIME", "AVG_MEMORY"], show="headings", height=6)
        tbl.heading("Algo", text="Thuật toán")
        tbl.heading("AVG_TIME", text="AVG_TIME (s)")
        tbl.heading("AVG_MEMORY", text="AVG_MEMORY (MB)")
        tbl.column("Algo", anchor=tk.CENTER, width=200)
        tbl.column("AVG_TIME", anchor=tk.CENTER, width=180)
        tbl.column("AVG_MEMORY", anchor=tk.CENTER, width=180)

        for algo in summary.index:
            tbl.insert("", tk.END, values=(algo, summary.loc[algo, "AVG_TIME"], summary.loc[algo, "AVG_MEMORY"]))

        tbl.pack(fill=tk.X, padx=10, pady=6)

        # Vẽ biểu đồ (2 cột)
        fig, axes = plt.subplots(1, 2, figsize=(10, 4))
        summary["AVG_TIME"].plot(kind="bar", ax=axes[0], color="#4fa6d5", rot=45)
        axes[0].set_title("Thời gian trung bình (s)")
        axes[0].set_ylabel("Seconds")
        axes[0].grid(axis="y", linestyle="--", alpha=0.6)

        summary["AVG_MEMORY"].plot(kind="bar", ax=axes[1], color="#f5a623", rot=45)
        axes[1].set_title("Bộ nhớ trung bình (MB)")
        axes[1].set_ylabel("MB")
        axes[1].grid(axis="y", linestyle="--", alpha=0.6)

        plt.tight_layout()

        canvas = FigureCanvasTkAgg(fig, master=win)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn_frame = ttk.Frame(win)
        btn_frame.pack(fill=tk.X, pady=6)
        ttk.Button(btn_frame, text="Đóng", command=win.destroy).pack(side=tk.RIGHT, padx=12)


    ttk.Button(root, text="📊 So sánh", command=So_Sanh,
               style="Accent.TButton").pack(pady=10)
    root.mainloop()
