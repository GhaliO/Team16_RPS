# Game_Modes/vs_computer.py

import cv2
import mediapipe as mp
import random
import time
from utils.gesture_detector import detect_hand_shape
from utils.ui_helpers import choose_difficulty, show_end_screen, draw_game_overlay

def get_computer_choice(difficulty, player_history):
    choices = ["Rock", "Paper", "Scissors"]

    if difficulty == "1":
        return random.choice(choices)

    elif difficulty == "2":
        if not player_history:
            return random.choice(choices)
        last_move = player_history[-1]
        counter = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}
        counter_move = counter[last_move]
        remaining_choices = [c for c in choices if c != counter_move]
        return random.choices([counter_move, *remaining_choices], weights=[0.7, 0.15, 0.15])[0]

    elif difficulty == "3":
        if len(player_history) < 3:
            return random.choice(choices)
        most_common = max(set(player_history), key=player_history.count)
        counter = {"Rock": "Paper", "Paper": "Scissors", "Scissors": "Rock"}
        return counter[most_common]

    else:
        return random.choice(choices)

def play():
    difficulty = choose_difficulty()

    cap = cv2.VideoCapture(0)
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils

    player_score = 0
    computer_score = 0
    round_num = 1
    player_history = []
    locked_result = None
    computer_choice = None
    display_timer = 0

    last_gesture = None
    gesture_timer_start = None
    lock_delay_seconds = 3

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(rgb)

        user_gesture = None
        if result.multi_hand_landmarks:
            for hand_landmarks in result.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                user_gesture = detect_hand_shape(hand_landmarks.landmark)
                break

        key = cv2.waitKey(10) & 0xFF

        if user_gesture:
            if user_gesture == last_gesture:
                if gesture_timer_start is None:
                    gesture_timer_start = time.time()
                elif time.time() - gesture_timer_start >= lock_delay_seconds:
                    computer_choice = get_computer_choice(difficulty, player_history)
                    player_history.append(user_gesture)

                    if user_gesture == computer_choice:
                        winner = "Tie!"
                    elif (user_gesture == "Rock" and computer_choice == "Scissors") or \
                         (user_gesture == "Paper" and computer_choice == "Rock") or \
                         (user_gesture == "Scissors" and computer_choice == "Paper"):
                        winner = "You Win!"
                        player_score += 1
                    else:
                        winner = "Computer Wins!"
                        computer_score += 1

                    locked_result = {
                        "player": user_gesture,
                        "computer": computer_choice,
                        "winner": winner
                    }
                    round_num += 1
                    display_timer = 60
                    gesture_timer_start = None
            else:
                last_gesture = user_gesture
                gesture_timer_start = time.time()
        else:
            last_gesture = None
            gesture_timer_start = None

        if user_gesture and gesture_timer_start:
            time_left = lock_delay_seconds - int(time.time() - gesture_timer_start)
            if time_left > 0:
                cv2.putText(frame, f"Locking in {time_left}...", (10, 120),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

        display = draw_game_overlay(
            frame,
            player_gesture=user_gesture if display_timer > 0 else None,
            opponent_gesture=computer_choice if display_timer > 0 else None,
            player_score=player_score,
            opponent_score=computer_score,
            mode="vs_computer",
            round_num=round_num,
            round_result=locked_result["winner"] if display_timer > 0 and locked_result else None,
            show_gestures=(display_timer > 0)
        )


        cv2.imshow("Play vs Computer", display)

        if display_timer > 0:
            display_timer -= 1

        if key == ord('q') or player_score == 5 or computer_score == 5:
            break

    cap.release()
    cv2.destroyAllWindows()

    result = "You Win!" if player_score == 5 else "You Lose!" if computer_score == 5 else "Game Over"
    score_line = f"Final Score: You {player_score} - {computer_score} CPU"
    cv2.waitKey(500)
    choice = show_end_screen(result, score_line, window_name="Play vs Computer")

    if choice == "restart":
        play()
    elif choice == "menu":
        return
    elif choice == "quit":
        exit()
