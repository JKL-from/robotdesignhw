import time
import numpy as np

from rustypot import Scs0009PyController


# =========================
# Basic Config
# =========================

SERIAL_PORT = "COM11"
BAUDRATE = 1000000
TIMEOUT = 0.5

MaxSpeed = 7
CloseSpeed = 3

# Replace values by your calibration results
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
# Pose Execution
# =========================

def move_pose(pose):
    speed = pose["speed"]

    Move_Index(
        pose["index"][0],
        pose["index"][1],
        speed
    )

    Move_Middle(
        pose["middle"][0],
        pose["middle"][1],
        speed
    )

    Move_Ring(
        pose["ring"][0],
        pose["ring"][1],
        speed
    )

    Move_Thumb(
        pose["thumb"][0],
        pose["thumb"][1],
        speed
    )


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
# Command Aliases
# =========================

ALIASES = {
    "box": "box",
    "盒子": "box",

    "tissue": "tissue",
    "纸巾": "tissue",
    "纸": "tissue",

    "bottle": "bottle",
    "瓶子": "bottle",
    "瓶": "bottle",

    "ok": "ok",
    "OK": "ok",
    "手势ok": "ok",
    "手势-OK": "ok",

    "rock": "rock",
    "摇滚": "rock",
    "手势rock": "rock",
    "手势-rock": "rock",

    "open": "open",
    "打开": "open",
    "张开": "open",

    "close": "close",
    "关闭": "close",
    "握拳": "close",
}


# =========================
# Main Loop
# =========================

def main():
    try:
        torque_on()
    except Exception as e:
        print(f"Torque On failed: {e}")

    while True:
        cmd = input("请输入动作: ").strip()

        if cmd == "":
            continue

        if cmd in ["q", "quit", "exit", "退出"]:
            break

        if cmd == "on":
            try:
                torque_on()
            except Exception as e:
                print(f"Torque On failed: {e}")
            continue

        if cmd == "off":
            try:
                torque_off()
            except Exception as e:
                print(f"Torque Off failed: {e}")
            continue

        if cmd == "free":
            try:
                torque_free()
            except Exception as e:
                print(f"Torque Free failed: {e}")
            continue

        pose_name = ALIASES.get(cmd)

        if pose_name is None:
            print(f"未知动作：{cmd}")
            continue

        try:
            time.sleep(3)
            move_pose(POSES[pose_name])
        except Exception as e:
            print(f"执行失败：{e}")


if __name__ == "__main__":
    main()