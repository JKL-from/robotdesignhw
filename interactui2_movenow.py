import time
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from rustypot import Scs0009PyController


# =========================
# Basic Config
# =========================

Side = 1

MaxSpeed = 7
CloseSpeed = 3

MiddlePos = [3, 0, -5, -8, -2, 5, -12, 0]

SERIAL_PORT = "COM11"
BAUDRATE = 1000000
TIMEOUT = 0.5


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
# UI Helper
# =========================

def get_speed():
    return int(speed_var.get())


def update_value_label(var, label):
    label.config(text=f"{int(float(var.get()))}°")


def safe_call(func):
    try:
        func()
    except Exception as e:
        messagebox.showerror("Control Error", str(e))


# 防止拖动太快时疯狂发送指令
# 单位：毫秒
REALTIME_DELAY_MS = 30

pending_jobs = {
    "Index": None,
    "Middle": None,
    "Ring": None,
    "Thumb": None,
}


def realtime_move_finger(finger_name):
    """
    滑块一变化就调用这个函数。
    这里用了 root.after 做防抖：
    用户拖动很快时，不会每一个像素都发一次指令，
    而是每隔约 30ms 发送一次最后的目标位置。
    """

    if finger_name == "Index":
        update_value_label(index_a1_var, index_a1_label)
        update_value_label(index_a2_var, index_a2_label)

    elif finger_name == "Middle":
        update_value_label(middle_a1_var, middle_a1_label)
        update_value_label(middle_a2_var, middle_a2_label)

    elif finger_name == "Ring":
        update_value_label(ring_a1_var, ring_a1_label)
        update_value_label(ring_a2_var, ring_a2_label)

    elif finger_name == "Thumb":
        update_value_label(thumb_a1_var, thumb_a1_label)
        update_value_label(thumb_a2_var, thumb_a2_label)

    old_job = pending_jobs.get(finger_name)
    if old_job is not None:
        root.after_cancel(old_job)

    new_job = root.after(
        REALTIME_DELAY_MS,
        lambda: send_realtime_command(finger_name)
    )

    pending_jobs[finger_name] = new_job


def send_realtime_command(finger_name):
    speed = get_speed()

    try:
        if finger_name == "Index":
            Move_Index(
                int(index_a1_var.get()),
                int(index_a2_var.get()),
                speed
            )

        elif finger_name == "Middle":
            Move_Middle(
                int(middle_a1_var.get()),
                int(middle_a2_var.get()),
                speed
            )

        elif finger_name == "Ring":
            Move_Ring(
                int(ring_a1_var.get()),
                int(ring_a2_var.get()),
                speed
            )

        elif finger_name == "Thumb":
            Move_Thumb(
                int(thumb_a1_var.get()),
                int(thumb_a2_var.get()),
                speed
            )

    except Exception as e:
        messagebox.showerror("Realtime Move Error", str(e))

    finally:
        pending_jobs[finger_name] = None


def realtime_move_all():
    """
    用于 Open / Close preset。
    """
    speed = get_speed()

    try:
        Move_Index(int(index_a1_var.get()), int(index_a2_var.get()), speed)
        Move_Middle(int(middle_a1_var.get()), int(middle_a2_var.get()), speed)
        Move_Ring(int(ring_a1_var.get()), int(ring_a2_var.get()), speed)
        Move_Thumb(int(thumb_a1_var.get()), int(thumb_a2_var.get()), speed)

    except Exception as e:
        messagebox.showerror("Move All Error", str(e))


def apply_open_preset():
    index_a1_var.set(-35)
    index_a2_var.set(35)

    middle_a1_var.set(-35)
    middle_a2_var.set(35)

    ring_a1_var.set(-35)
    ring_a2_var.set(35)

    thumb_a1_var.set(-35)
    thumb_a2_var.set(35)

    refresh_all_labels()
    realtime_move_all()


def apply_close_preset():
    index_a1_var.set(90)
    index_a2_var.set(-90)

    middle_a1_var.set(90)
    middle_a2_var.set(-90)

    ring_a1_var.set(90)
    ring_a2_var.set(-90)

    thumb_a1_var.set(90)
    thumb_a2_var.set(-90)

    refresh_all_labels()
    realtime_move_all()


def torque_on():
    try:
        c.write_torque_enable(1, 1)
    except Exception as e:
        messagebox.showerror("Torque Error", str(e))


def torque_off():
    try:
        c.write_torque_enable(1, 2)
    except Exception as e:
        messagebox.showerror("Torque Error", str(e))


def torque_free():
    try:
        c.write_torque_enable(1, 3)
    except Exception as e:
        messagebox.showerror("Torque Error", str(e))


# =========================
# UI Layout
# =========================

root = tk.Tk()
root.title("Realtime Robotic Hand Finger UI")
root.geometry("760x580")

main_frame = ttk.Frame(root, padding=16)
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(
    main_frame,
    text="Realtime Robotic Hand Finger Controller",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=8)


# Speed Control

speed_frame = ttk.LabelFrame(main_frame, text="Speed", padding=10)
speed_frame.pack(fill="x", pady=8)

speed_var = tk.IntVar(value=MaxSpeed)

speed_slider = ttk.Scale(
    speed_frame,
    from_=1,
    to=10,
    orient="horizontal",
    variable=speed_var
)
speed_slider.pack(side="left", fill="x", expand=True, padx=8)

speed_value_label = ttk.Label(speed_frame, textvariable=speed_var, width=5)
speed_value_label.pack(side="left")


# Finger Control Creator

def create_finger_control(parent, finger_name, default_a1=0, default_a2=0):
    frame = ttk.LabelFrame(parent, text=finger_name, padding=10)
    frame.pack(fill="x", pady=8)

    a1_var = tk.IntVar(value=default_a1)
    a2_var = tk.IntVar(value=default_a2)

    # Angle 1
    a1_row = ttk.Frame(frame)
    a1_row.pack(fill="x", pady=4)

    ttk.Label(a1_row, text="Angle 1", width=10).pack(side="left")

    a1_value_label = ttk.Label(a1_row, text=f"{default_a1}°", width=8)
    a1_value_label.pack(side="right")

    a1_slider = ttk.Scale(
        a1_row,
        from_=-90,
        to=90,
        orient="horizontal",
        variable=a1_var,
        command=lambda event: realtime_move_finger(finger_name)
    )
    a1_slider.pack(side="left", fill="x", expand=True, padx=8)

    # Angle 2
    a2_row = ttk.Frame(frame)
    a2_row.pack(fill="x", pady=4)

    ttk.Label(a2_row, text="Angle 2", width=10).pack(side="left")

    a2_value_label = ttk.Label(a2_row, text=f"{default_a2}°", width=8)
    a2_value_label.pack(side="right")

    a2_slider = ttk.Scale(
        a2_row,
        from_=-90,
        to=90,
        orient="horizontal",
        variable=a2_var,
        command=lambda event: realtime_move_finger(finger_name)
    )
    a2_slider.pack(side="left", fill="x", expand=True, padx=8)

    return a1_var, a2_var, a1_value_label, a2_value_label


index_a1_var, index_a2_var, index_a1_label, index_a2_label = create_finger_control(
    main_frame,
    "Index",
    -35,
    35
)

middle_a1_var, middle_a2_var, middle_a1_label, middle_a2_label = create_finger_control(
    main_frame,
    "Middle",
    -35,
    35
)

ring_a1_var, ring_a2_var, ring_a1_label, ring_a2_label = create_finger_control(
    main_frame,
    "Ring",
    -35,
    35
)

thumb_a1_var, thumb_a2_var, thumb_a1_label, thumb_a2_label = create_finger_control(
    main_frame,
    "Thumb",
    -35,
    35
)


def refresh_all_labels():
    update_value_label(index_a1_var, index_a1_label)
    update_value_label(index_a2_var, index_a2_label)

    update_value_label(middle_a1_var, middle_a1_label)
    update_value_label(middle_a2_var, middle_a2_label)

    update_value_label(ring_a1_var, ring_a1_label)
    update_value_label(ring_a2_var, ring_a2_label)

    update_value_label(thumb_a1_var, thumb_a1_label)
    update_value_label(thumb_a2_var, thumb_a2_label)


# Global Buttons

global_button_frame = ttk.Frame(main_frame)
global_button_frame.pack(fill="x", pady=12)

ttk.Button(
    global_button_frame,
    text="Open Preset",
    command=apply_open_preset
).pack(side="left", expand=True, fill="x", padx=5)

ttk.Button(
    global_button_frame,
    text="Close Preset",
    command=apply_close_preset
).pack(side="left", expand=True, fill="x", padx=5)


torque_button_frame = ttk.Frame(main_frame)
torque_button_frame.pack(fill="x", pady=6)

ttk.Button(
    torque_button_frame,
    text="Torque On",
    command=torque_on
).pack(side="left", expand=True, fill="x", padx=5)

ttk.Button(
    torque_button_frame,
    text="Torque Off",
    command=torque_off
).pack(side="left", expand=True, fill="x", padx=5)

ttk.Button(
    torque_button_frame,
    text="Free",
    command=torque_free
).pack(side="left", expand=True, fill="x", padx=5)


try:
    torque_on()
except Exception:
    pass

root.mainloop()