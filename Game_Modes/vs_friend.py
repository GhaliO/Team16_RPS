# Game_Modes/vs_friend.py

import cv2
import mediapipe as mp
import time
from utils.gesture_detector import detect_hand_shape
from utils.ui_helpers import (
    show_multiplayer_intro,
    show_end_screen,
    draw_game_overlay
)

def play():
    user_choice = show_multiplayer_intro()
    if user_choice == "back":
        return

    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=2, min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    score_p1 = 0
    score_p2 = 0
    round_num = 1
    display_timer = 0
    locked_result = None

    gesture_timer_start = None
    lock_delay_seconds = 3
    last_gestures = [None, None]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        player_gestures = []

        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                gesture = detect_hand_shape(hand_landmarks.landmark)
                player_gestures.append(gesture)

        key = cv2.waitKey(10) & 0xFF

        if len(player_gestures) == 2 and all(player_gestures):
            if player_gestures == last_gestures:
                if gesture_timer_start is None:
                    gesture_timer_start = time.time()
                elif time.time() - gesture_timer_start >= lock_delay_seconds:
                    g1, g2 = player_gestures

                    if g1 == g2:
                        winner = "Tie!"
                    elif (g1 == "Rock" and g2 == "Scissors") or \
                         (g1 == "Paper" and g2 == "Rock") or \
                         (g1 == "Scissors" and g2 == "Paper"):
                        winner = "Player 1 Wins!"
                        score_p1 += 1
                    else:
                        winner = "Player 2 Wins!"
                        score_p2 += 1

                    locked_result = {
                        "p1": g1,
                        "p2": g2,
                        "winner": winner
                    }

                    round_num += 1
                    display_timer = 60
                    gesture_timer_start = None
            else:
                last_gestures = player_gestures
                gesture_timer_start = time.time()
        else:
            last_gestures = [None, None]
            gesture_timer_start = None

        # Show countdown if both hands detected
        if len(player_gestures) == 2 and all(player_gestures) and gesture_timer_start:
            time_left = lock_delay_seconds - int(time.time() - gesture_timer_start)
            if time_left > 0:
                cv2.putText(frame, f"Locking in {time_left}...", (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        # Draw UI
        display = draw_game_overlay(
            frame,
            player_gesture=locked_result['p1'] if display_timer > 0 and locked_result else None,
            opponent_gesture=locked_result['p2'] if display_timer > 0 and locked_result else None,
            player_score=score_p1,
            opponent_score=score_p2,
            mode="vs_friend",
            round_num=round_num,
            round_result=locked_result["winner"] if display_timer > 0 and locked_result else None,
            show_gestures=(display_timer > 0)
        )

        cv2.imshow("Multiplayer Mode", display)

        if display_timer > 0:
            display_timer -= 1
        else:
            locked_result = None

        if key == ord('q') or score_p1 == 5 or score_p2 == 5:
            break

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(500)

    # Game result
    if score_p1 > score_p2:
        result = "Player 1 Wins!"
    elif score_p2 > score_p1:
        result = "Player 2 Wins!"
    else:
        result = "It's a Tie!"

    score_line = f"Final Score: P1 {score_p1} - {score_p2} P2"
    choice = show_end_screen(result, score_line, window_name="Multiplayer Mode")

    if choice == "restart":
        play()
    elif choice == "menu":
        return
    elif choice == "quit":
        exit()
