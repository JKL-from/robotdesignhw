import time
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
# Combined Gesture Sequence
# =========================

def gesture_sequence():
    """
    输入 run 或 手势 时执行：
    旧代码里的手势动作全部做一遍，
    然后做 ok，
    最后做 rock，并停在 rock。
    """

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

    "手势": "gesture",
    "run": "gesture",
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
            if pose_name == "gesture":
                time.sleep(3)
                gesture_sequence()

            else:
                if pose_name != "open":
                    time.sleep(3)

                move_pose(POSES[pose_name])

        except Exception as e:
            print(f"执行失败：{e}")


if __name__ == "__main__":
    main()