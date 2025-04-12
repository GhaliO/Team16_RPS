# utils/gesture_detector.py

def detect_hand_shape(landmarks):
    """
    Determines if the hand shape is Rock, Paper, or Scissors based on landmark positions.
    """
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    middle_tip = landmarks[12]
    ring_tip = landmarks[16]
    pinky_tip = landmarks[20]

    # Count extended fingers (ignoring thumb)
    fingers = [index_tip, middle_tip, ring_tip, pinky_tip]
    extended = sum(1 for finger in fingers if finger.y < landmarks[5].y)

    if extended == 0:
        return "Rock"
    elif extended == 2:
        return "Scissors"
    elif extended == 4:
        return "Paper"
    else:
        return None
