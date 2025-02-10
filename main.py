import cv2
import numpy as np
import mediapipe as mp
import pyautogui
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=2)

# Get screen size
screen_width, screen_height = pyautogui.size()

# Start video capture
cap = cv2.VideoCapture(0)

# Cursor smoothing
prev_x, prev_y = 0, 0
smoothing_factor = 0.2

# Gesture state tracking
dragging = False
last_swipe_time = time.time()
last_zoom_time = time.time()

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # Flip image for natural interaction
    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Process frame
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        hand_positions = []
        for hand_landmarks in results.multi_hand_landmarks:
            # Extract key landmarks
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]

            x, y = int(index_tip.x * w), int(index_tip.y * h)

            # Convert to screen coordinates
            screen_x = np.interp(x, [0, w], [0, screen_width])
            screen_y = np.interp(y, [0, h], [0, screen_height])

            # Apply adaptive smoothing
            alpha = 0.3 if abs(screen_x - prev_x) > 50 else 0.1
            screen_x = prev_x * (1 - alpha) + screen_x * alpha
            screen_y = prev_y * (1 - alpha) + screen_y * alpha
            prev_x, prev_y = screen_x, screen_y

            # Move mouse
            pyautogui.moveTo(screen_x, screen_y, duration=0.05)

            # Store hand position for gestures
            hand_positions.append((wrist.x, wrist.y))

            # Dynamic click threshold based on hand size
            hand_size = np.linalg.norm(np.array([wrist.x, wrist.y]) - np.array([index_tip.x, index_tip.y]))
            click_threshold = hand_size * w * 0.5

            # Click gesture (index & thumb close)
            thumb_x, thumb_y = int(thumb_tip.x * w), int(thumb_tip.y * h)
            if abs(thumb_x - x) < click_threshold and abs(thumb_y - y) < click_threshold:
                pyautogui.click()

            # Right-click gesture (thumb & middle finger close)
            middle_x, middle_y = int(middle_tip.x * w), int(middle_tip.y * h)
            if abs(thumb_x - middle_x) < click_threshold and abs(thumb_y - middle_y) < click_threshold:
                pyautogui.rightClick()

            # Scroll gesture (Index & Middle Finger spacing)
            if y < middle_y - 30:
                pyautogui.scroll(10)
            elif y > middle_y + 30:
                pyautogui.scroll(-10)

            # Drag & Drop Gesture
            if abs(thumb_x - x) < click_threshold and abs(thumb_y - y) < click_threshold:
                if not dragging:
                    pyautogui.mouseDown()
                    dragging = True
            else:
                if dragging:
                    pyautogui.mouseUp()
                    dragging = False

            # Zoom In/Out Gesture (Pinch Gesture with timer)
            hand_distance = np.linalg.norm(np.array([index_tip.x, index_tip.y]) - np.array([thumb_tip.x, thumb_tip.y]))
            if time.time() - last_zoom_time > 0.5:  # Prevent rapid zooming
                if hand_distance > 0.08:
                    pyautogui.hotkey('ctrl', '+')
                elif hand_distance < 0.03:
                    pyautogui.hotkey('ctrl', '-')
                last_zoom_time = time.time()

            # Draw landmarks
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        # Swipe Left/Right Gesture (Switch Tabs/Windows with velocity check)
        if len(hand_positions) == 2:
            left_hand, right_hand = sorted(hand_positions, key=lambda x: x[0])
            velocity = abs(right_hand[0] - left_hand[0]) / (time.time() - last_swipe_time)
            if velocity > 0.3 and time.time() - last_swipe_time > 1:
                pyautogui.hotkey("alt", "tab")
                last_swipe_time = time.time()

    # Display output
    cv2.imshow("Hand Gesture Mouse", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
