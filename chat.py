import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from rustypot import Scs0009PyController


# =========================
# Basic Config
# =========================

SERIAL_PORT = "COM11"
BAUDRATE = 1000000
TIMEOUT = 0.5

Side = 1  # 1 = Right Hand, 2 = Left Hand

MaxSpeed = 7
CloseSpeed = 3

MiddlePos = [3, 0, -5, -8, -2, 5, -12, 0]


# =========================
# Controller Init
# =========================

c = Scs0009PyController(
    serial_port=SERIAL_PORT,
    baudrate=BAUDRATE,
    timeout=TIMEOUT,
)


# =========================
# Low-level Move Functions
# =========================

def Move_Index(Angle_1, Angle_2, Speed):
    c.write_goal_speed(1, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(2, Speed)
    time.sleep(0.0002)

    Pos_1 = np.deg2rad(MiddlePos[0] + Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[1] + Angle_2)

    c.write_goal_position(1, Pos_1)
    c.write_goal_position(2, Pos_2)

    time.sleep(0.005)


def Move_Middle(Angle_1, Angle_2, Speed):
    c.write_goal_speed(3, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(4, Speed)
    time.sleep(0.0002)

    Pos_1 = np.deg2rad(MiddlePos[2] + Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[3] + Angle_2)

    c.write_goal_position(3, Pos_1)
    c.write_goal_position(4, Pos_2)

    time.sleep(0.005)


def Move_Ring(Angle_1, Angle_2, Speed):
    c.write_goal_speed(5, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(6, Speed)
    time.sleep(0.0002)

    Pos_1 = np.deg2rad(MiddlePos[4] + Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[5] + Angle_2)

    c.write_goal_position(5, Pos_1)
    c.write_goal_position(6, Pos_2)

    time.sleep(0.005)


def Move_Thumb(Angle_1, Angle_2, Speed):
    c.write_goal_speed(7, Speed)
    time.sleep(0.0002)
    c.write_goal_speed(8, Speed)
    time.sleep(0.0002)

    Pos_1 = np.deg2rad(MiddlePos[6] + Angle_1)
    Pos_2 = np.deg2rad(MiddlePos[7] + Angle_2)

    c.write_goal_position(7, Pos_1)
    c.write_goal_position(8, Pos_2)

    time.sleep(0.005)


# =========================
# Torque Control
# =========================

def torque_on():
    c.write_torque_enable(1, 1)


def torque_off():
    c.write_torque_enable(1, 2)


def torque_free():
    c.write_torque_enable(1, 3)


# =========================
# Old Gesture Functions
# =========================

def OpenHand():
    Move_Index(-35, 35, MaxSpeed)
    Move_Middle(-35, 35, MaxSpeed)
    Move_Ring(-35, 35, MaxSpeed)
    Move_Thumb(-35, 35, MaxSpeed)


def CloseHand():
    Move_Index(90, -90, CloseSpeed)
    Move_Middle(90, -90, CloseSpeed)
    Move_Ring(90, -90, CloseSpeed)
    Move_Thumb(90, -90, CloseSpeed + 1)


def OpenHand_Progressive():
    Move_Index(-35, 35, MaxSpeed - 2)
    time.sleep(0.2)

    Move_Middle(-35, 35, MaxSpeed - 2)
    time.sleep(0.2)

    Move_Ring(-35, 35, MaxSpeed - 2)
    time.sleep(0.2)

    Move_Thumb(-35, 35, MaxSpeed - 2)


def SpreadHand():
    if Side == 1:
        Move_Index(4, 90, MaxSpeed)
        Move_Middle(-32, 32, MaxSpeed)
        Move_Ring(-90, -4, MaxSpeed)
        Move_Thumb(-90, -4, MaxSpeed)

    if Side == 2:
        Move_Index(-60, 0, MaxSpeed)
        Move_Middle(-35, 35, MaxSpeed)
        Move_Ring(-4, 90, MaxSpeed)
        Move_Thumb(-4, 90, MaxSpeed)


def ClenchHand():
    if Side == 1:
        Move_Index(-60, 0, MaxSpeed)
        Move_Middle(-35, 35, MaxSpeed)
        Move_Ring(0, 70, MaxSpeed)
        Move_Thumb(-4, 90, MaxSpeed)

    if Side == 2:
        Move_Index(0, 60, MaxSpeed)
        Move_Middle(-35, 35, MaxSpeed)
        Move_Ring(-70, 0, MaxSpeed)
        Move_Thumb(-90, -4, MaxSpeed)


def Index_Pointing():
    Move_Index(-40, 40, MaxSpeed)
    Move_Middle(90, -90, MaxSpeed)
    Move_Ring(90, -90, MaxSpeed)
    Move_Thumb(90, -90, MaxSpeed)


def Nonono():
    Index_Pointing()

    for i in range(3):
        time.sleep(0.2)
        Move_Index(-10, 80, MaxSpeed)

        time.sleep(0.2)
        Move_Index(-80, 10, MaxSpeed)

    Move_Index(-35, 35, MaxSpeed)
    time.sleep(0.4)


def Perfect():
    if Side == 1:
        Move_Index(50, -50, MaxSpeed)
        Move_Middle(0, 0, MaxSpeed)
        Move_Ring(-20, 20, MaxSpeed)
        Move_Thumb(65, 12, MaxSpeed)

    if Side == 2:
        Move_Index(50, -50, MaxSpeed)
        Move_Middle(0, 0, MaxSpeed)
        Move_Ring(-20, 20, MaxSpeed)
        Move_Thumb(-12, -65, MaxSpeed)


def Victory():
    if Side == 1:
        Move_Index(-15, 65, MaxSpeed)
        Move_Middle(-65, 15, MaxSpeed)
        Move_Ring(90, -90, MaxSpeed)
        Move_Thumb(90, -90, MaxSpeed)

    if Side == 2:
        Move_Index(-65, 15, MaxSpeed)
        Move_Middle(-15, 65, MaxSpeed)
        Move_Ring(90, -90, MaxSpeed)
        Move_Thumb(90, -90, MaxSpeed)


def Scissors():
    Victory()

    if Side == 1:
        for i in range(3):
            time.sleep(0.2)
            Move_Index(-50, 20, MaxSpeed)
            Move_Middle(-20, 50, MaxSpeed)

            time.sleep(0.2)
            Move_Index(-15, 65, MaxSpeed)
            Move_Middle(-65, 15, MaxSpeed)

    if Side == 2:
        for i in range(3):
            time.sleep(0.2)
            Move_Index(-20, 50, MaxSpeed)
            Move_Middle(-50, 20, MaxSpeed)

            time.sleep(0.2)
            Move_Index(-65, 15, MaxSpeed)
            Move_Middle(-15, 65, MaxSpeed)


def Pinched():
    if Side == 1:
        Move_Index(90, -90, MaxSpeed)
        Move_Middle(90, -90, MaxSpeed)
        Move_Ring(90, -90, MaxSpeed)
        Move_Thumb(0, -75, MaxSpeed)

    if Side == 2:
        Move_Index(90, -90, MaxSpeed)
        Move_Middle(90, -90, MaxSpeed)
        Move_Ring(90, -90, MaxSpeed)
        Move_Thumb(75, 5, MaxSpeed)


# =========================
# Pose Execution
# =========================

def move_pose(pose):
    speed = pose["speed"]

    Move_Index(pose["index"][0], pose["index"][1], speed)
    Move_Middle(pose["middle"][0], pose["middle"][1], speed)
    Move_Ring(pose["ring"][0], pose["ring"][1], speed)
    Move_Thumb(pose["thumb"][0], pose["thumb"][1], speed)


# =========================
# Custom Poses
# =========================

POSES = {
    "box": {
        "speed": 7,
        "index":  [51, -28],
        "middle": [28, -40],
        "ring":   [74, -85],
        "thumb":  [14, -14],
    },

    "tissue": {
        "speed": 7,
        "index":  [32, -7],
        "middle": [22, -42],
        "ring":   [79, -90],
        "thumb":  [4, -40],
    },

    "bottle": {
        "speed": 7,
        "index":  [73, -84],
        "middle": [63, -90],
        "ring":   [16, -90],
        "thumb":  [34, -79],
    },

    "ok": {
        "speed": 7,
        "index":  [90, -90],
        "middle": [-35, 35],
        "ring":   [-22, 35],
        "thumb":  [0, -90],
    },

    "rock": {
        "speed": 7,
        "index":  [-81, 18],
        "middle": [90, -90],
        "ring":   [-26, 68],
        "thumb":  [90, 90],
    },

    "open": {
        "speed": 7,
        "index":  [-35, 35],
        "middle": [-35, 35],
        "ring":   [-35, 35],
        "thumb":  [-35, 35],
    },

    "close": {
        "speed": 3,
        "index":  [90, -90],
        "middle": [90, -90],
        "ring":   [90, -90],
        "thumb":  [90, -90],
    },
}


# =========================
# Combined Gesture Sequence
# =========================

def gesture_sequence():
    OpenHand()
    time.sleep(0.5)

    CloseHand()
    time.sleep(1.0)

    OpenHand_Progressive()
    time.sleep(0.5)

    SpreadHand()
    time.sleep(0.6)

    ClenchHand()
    time.sleep(0.6)

    OpenHand()
    time.sleep(0.3)

    Index_Pointing()
    time.sleep(0.5)

    Nonono()
    time.sleep(0.5)

    OpenHand()
    time.sleep(0.3)

    Perfect()
    time.sleep(0.8)

    OpenHand()
    time.sleep(0.4)

    Victory()
    time.sleep(0.8)

    Scissors()
    time.sleep(0.6)

    OpenHand()
    time.sleep(0.4)

    Pinched()
    time.sleep(0.8)

    OpenHand()
    time.sleep(0.4)

    move_pose(POSES["ok"])
    time.sleep(1.0)

    move_pose(POSES["rock"])


# =========================
# Natural Language Matching
# =========================

KEYWORD_RULES = [
    {
        "command": "box",
        "keywords": ["box", "盒子", "方盒", "箱子", "拿盒子", "抓盒子"],
    },
    {
        "command": "tissue",
        "keywords": ["tissue", "纸巾", "抽纸", "餐巾纸", "拿纸", "拿纸巾", "抓纸巾"],
    },
    {
        "command": "bottle",
        "keywords": ["bottle", "瓶子", "水瓶", "杯子", "拿瓶子", "抓瓶子", "thirsty","渴"],
    },
    {
        "command": "ok",
        "keywords": ["ok", "OK", "okay", "手势ok", "ok手势", "手势-OK"],
    },
    {
        "command": "rock",
        "keywords": ["rock", "摇滚", "rock手势", "手势rock", "手势-rock"],
    },
    {
        "command": "gesture",
        "keywords": ["run", "手势", "全部手势", "所有手势", "做一遍", "演示", "展示"],
    },
    {
        "command": "open",
        "keywords": ["open", "打开", "张开", "复位", "恢复", "恢复原状", "回到原位"],
    },
    {
        "command": "close",
        "keywords": ["close", "关闭", "握拳", "握住", "合上"],
    },
]


COMMAND_DISPLAY_NAME = {
    "box": "box / 盒子",
    "tissue": "tissue / 纸巾",
    "bottle": "bottle / 瓶子",
    "ok": "ok / OK手势",
    "rock": "rock / rock手势",
    "gesture": "run / 手势组合动作",
    "open": "open / 复位",
    "close": "close / 握拳",
}


def extract_command(text):
    text_original = text.strip()
    text_lower = text_original.lower()

    for rule in KEYWORD_RULES:
        for keyword in rule["keywords"]:
            keyword_lower = keyword.lower()

            if keyword_lower in text_lower:
                return rule["command"], keyword

    return None, None


# =========================
# UI Command Execution
# =========================

is_running = False
run_lock = threading.Lock()


def set_status(message):
    status_var.set(message)


def execute_command(command):
    global is_running

    with run_lock:
        if is_running:
            root.after(0, lambda: set_status("当前动作还在执行，请稍等。"))
            return

        is_running = True

    try:
        root.after(0, lambda: set_status(f"匹配命令：{COMMAND_DISPLAY_NAME[command]}"))

        if command == "open":
            root.after(0, lambda: set_status("正在复位：open"))
            move_pose(POSES["open"])
            root.after(0, lambda: set_status("已复位。"))

        elif command == "gesture":
            root.after(0, lambda: set_status("匹配到 run，3 秒后执行组合手势。"))
            time.sleep(3)
            gesture_sequence()
            root.after(0, lambda: set_status("组合手势完成，当前停在 rock。"))

        else:
            root.after(0, lambda: set_status(f"3 秒后执行：{COMMAND_DISPLAY_NAME[command]}"))
            time.sleep(3)
            move_pose(POSES[command])
            root.after(0, lambda: set_status(f"动作完成：{COMMAND_DISPLAY_NAME[command]}"))

    except Exception as e:
        root.after(0, lambda: messagebox.showerror("执行失败", str(e)))
        root.after(0, lambda: set_status("执行失败。"))

    finally:
        with run_lock:
            is_running = False


def on_send():
    text = input_text.get("1.0", "end").strip()

    if text == "":
        messagebox.showwarning("提示", "请输入一句话。")
        return

    command, keyword = extract_command(text)

    if command is None:
        set_status("没有匹配到命令。")
        messagebox.showinfo("未匹配", "没有找到对应动作关键词。")
        return

    matched_var.set(f"提取关键词：{keyword}    对应命令：{COMMAND_DISPLAY_NAME[command]}")

    worker = threading.Thread(
        target=execute_command,
        args=(command,),
        daemon=True
    )
    worker.start()


def on_reset():
    matched_var.set("提取关键词：复位    对应命令：open / 复位")

    worker = threading.Thread(
        target=execute_command,
        args=("open",),
        daemon=True
    )
    worker.start()


def on_torque_on():
    try:
        torque_on()
        set_status("Torque On")
    except Exception as e:
        messagebox.showerror("Torque On failed", str(e))


def on_torque_off():
    try:
        torque_off()
        set_status("Torque Off")
    except Exception as e:
        messagebox.showerror("Torque Off failed", str(e))


def on_torque_free():
    try:
        torque_free()
        set_status("Torque Free")
    except Exception as e:
        messagebox.showerror("Torque Free failed", str(e))


# =========================
# UI Layout
# =========================

root = tk.Tk()
root.title("机械手自然语言控制界面")
root.geometry("720x460")

main_frame = ttk.Frame(root, padding=18)
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(
    main_frame,
    text="机械手自然语言控制",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=8)

hint_label = ttk.Label(
    main_frame,
    text="输入一句话，例如：帮我拿瓶子 / 做一个OK手势 / 展示所有手势 / 复位",
    font=("Arial", 10)
)
hint_label.pack(pady=4)

input_frame = ttk.LabelFrame(main_frame, text="输入对话", padding=10)
input_frame.pack(fill="both", expand=True, pady=10)

input_text = tk.Text(input_frame, height=7, font=("Arial", 12))
input_text.pack(fill="both", expand=True)

matched_var = tk.StringVar(value="提取关键词：无    对应命令：无")
matched_label = ttk.Label(
    main_frame,
    textvariable=matched_var,
    font=("Arial", 11)
)
matched_label.pack(fill="x", pady=6)

button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x", pady=10)

send_button = ttk.Button(
    button_frame,
    text="发送并执行",
    command=on_send
)
send_button.pack(side="left", expand=True, fill="x", padx=5)

reset_button = ttk.Button(
    button_frame,
    text="复位 Open",
    command=on_reset
)
reset_button.pack(side="left", expand=True, fill="x", padx=5)

torque_frame = ttk.Frame(main_frame)
torque_frame.pack(fill="x", pady=6)

ttk.Button(
    torque_frame,
    text="Torque On",
    command=on_torque_on
).pack(side="left", expand=True, fill="x", padx=5)

ttk.Button(
    torque_frame,
    text="Torque Off",
    command=on_torque_off
).pack(side="left", expand=True, fill="x", padx=5)

ttk.Button(
    torque_frame,
    text="Free",
    command=on_torque_free
).pack(side="left", expand=True, fill="x", padx=5)

status_var = tk.StringVar(value="状态：等待输入")
status_label = ttk.Label(
    main_frame,
    textvariable=status_var,
    font=("Arial", 10)
)
status_label.pack(fill="x", pady=8)


# =========================
# Start
# =========================

try:
    torque_on()
    set_status("Torque On，等待输入。")
except Exception as e:
    set_status(f"Torque On failed: {e}")

root.mainloop()