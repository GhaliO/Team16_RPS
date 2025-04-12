import cv2
import numpy as np
from Game_Modes import vs_computer, vs_friend

def show_main_menu():
    screen = np.ones((500, 700, 3), dtype=np.uint8) * 30

    button_color = (50, 150, 255)
    button_hover = (80, 180, 255)
    text_color = (255, 255, 255)
    buttons = {
        "computer": {"text": "Play vs Computer", "pos": (200, 180, 300, 60)},
        "friend": {"text": "Play with a Friend", "pos": (200, 260, 300, 60)},
        "quit": {"text": "Quit", "pos": (200, 340, 300, 60)},
    }

    hovered = None
    result = [None]

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
                    result[0] = key
                    cv2.destroyAllWindows()

    cv2.namedWindow("Main Menu")
    cv2.setMouseCallback("Main Menu", mouse_handler)

    while result[0] is None:
        screen[:] = (30, 30, 30)
        cv2.putText(screen, "ROCK PAPER SCISSORS", (130, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.3, (0, 255, 255), 3)

        for key, data in buttons.items():
            x, y, w, h = data["pos"]
            color = button_hover if hovered == key else button_color
            cv2.rectangle(screen, (x, y), (x + w, y + h), color, -1)
            cv2.putText(screen, data["text"], (x + 20, y + 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (30, 30, 30), 2)

        cv2.imshow("Main Menu", screen)
        cv2.waitKey(1)

    return result[0]


def main():
    while True:
        choice = show_main_menu()
        if choice == "computer":
            vs_computer.play()
        elif choice == "friend":
            vs_friend.play()
        elif choice == "quit":
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()
