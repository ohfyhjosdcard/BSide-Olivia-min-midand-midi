import mido
import tkinter as tk
from tkinter import filedialog, messagebox
import webbrowser
import os

# ================= 全局配置区 =================
APP_NAME = "MIDI 上传修复工具"
TARGET_GAME = "BSide Olivia Lin"
AUTHOR = "史上第一个杨某人"
HOMEPAGE_URL = "https://www.miyoushe.com/dby/accountCenter/postList?id=373282433"


# ================= 核心修复逻辑 =================
def fix_midi_file(input_path):
    """读取MIDI，添加延音踏板(CC64)，保存为新文件"""
    try:
        if not input_path.lower().endswith(('.mid', '.midi')):
            return False, "格式错误：请上传 .mid 或 .midi 文件"

        mid = mido.MidiFile(input_path, clip=True)
        new_mid = mido.MidiFile(type=1, ticks_per_beat=mid.ticks_per_beat)
        new_track = mido.MidiTrack()
        new_mid.tracks.append(new_track)

        # 添加全程延音踏板信号
        new_track.append(mido.Message('control_change', control=64, value=127, time=0))

        # 复制原有音符数据
        for track in mid.tracks:
            for msg in track:
                if msg.type not in ('sysex', 'meta'):
                    new_track.append(msg.copy(time=msg.time))

        # 保存文件
        dir_name = os.path.dirname(input_path)
        base_name = os.path.basename(input_path)
        output_path = os.path.join(dir_name, f"[已修复]_{base_name}")
        new_mid.save(output_path)
        return True, output_path

    except Exception as e:
        return False, f"处理失败: {str(e)}\n建议重新导出或寻找其他资源"


# ================= 主窗口逻辑 =================
def create_main_window():
    """创建并显示主功能窗口"""
    root = tk.Tk()
    root.title(f"{APP_NAME} - {AUTHOR}")
    root.geometry("500x350")
    root.resizable(False, False)

    # 居中显示
    root.update_idletasks()
    x = (root.winfo_screenwidth() - 500) // 2
    y = (root.winfo_screenheight() - 350) // 2
    root.geometry(f"+{x}+{y}")

    # 主容器
    main_frame = tk.Frame(root, padx=40, pady=40)
    main_frame.pack(fill="both", expand=True)

    # 标题
    tk.Label(main_frame, text=APP_NAME, font=("Microsoft YaHei", 20, "bold")).pack(pady=(0, 5))
    tk.Label(main_frame, text=f"🎯 专用于: {TARGET_GAME}", font=("Microsoft YaHei", 12), fg="#d32f2f").pack(pady=(0, 20))
    tk.Label(main_frame, text="点击下方按钮选择本地 MIDI 文件\n程序将自动添加延音踏板信息以适配上传",
             font=("Microsoft YaHei", 10), fg="#666", justify="center").pack(pady=(0, 20))

    # 修复按钮
    def select_and_fix():
        file_path = filedialog.askopenfilename(title="选择 MIDI 文件", filetypes=[("MIDI Files", "*.mid *.midi")])
        if file_path:
            root.config(cursor="wait")
            root.update()
            success, result = fix_midi_file(file_path)
            root.config(cursor="")
            if success:
                messagebox.showinfo("修复成功", f"文件已保存至:\n{result}")
            else:
                messagebox.showerror("修复失败", result)

    tk.Button(main_frame, text="📂 选择 MIDI 文件并开始修复", font=("Microsoft YaHei", 12),
              bg="#2196F3", fg="white", padx=20, pady=10, cursor="hand2", command=select_and_fix).pack(pady=10)

    # 作者链接
    def open_homepage(event):
        webbrowser.open(HOMEPAGE_URL)

    author_link = tk.Label(main_frame, text=f"Author: {AUTHOR} (点击访问主页)",
                           font=("Microsoft YaHei", 9), fg="#1976D2", cursor="hand2")
    author_link.pack(pady=(20, 0))
    author_link.bind("<Button-1>", open_homepage)

    # ================= 许可弹窗逻辑 =================
    def show_license():
        top = tk.Toplevel(root)
        top.title("使用许可与免责声明")
        top.geometry("450x400")
        top.resizable(False, False)
        top.transient(root)
        top.grab_set()  # 锁定主窗口，必须点击同意才能继续

        # 居中显示弹窗
        top.update_idletasks()
        x = (root.winfo_screenwidth() - 450) // 2
        y = (root.winfo_screenheight() - 400) // 2
        top.geometry(f"+{x}+{y}")

        text_content = f"""欢迎使用 {APP_NAME} ({TARGET_GAME} 专用版)

【重要声明】
目前本作者已经测试了上述问题，可以通过网上下载进行解决。至于其他问题，请自行探索。如有疑问，请通过发送邮件或私信的形式联系。其他的方式请自行探索。

【适用范围】
目前该软件仅适用于：{TARGET_GAME}
(搜索对应的中文名即可找到相关资源)

【版权与责任】
1. 此代码由 AI 生成，如有问题请联系作者：{AUTHOR}
2. 请勿商用，仅供学习交流使用。
3. 如果有问题请联系私信作者。

点击下方“我已阅读相关许可”即表示您同意以上条款。"""

        text_widget = tk.Text(top, wrap="word", font=("Microsoft YaHei", 10), padx=10, pady=10, bd=0)
        text_widget.insert("1.0", text_content)
        text_widget.config(state="disabled")
        text_widget.pack(fill="both", expand=True, padx=10, pady=(10, 5))

        def agree():
            top.grab_release()
            top.destroy()

        tk.Button(top, text="我已阅读相关许可", bg="#4CAF50", fg="white",
                  font=("Microsoft YaHei", 11, "bold"), padx=20, pady=8, command=agree).pack(pady=(0, 15))

    # 程序启动时立即弹出许可窗口
    root.after(100, show_license)
    root.mainloop()


# ================= 程序入口 =================
if __name__ == "__main__":
    create_main_window()