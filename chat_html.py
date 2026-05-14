import time
import threading
import numpy as np

from flask import Flask, request, jsonify, render_template_string
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
        "keywords": [
            "box", "cube", "case", "container",
            "pick up the box", "grab the box", "hold the box",
            "盒子", "方盒", "箱子", "拿盒子", "抓盒子"
        ],
    },
    {
        "command": "tissue",
        "keywords": [
            "tissue", "paper", "napkin", "paper towel",
            "pick up the tissue", "grab the tissue", "hold the tissue",
            "纸巾", "抽纸", "餐巾纸", "纸", "拿纸", "拿纸巾", "抓纸巾"
        ],
    },
    {
        "command": "bottle",
        "keywords": [
            "bottle", "water bottle", "cup",
            "pick up the bottle", "grab the bottle", "hold the bottle", "water",
            "瓶子", "水瓶", "杯子", "拿瓶子", "抓瓶子","水"
        ],
    },
    {
        "command": "ok",
        "keywords": [
            "ok", "okay", "ok gesture", "make ok", "make an ok sign",
            "show ok", "show me ok",
            "OK", "手势ok", "ok手势", "手势-OK"
        ],
    },
    {
        "command": "rock",
        "keywords": [
            "rock", "rock gesture", "rock sign", "rock and roll",
            "make rock", "show rock",
            "摇滚", "rock手势", "手势rock", "手势-rock"
        ],
    },
    {
        "command": "gesture",
        "keywords": [
            "run", "gesture", "gestures", "all gestures",
            "show all gestures", "demo", "demonstration",
            "show me all gestures",
            "手势", "全部手势", "所有手势", "做一遍", "演示", "展示"
        ],
    },
    {
        "command": "open",
        "keywords": [
            "open", "reset", "restore", "back to normal", "home",
            "open hand", "reset hand",
            "打开", "张开", "复位", "恢复", "恢复原状", "回到原位"
        ],
    },
    {
        "command": "close",
        "keywords": [
            "close", "fist", "clench", "grip", "close hand",
            "make a fist",
            "关闭", "握拳", "握住", "合上"
        ],
    },
]


COMMAND_REPLY = {
    "box": "好的，我来执行 box 动作。",
    "tissue": "好的，我来执行 tissue 动作。",
    "bottle": "好的，我来执行 bottle 动作。",
    "ok": "好的，我来做 OK 手势。",
    "rock": "好的，我来做 rock 手势。",
    "gesture": "好的，我来运行完整手势序列，最后停在 rock。",
    "open": "好的，已复位到 open。",
    "close": "好的，我来执行 close 动作。",
}


def extract_command(text):
    text_original = text.strip()
    text_lower = text_original.lower()

    for rule in KEYWORD_RULES:
        for keyword in rule["keywords"]:
            if keyword.lower() in text_lower:
                return rule["command"]

    return None


# =========================
# Command Execution
# =========================

robot_lock = threading.Lock()


def run_robot_command(command):
    with robot_lock:
        if command == "open":
            move_pose(POSES["open"])
            return

        if command == "gesture":
            time.sleep(3)
            gesture_sequence()
            return

        time.sleep(3)
        move_pose(POSES[command])


# =========================
# Flask Web App
# =========================

app = Flask(__name__)


HTML_PAGE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>EmbodiedGPT</title>
    <style>
        :root {
            --bg: #212121;
            --panel: #2f2f2f;
            --panel-light: #3a3a3a;
            --text: #f5f5f5;
            --muted: #b4b4b4;
            --border: #454545;
            --user: #2f2f2f;
            --assistant: #212121;
            --accent: #10a37f;
            --accent-hover: #0d8f70;
            --danger: #d9534f;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            height: 100vh;
            background: var(--bg);
            color: var(--text);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Arial, sans-serif;
            display: flex;
            flex-direction: column;
        }

        header {
            height: 58px;
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 21px;
            font-weight: 700;
            letter-spacing: 0.2px;
        }

        #chat {
            flex: 1;
            overflow-y: auto;
            padding: 24px 0 150px;
        }

        .message {
            width: 100%;
            display: flex;
            justify-content: center;
            padding: 14px 16px;
        }

        .message-inner {
            width: min(820px, 100%);
            display: flex;
            gap: 14px;
            line-height: 1.6;
            font-size: 15px;
        }

        .avatar {
            width: 30px;
            height: 30px;
            border-radius: 50%;
            flex-shrink: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 13px;
            font-weight: 700;
        }

        .avatar.user {
            background: #5a5a5a;
        }

        .avatar.assistant {
            background: var(--accent);
        }

        .bubble {
            white-space: pre-wrap;
            word-break: break-word;
            padding-top: 2px;
        }

        .composer-wrap {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            background: linear-gradient(to top, var(--bg) 80%, rgba(33,33,33,0));
            padding: 20px 16px 26px;
            display: flex;
            justify-content: center;
        }

        .composer {
            width: min(820px, 100%);
            background: var(--panel);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 10px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.25);
        }

        textarea {
            width: 100%;
            min-height: 52px;
            max-height: 170px;
            resize: none;
            border: none;
            outline: none;
            background: transparent;
            color: var(--text);
            font-size: 15px;
            line-height: 1.5;
            padding: 8px 10px;
            font-family: inherit;
        }

        textarea::placeholder {
            color: var(--muted);
        }

        .composer-actions {
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 4px 2px 0;
            gap: 10px;
        }

        .hint {
            color: var(--muted);
            font-size: 12px;
            padding-left: 8px;
        }

        .buttons {
            display: flex;
            gap: 8px;
        }

        button {
            border: none;
            outline: none;
            border-radius: 999px;
            padding: 9px 14px;
            font-size: 14px;
            cursor: pointer;
            color: white;
            background: var(--panel-light);
        }

        button:hover {
            filter: brightness(1.08);
        }

        #sendBtn {
            background: var(--accent);
        }

        #sendBtn:hover {
            background: var(--accent-hover);
        }

        #resetBtn {
            background: #4a4a4a;
        }

        #status {
            position: fixed;
            top: 70px;
            right: 18px;
            color: var(--muted);
            font-size: 13px;
            background: rgba(47,47,47,0.9);
            border: 1px solid var(--border);
            border-radius: 999px;
            padding: 8px 12px;
        }

        @media (max-width: 640px) {
            header {
                justify-content: flex-start;
                padding-left: 18px;
            }

            .hint {
                display: none;
            }

            button {
                padding: 8px 12px;
            }
        }
    </style>
</head>
<body>
    <header>EmbodiedGPT</header>

    <div id="status">Ready</div>

    <main id="chat">
        <div class="message">
            <div class="message-inner">
                <div class="avatar assistant">E</div>
                <div class="bubble">你好，我是 EmbodiedGPT。你可以输入：帮我拿瓶子、make an OK gesture、run all gestures、reset the hand。</div>
            </div>
        </div>
    </main>

    <div class="composer-wrap">
        <div class="composer">
            <textarea id="input" placeholder="输入一句话，按 Enter 发送，Shift + Enter 换行"></textarea>
            <div class="composer-actions">
                <div class="hint">Enter 发送 · Shift + Enter 换行</div>
                <div class="buttons">
                    <button id="resetBtn">复位</button>
                    <button id="sendBtn">发送</button>
                </div>
            </div>
        </div>
    </div>

    <script>
        const chat = document.getElementById("chat");
        const input = document.getElementById("input");
        const sendBtn = document.getElementById("sendBtn");
        const resetBtn = document.getElementById("resetBtn");
        const statusEl = document.getElementById("status");

        function scrollToBottom() {
            chat.scrollTop = chat.scrollHeight;
        }

        function addMessage(role, text) {
            const wrapper = document.createElement("div");
            wrapper.className = "message";

            const inner = document.createElement("div");
            inner.className = "message-inner";

            const avatar = document.createElement("div");
            avatar.className = "avatar " + role;
            avatar.textContent = role === "user" ? "U" : "E";

            const bubble = document.createElement("div");
            bubble.className = "bubble";
            bubble.textContent = text;

            inner.appendChild(avatar);
            inner.appendChild(bubble);
            wrapper.appendChild(inner);
            chat.appendChild(wrapper);

            scrollToBottom();
        }

        function setStatus(text) {
            statusEl.textContent = text;
        }

        async function sendMessage() {
            const text = input.value.trim();
            if (!text) return;

            addMessage("user", text);
            input.value = "";
            setStatus("Executing...");

            try {
                const res = await fetch("/api/chat", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({ message: text })
                });

                const data = await res.json();

                addMessage("assistant", data.reply || "已处理。");
                setStatus(data.status || "Ready");
            } catch (err) {
                addMessage("assistant", "执行失败：" + err.message);
                setStatus("Error");
            }
        }

        async function resetHand() {
            addMessage("user", "复位");
            setStatus("Resetting...");

            try {
                const res = await fetch("/api/reset", {
                    method: "POST"
                });

                const data = await res.json();

                addMessage("assistant", data.reply || "已复位。");
                setStatus(data.status || "Ready");
            } catch (err) {
                addMessage("assistant", "复位失败：" + err.message);
                setStatus("Error");
            }
        }

        input.addEventListener("keydown", function(e) {
            if (e.key === "Enter" && !e.shiftKey) {
                e.preventDefault();
                sendMessage();
            }
        });

        sendBtn.addEventListener("click", sendMessage);
        resetBtn.addEventListener("click", resetHand);

        scrollToBottom();
    </script>
</body>
</html>
"""


@app.route("/")
def index():
    return render_template_string(HTML_PAGE)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json(force=True)
    message = data.get("message", "").strip()

    if not message:
        return jsonify({
            "reply": "请输入一句话。",
            "status": "Ready"
        })

    command = extract_command(message)

    if command is None:
        return jsonify({
            "reply": "我没有识别到对应动作。你可以换一种说法，例如：pick up the bottle、show me OK、run all gestures、reset the hand。",
            "status": "No match"
        })

    if robot_lock.locked():
        return jsonify({
            "reply": "当前机械手还在执行动作，请稍后再发送新的指令。",
            "status": "Busy"
        })

    try:
        run_robot_command(command)

        return jsonify({
            "reply": COMMAND_REPLY.get(command, "动作已完成。"),
            "status": "Ready"
        })

    except Exception as e:
        return jsonify({
            "reply": f"执行失败：{str(e)}",
            "status": "Error"
        })


@app.route("/api/reset", methods=["POST"])
def api_reset():
    if robot_lock.locked():
        return jsonify({
            "reply": "当前机械手还在执行动作，请稍后再复位。",
            "status": "Busy"
        })

    try:
        run_robot_command("open")

        return jsonify({
            "reply": "已复位到 open。",
            "status": "Ready"
        })

    except Exception as e:
        return jsonify({
            "reply": f"复位失败：{str(e)}",
            "status": "Error"
        })


# =========================
# Start Server
# =========================

if __name__ == "__main__":
    try:
        torque_on()
        print("Torque On")
    except Exception as e:
        print(f"Torque On failed: {e}")

    print("EmbodiedGPT is running at http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=False)