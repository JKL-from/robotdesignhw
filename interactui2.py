import time
import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

from rustypot import Scs0009PyController


# =========================
# Basic Config
# =========================

Side = 1  # 1 = Right Hand, 2 = Left Hand

MaxSpeed = 7
CloseSpeed = 3

# Replace values by your calibration results
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
# Preset Hand Functions
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


# =========================
# UI Helper Functions
# =========================

def get_speed():
    return int(speed_var.get())


def update_value_label(var, label):
    label.config(text=f"{int(float(var.get()))}°")


def safe_move(move_func, angle_1, angle_2, speed):
    try:
        move_func(angle_1, angle_2, speed)
    except Exception as e:
        messagebox.showerror("Move Error", str(e))


def move_one_finger(finger_name):
    speed = get_speed()

    if finger_name == "Index":
        a1 = int(index_a1_var.get())
        a2 = int(index_a2_var.get())
        safe_move(Move_Index, a1, a2, speed)

    elif finger_name == "Middle":
        a1 = int(middle_a1_var.get())
        a2 = int(middle_a2_var.get())
        safe_move(Move_Middle, a1, a2, speed)

    elif finger_name == "Ring":
        a1 = int(ring_a1_var.get())
        a2 = int(ring_a2_var.get())
        safe_move(Move_Ring, a1, a2, speed)

    elif finger_name == "Thumb":
        a1 = int(thumb_a1_var.get())
        a2 = int(thumb_a2_var.get())
        safe_move(Move_Thumb, a1, a2, speed)


def move_all_fingers():
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
    move_all_fingers()


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
    move_all_fingers()


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
root.title("Robotic Hand Finger UI")
root.geometry("760x620")

main_frame = ttk.Frame(root, padding=16)
main_frame.pack(fill="both", expand=True)

title_label = ttk.Label(
    main_frame,
    text="Robotic Hand Finger Controller",
    font=("Arial", 18, "bold")
)
title_label.pack(pady=8)


# =========================
# Speed Control
# =========================

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


# =========================
# Finger Control Creator
# =========================

def create_finger_control(parent, finger_name, default_a1=0, default_a2=0):
    frame = ttk.LabelFrame(parent, text=finger_name, padding=10)
    frame.pack(fill="x", pady=8)

    a1_var = tk.IntVar(value=default_a1)
    a2_var = tk.IntVar(value=default_a2)

    # Angle 1 row
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
        command=lambda event: update_value_label(a1_var, a1_value_label)
    )
    a1_slider.pack(side="left", fill="x", expand=True, padx=8)

    # Angle 2 row
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
        command=lambda event: update_value_label(a2_var, a2_value_label)
    )
    a2_slider.pack(side="left", fill="x", expand=True, padx=8)

    # Move button
    button_row = ttk.Frame(frame)
    button_row.pack(fill="x", pady=6)

    move_button = ttk.Button(
        button_row,
        text=f"Move {finger_name}",
        command=lambda: move_one_finger(finger_name)
    )
    move_button.pack(side="right")

    return a1_var, a2_var, a1_value_label, a2_value_label


# =========================
# Create Four Finger Controls
# =========================

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


# =========================
# Global Buttons
# =========================

global_button_frame = ttk.Frame(main_frame)
global_button_frame.pack(fill="x", pady=12)

ttk.Button(
    global_button_frame,
    text="Move All Fingers",
    command=move_all_fingers
).pack(side="left", expand=True, fill="x", padx=5)

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


# =========================
# Start
# =========================

try:
    torque_on()
except Exception:
    pass

root.mainloop()