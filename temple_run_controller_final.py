import cv2
import mediapipe as mp
import pyautogui
import time
from collections import deque

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.75)
mp_draw = mp.solutions.drawing_utils

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# State variables
position_history = deque(maxlen=4)
cooldown = 0.3  # seconds
last_gesture_time = time.time()
last_action = ""
fist_triggered = False

# Helper: Get hand center
def get_hand_center(handLms):
    landmarks = [handLms.landmark[i] for i in [0, 5, 9]]
    avg_x = sum([lm.x for lm in landmarks]) / len(landmarks)
    avg_y = sum([lm.y for lm in landmarks]) / len(landmarks)
    return int(avg_x * 640), int(avg_y * 480)

# Helper: Count fingers up accurately (thumb + fingers)
def fingers_up(handLms):
    fingers = []

    # Thumb
    if handLms.landmark[4].x < handLms.landmark[3].x:
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tip_ids = [8, 12, 16, 20]
    for tip_id in tip_ids:
        if handLms.landmark[tip_id].y < handLms.landmark[tip_id - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)

# Gesture detection from hand movement
def detect_smoothed_gesture():
    global last_gesture_time, last_action

    if len(position_history) < 4:
        return None

    x_move = position_history[-1][0] - position_history[0][0]
    y_move = position_history[-1][1] - position_history[0][1]
    time_gap = time.time() - last_gesture_time

    if time_gap < cooldown:
        return None

    threshold = 45
    gesture = None

    if x_move < -threshold:
        pyautogui.press('left')
        gesture = "LEFT"
    elif x_move > threshold:
        pyautogui.press('right')
        gesture = "RIGHT"
    elif y_move < -threshold:
        pyautogui.press('up')
        gesture = "JUMP"
    elif y_move > threshold:
        pyautogui.press('down')
        gesture = "SLIDE"

    if gesture:
        last_gesture_time = time.time()
        last_action = gesture
    return gesture

while True:
    success, img = cap.read()
    img = cv2.flip(img, 1)
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    gesture_text = ""
    finger_count = 0

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)

            finger_count = fingers_up(handLms)

            # ✊ Closed palm detected (FIST)
            if finger_count < 2:
                if not fist_triggered:
                    pyautogui.press('space')  # Pause/resume
                    gesture_text = "SPACE Triggered (Pause/Resume)"
                    fist_triggered = True
            else:
                fist_triggered = False  # Reset for next fist
                # 🖐️ Open hand - continue tracking
                cx, cy = get_hand_center(handLms)
                position_history.append((cx, cy))
                gesture = detect_smoothed_gesture()
                if gesture:
                    gesture_text = f"Gesture: {gesture}"

    # Overlay texts
    if last_action:
        cv2.putText(img, f"Last: {last_action}", (10, 40),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    if gesture_text:
        cv2.putText(img, gesture_text, (10, 80),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    # Show finger count for debugging
    cv2.putText(img, f"Fingers: {finger_count}", (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

    cv2.imshow("Temple Run Gesture Controller (Final)", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
