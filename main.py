
import cv2
import mediapipe as mp
import numpy as np
import os
from datetime import datetime


# ==================================================
# 1. MEDIAPIPE INITIALIZATION
# ==================================================

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)


# ==================================================
# 2. WEBCAM INITIALIZATION
# ==================================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Cannot open webcam")
    hands.close()
    exit()


# ==================================================
# 3. DRAWING VARIABLES
# ==================================================

canvas = None

previous_x = 0
previous_y = 0

colors = [
    (255, 0, 255),    # Magenta
    (255, 0, 0),      # Blue
    (0, 255, 0),      # Green
    (0, 0, 255),      # Red
    (0, 255, 255),    # Yellow
    (255, 255, 255)   # White
]

current_color = colors[0]

brush_thickness = 10
eraser_thickness = 50

drawing_mode = "BRUSH"
gesture_status = "NO HAND"

os.makedirs("output", exist_ok=True)


# ==================================================
# 4. FINGER DETECTION
# ==================================================

def fingers_up(hand_landmarks):

    landmarks = hand_landmarks.landmark

    thumb = landmarks[4].x < landmarks[3].x

    index = landmarks[8].y < landmarks[6].y
    middle = landmarks[12].y < landmarks[10].y
    ring = landmarks[16].y < landmarks[14].y
    pinky = landmarks[20].y < landmarks[18].y

    return [thumb, index, middle, ring, pinky]


# ==================================================
# 5. PROFESSIONAL COLOR TOOLBAR
# ==================================================

def draw_toolbar(frame):

    height, width, _ = frame.shape

    # Dark header background
    cv2.rectangle(
        frame,
        (0, 0),
        (width, 110),
        (30, 30, 30),
        -1
    )

    # Application title
    cv2.putText(
        frame,
        "AI VIRTUAL PAINTER",
        (15, 28),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # Color palette
    for i, color in enumerate(colors):

        x1 = 15 + (i * 62)
        y1 = 48
        x2 = x1 + 48
        y2 = 88

        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            color,
            -1
        )

        # Highlight selected color
        if color == current_color:

            cv2.rectangle(
                frame,
                (x1 - 3, y1 - 3),
                (x2 + 3, y2 + 3),
                (255, 255, 255),
                2
            )

    # Active mode panel
    cv2.putText(
        frame,
        "MODE: " + gesture_status,
        (width - 220, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (0, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "TOOL: " + drawing_mode,
        (width - 220, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.5,
        (255, 255, 255),
        1
    )

    # Brush thickness
    cv2.putText(
        frame,
        "SIZE: " + str(brush_thickness),
        (width - 220, 92),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.45,
        (200, 200, 200),
        1
    )


# ==================================================
# 6. BOTTOM CONTROL PANEL
# ==================================================

def draw_bottom_panel(frame):

    height, width, _ = frame.shape

    # Dark bottom background
    cv2.rectangle(
        frame,
        (0, height - 45),
        (width, height),
        (30, 30, 30),
        -1
    )

    instructions = (
        "E: Eraser | B: Brush | C: Clear | "
        "S: Save | [ ]: Size | Q: Quit"
    )

    cv2.putText(
        frame,
        instructions,
        (10, height - 15),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.48,
        (255, 255, 255),
        1
    )


# ==================================================
# 7. MAIN APPLICATION LOOP
# ==================================================

while True:

    success, frame = cap.read()

    if not success:
        print("Webcam frame not received")
        break

    # Mirror webcam
    frame = cv2.flip(frame, 1)

    height, width, _ = frame.shape

    # Create black drawing canvas
    if canvas is None:

        canvas = np.zeros(
            (height, width, 3),
            dtype=np.uint8
        )

    # Convert image to RGB
    rgb_frame = cv2.cvtColor(
        frame,
        cv2.COLOR_BGR2RGB
    )

    results = hands.process(rgb_frame)

    gesture_status = "NO HAND"

    # ==================================================
    # 8. HAND TRACKING
    # ==================================================

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            # Draw hand landmarks
            mp_drawing.draw_landmarks(
                frame,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            fingers = fingers_up(hand_landmarks)

            # Index fingertip position
            x = int(
                hand_landmarks.landmark[8].x * width
            )

            y = int(
                hand_landmarks.landmark[8].y * height
            )

            # ------------------------------------------
            # GESTURE 1: DRAWING
            # ------------------------------------------

            if fingers == [
                False, True, False, False, False
            ]:

                gesture_status = "DRAWING"

                if previous_x != 0 and previous_y != 0:

                    if drawing_mode == "BRUSH":

                        cv2.line(
                            canvas,
                            (previous_x, previous_y),
                            (x, y),
                            current_color,
                            brush_thickness
                        )

                    elif drawing_mode == "ERASER":

                        cv2.line(
                            canvas,
                            (previous_x, previous_y),
                            (x, y),
                            (0, 0, 0),
                            eraser_thickness
                        )

                previous_x = x
                previous_y = y

            # ------------------------------------------
            # GESTURE 2: COLOR SELECTION
            # ------------------------------------------

            elif fingers == [
                False, True, True, False, False
            ]:

                gesture_status = "COLOR SELECTION"

                previous_x = 0
                previous_y = 0

                # Toolbar color selection area
                if 48 < y < 90:

                    for i, color in enumerate(colors):

                        x1 = 15 + (i * 62)
                        x2 = x1 + 48

                        if x1 < x < x2:

                            current_color = color
                            drawing_mode = "BRUSH"

                            break

            # ------------------------------------------
            # GESTURE 3: CLOSED FIST
            # ------------------------------------------

            elif fingers == [
                False, False, False, False, False
            ]:

                gesture_status = "PAUSE"

                previous_x = 0
                previous_y = 0

            # ------------------------------------------
            # OTHER GESTURES
            # ------------------------------------------

            else:

                gesture_status = "IDLE"

                previous_x = 0
                previous_y = 0

    else:

        previous_x = 0
        previous_y = 0


    # ==================================================
    # 9. COMBINE WEBCAM AND DRAWING CANVAS
    # ==================================================

    output = cv2.addWeighted(
        frame,
        1,
        canvas,
        1,
        0
    )

    # Draw redesigned interface on top
    draw_toolbar(output)
    draw_bottom_panel(output)

    cv2.imshow(
        "AI Virtual Painter",
        output
    )


    # ==================================================
    # 10. KEYBOARD CONTROLS
    # ==================================================

    key = cv2.waitKey(1) & 0xFF

    # E = Eraser
    if key == ord('e'):

        drawing_mode = "ERASER"

    # B = Brush
    elif key == ord('b'):

        drawing_mode = "BRUSH"

    # C = Clear canvas
    elif key == ord('c'):

        canvas = np.zeros(
            (height, width, 3),
            dtype=np.uint8
        )

        previous_x = 0
        previous_y = 0

        print("Canvas cleared")

    # S = Save drawing
    elif key == ord('s'):

        filename = datetime.now().strftime(
            "drawing_%Y%m%d_%H%M%S.png"
        )

        save_path = os.path.join(
            "output",
            filename
        )

        cv2.imwrite(save_path, canvas)

        print("Drawing saved:", save_path)

    # Decrease brush size
    elif key == ord('['):

        brush_thickness = max(
            1,
            brush_thickness - 2
        )

    # Increase brush size
    elif key == ord(']'):

        brush_thickness = min(
            50,
            brush_thickness + 2
        )

    # Q = Exit
    elif key == ord('q'):

        break


# ==================================================
# 11. RELEASE RESOURCES
# ==================================================

cap.release()
hands.close()

cv2.destroyAllWindows()

print("AI Virtual Painter closed successfully")
