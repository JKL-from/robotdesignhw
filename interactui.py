import time
import tkinter as tk
from tkinter import ttk
import numpy as np

from rustypot import Scs0009PyController


# ===== 基础配置 =====
Side = 1  # 1 = Right Hand, 2 = Left Hand

MaxSpeed = 7
CloseSpeed = 3

MiddlePos = [3, 0, -5, -8, -2, 5, -12, 0]

c = Scs0009PyController(
    serial_port="COM11",
    baudrate=1000000,
    timeout=0.5,
)


# ===== 四个手指的底层 Move 函数 =====
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


# ===== 把一个输入值映射成两个电机角度 =====
def value_to_angles(value):
    """
    value 范围：-90 到 90
    输出：Angle_1, Angle_2

    这里采用你的原始逻辑：
    张开类似 (-35, 35)
    闭合类似 (90, -90)

    所以一个值 value 可以控制成：
    Angle_1 = value
    Angle_2 = -value
    """
    angle_1 = value
    angle_2 = -value
    return angle_1, angle_2


def move_finger(finger_name, value, speed):
    angle_1, angle_2 = value_to_angles(value)

    if finger_name == "Index":
        Move_Index(angle_1, angle_2, speed)
    elif finger_name == "Middle":
        Move_Middle(angle_1, angle_2, speed)
    elif finger_name == "Ring":
        Move_Ring(angle_1, angle_2, speed)
    elif finger_name == "Thumb":
        Move_Thumb(angle_1, angle_2, speed)


def move_all(value, speed):
    angle_1, angle_2 = value_to_angles(value)

    Move_Index(angle_1, angle_2, speed)
    Move_Middle(angle_1, angle_2, speed)
    Move_Ring(angle_1, angle_2, speed)
    Move_Thumb(angle_1, angle_2, speed)


# ===== UI 控制逻辑 =====
def update_finger_from_slider(finger_name, var, label, speed_var):
    value = int(float(var.get()))
    speed = int(float(speed_var.get()))

    label.config(text=f"{value}°")
    move_finger(finger_name, value, speed)


def update_all_from_slider(var, label, speed_var):
    value = int(float(var.get()))
    speed = int(float(speed_var.get()))

    label.config(text=f"{value}°")
    move_all(value, speed)


def set_open():
    speed = int(speed_var.get())
    value = -35

    index_var.set(value)
    middle_var.set(value)
    ring_var.set(value)
    thumb_var.set(value)
    all_var.set(value)

    move_all(value, speed)


def set_close():
    speed = int(speed_var.get())
    value = 90

    index_var.set(value)
    middle_var.set(value)
    ring_var.set(value)
    thumb_var.set(value)
    all_var.set(value)

    move_all(value, speed)


def torque_on():
    c.write_torque_enable(1, 1)


def torque_off():
    c.write_torque_enable(1, 2)


def torque_free():
    c.write_torque_enable(1, 3)


# ===== 创建 UI =====
root = tk.Tk()
root.title("Four Finger Control UI")
root.geometry("520x520")

main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill="both", expand=True)

title = ttk.Label(main_frame, text="Robotic Hand Finger Control", font=("Arial", 18))
title.pack(pady=10)

# 速度控制
speed_frame = ttk.LabelFrame(main_frame, text="Speed", padding=10)
speed_frame.pack(fill="x", pady=10)

speed_var = tk.IntVar(value=MaxSpeed)

speed_slider = ttk.Scale(
    speed_frame,
    from_=1,
    to=10,
    orient="horizontal",
    variable=speed_var
)
speed_slider.pack(fill="x")

speed_label = ttk.Label(speed_frame, textvariable=speed_var)
speed_label.pack()


# 单个手指控制函数
def create_finger_control(parent, name):
    frame = ttk.LabelFrame(parent, text=name, padding=10)
    frame.pack(fill="x", pady=6)

    var = tk.IntVar(value=0)
    value_label = ttk.Label(frame, text="0°", width=8)
    value_label.pack(side="right")

    slider = ttk.Scale(
        frame,
        from_=-90,
        to=90,
        orient="horizontal",
        variable=var,
        command=lambda event: update_finger_from_slider(name, var, value_label, speed_var)
    )
    slider.pack(side="left", fill="x", expand=True)

    return var


index_var = create_finger_control(main_frame, "Index")
middle_var = create_finger_control(main_frame, "Middle")
ring_var = create_finger_control(main_frame, "Ring")
thumb_var = create_finger_control(main_frame, "Thumb")


# 全部手指一起控制
all_frame = ttk.LabelFrame(main_frame, text="All Fingers", padding=10)
all_frame.pack(fill="x", pady=10)

all_var = tk.IntVar(value=0)
all_label = ttk.Label(all_frame, text="0°", width=8)
all_label.pack(side="right")

all_slider = ttk.Scale(
    all_frame,
    from_=-90,
    to=90,
    orient="horizontal",
    variable=all_var,
    command=lambda event: update_all_from_slider(all_var, all_label, speed_var)
)
all_slider.pack(side="left", fill="x", expand=True)


# 快捷按钮
button_frame = ttk.Frame(main_frame)
button_frame.pack(fill="x", pady=15)

ttk.Button(button_frame, text="Open Hand", command=set_open).pack(side="left", expand=True, padx=5)
ttk.Button(button_frame, text="Close Hand", command=set_close).pack(side="left", expand=True, padx=5)

torque_frame = ttk.Frame(main_frame)
torque_frame.pack(fill="x", pady=10)

ttk.Button(torque_frame, text="Torque On", command=torque_on).pack(side="left", expand=True, padx=5)
ttk.Button(torque_frame, text="Torque Off", command=torque_off).pack(side="left", expand=True, padx=5)
ttk.Button(torque_frame, text="Free", command=torque_free).pack(side="left", expand=True, padx=5)


# 启动时打开扭矩
torque_on()

root.mainloop()