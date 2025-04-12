# utils/ui_helpers.py

import cv2
import numpy as np


def choose_difficulty():
    """
    Clickable difficulty selection screen.
    Returns: "1", "2", "3", or "back"
    """
    screen = np.ones((500, 700, 3), dtype=np.uint8) * 30

    buttons = {
        "1": {"text": "Easy (Test your luck - Random)", "pos": (100, 160, 500, 50)},
        "2": {"text": "Medium (Counters your last move)", "pos": (100, 230, 500, 50)},
        "3": {"text": "Hard (Unbeatable AI - Predicts you)", "pos": (100, 300, 500, 50)},
        "back": {"text": "Back to Menu", "pos": (250, 390, 200, 50)},
    }

    hovered = None
    result = [None]

    def mouse_handler(event, x, y, flags, param):
        nonlocal hovered
        hovered = None
        if event == cv2.EVENT_MOUSEMOVE:
            for key, b in buttons.items():
                bx, by, bw, bh = b["pos"]
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    hovered = key
        elif event == cv2.EVENT_LBUTTONDOWN:
            for key, b in buttons.items():
                bx, by, bw, bh = b["pos"]
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    result[0] = key
                    cv2.destroyAllWindows()

    cv2.namedWindow("Select Difficulty")
    cv2.setMouseCallback("Select Difficulty", mouse_handler)

    while result[0] is None:
        screen[:] = (30, 30, 30)
        cv2.putText(screen, "Choose Difficulty", (180, 90), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        for key, b in buttons.items():
            x, y, w, h = b["pos"]
            color = (80, 180, 255) if hovered == key else (50, 150, 255)
            cv2.rectangle(screen, (x, y), (x + w, y + h), color, -1)
            cv2.putText(screen, b["text"], (x + 10, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)

        cv2.imshow("Select Difficulty", screen)
        cv2.waitKey(1)

    return result[0]



def show_end_screen(result_text, score_text, window_name="Game Over"):
    """
    Displays a clickable end screen with the game result and options.
    Draws it inside the same window as the game (e.g., "Play vs Computer").
    Returns: "restart", "menu", or "quit"
    """

    screen = np.ones((500, 700, 3), dtype=np.uint8) * 30
    button_color = (50, 150, 255)
    button_hover = (80, 180, 255)
    text_color = (255, 255, 255)
    buttons = {
        "restart": {"text": "Play Again", "pos": (100, 350, 200, 60)},
        "menu": {"text": "Main Menu", "pos": (270, 350, 200, 60)},
        "quit": {"text": "Quit", "pos": (440, 350, 150, 60)}
    }

    hovered = None
    return_value = [None]

    def mouse_handler(event, x, y, flags, param):
        nonlocal hovered
        hovered = None
        if event == cv2.EVENT_MOUSEMOVE:
            for key, data in buttons.items():
                bx, by, bw, bh = data["pos"]
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    hovered = key
        elif event == cv2.EVENT_LBUTTONDOWN:
            for key, data in buttons.items():
                bx, by, bw, bh = data["pos"]
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    return_value[0] = key
                    cv2.setMouseCallback(window_name, lambda *args : None)  # Unhook callback
                    cv2.destroyWindow(window_name)

    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, mouse_handler)

    while return_value[0] is None:
        screen[:] = (30, 30, 30)

        # Main result text
        color = (0, 255, 0) if "Win" in result_text else (0, 0, 255) if "Lose" in result_text else (255, 255, 0)
        cv2.putText(screen, result_text, (150, 130), cv2.FONT_HERSHEY_SIMPLEX, 2, color, 5)
        cv2.putText(screen, score_text, (150, 200), cv2.FONT_HERSHEY_SIMPLEX, 0.9, text_color, 2)

        # Buttons
        for key, data in buttons.items():
            x, y, w, h = data["pos"]
            color = button_hover if hovered == key else button_color
            cv2.rectangle(screen, (x, y), (x + w, y + h), color, -1)
            cv2.putText(screen, data["text"], (x + 10, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2)

        cv2.imshow(window_name, screen)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return_value[0] = "quit"

    return return_value[0]


def show_multiplayer_intro():
    """
    Clickable intro screen for multiplayer mode.
    Returns: "start" or "back"
    """
    screen = np.ones((500, 700, 3), dtype=np.uint8) * 30

    buttons = {
        "start": {"text": "Start Game", "pos": (200, 370, 140, 50)},
        "back": {"text": "Back to Menu", "pos": (360, 370, 160, 50)},
    }

    hovered = None
    result = [None]

    def mouse_handler(event, x, y, flags, param):
        nonlocal hovered
        hovered = None
        if event == cv2.EVENT_MOUSEMOVE:
            for key, b in buttons.items():
                bx, by, bw, bh = b["pos"]
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    hovered = key
        elif event == cv2.EVENT_LBUTTONDOWN:
            for key, b in buttons.items():
                bx, by, bw, bh = b["pos"]
                if bx <= x <= bx + bw and by <= y <= by + bh:
                    result[0] = key
                    cv2.destroyAllWindows()

    cv2.namedWindow("Multiplayer Mode")
    cv2.setMouseCallback("Multiplayer Mode", mouse_handler)

    while result[0] is None:
        screen[:] = (30, 30, 30)
        cv2.putText(screen, "🎮 Multiplayer Mode", (180, 60), cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)

        lines = [
            "Both players: show your hand gestures!",
            "",
            "Why use this mode?",
            "- Automatically detects both players' moves",
            "- Tracks score across rounds",
            "- Declares the winner for fairness",
            "- Great for tournament-style play!",
        ]

        y = 120
        for line in lines:
            cv2.putText(screen, line, (50, y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            y += 35

        for key, b in buttons.items():
            x, y, w, h = b["pos"]
            color = (80, 180, 255) if hovered == key else (50, 150, 255)
            cv2.rectangle(screen, (x, y), (x + w, y + h), color, -1)
            cv2.putText(screen, b["text"], (x + 10, y + 35), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (30, 30, 30), 2)

        cv2.imshow("Multiplayer Mode", screen)
        cv2.waitKey(1)

    return result[0]

def draw_game_overlay(frame, player_gesture, opponent_gesture,
                      player_score, opponent_score,
                      mode="vs_computer", round_num=1, round_result=None,
                      show_gestures=True):
    """
    Wraps the webcam frame inside a styled UI canvas and adds overlay text.
    `show_gestures`: if False, gesture names/emojis will be hidden.
    """
    padding_top = 50
    padding_left = 30

    frame_h, frame_w = frame.shape[:2]
    canvas_w = frame_w + 300
    canvas_h = frame_h + 100

    canvas = np.ones((canvas_h, canvas_w, 3), dtype=np.uint8) * 30
    cv2.rectangle(canvas, (0, 0), (canvas_w, 40), (0, 0, 0), -1)
    title = "ROCK PAPER SCISSORS - VS COMPUTER" if mode == "vs_computer" else "ROCK PAPER SCISSORS - MULTIPLAYER"
    cv2.putText(canvas, title, (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)

    canvas[padding_top:padding_top + frame_h, padding_left:padding_left + frame_w] = frame
    cv2.putText(canvas, "Player 1", (padding_left, padding_top + frame_h + 30),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)


    cv2.rectangle(canvas,
                  (padding_left - 2, padding_top - 2),
                  (padding_left + frame_w + 2, padding_top + frame_h + 2),
                  (255, 255, 255), 2)
    cv2.line(canvas, (padding_left + frame_w + 20, 50),
             (padding_left + frame_w + 20, padding_top + frame_h), (100, 100, 100), 2)

    cv2.putText(canvas, f"Round {round_num}", (frame_w + 50, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    score_text = f"Score: You {player_score} - {opponent_score} {'CPU' if mode == 'vs_computer' else 'P2'}"
    cv2.putText(canvas, score_text, (frame_w + 50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    gesture_colors = {"Rock": (0, 0, 255), "Paper": (0, 255, 0), "Scissors": (255, 0, 0)}

    if show_gestures:
        if player_gesture:
            cv2.putText(canvas, f"You: {player_gesture}", (frame_w + 50, 160),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        gesture_colors.get(player_gesture, (255, 255, 255)), 2)

        if opponent_gesture:
            label = "CPU" if mode == "vs_computer" else "P2"
            cv2.putText(canvas, f"{label}: {opponent_gesture}", (frame_w + 50, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7,
                        gesture_colors.get(opponent_gesture, (255, 255, 255)), 2)

        cv2.putText(canvas, "Hold gesture for 3 sec to lock", (frame_w + 50, 280),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    cv2.putText(canvas, "[Q] Quit", (frame_w + 50, 310),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (200, 200, 200), 1)

    # Show winner message below gestures
    if round_result:
        result_color = (0, 255, 0) if "Win" in round_result else (0, 0, 255) if "Lose" in round_result else (255, 255, 0)
        cv2.putText(canvas, f"Result: {round_result}", (frame_w + 50, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, result_color, 2)

    cv2.rectangle(canvas, (0, 0), (canvas.shape[1] - 1, canvas.shape[0] - 1), (100, 100, 100), 2)

    return canvas
