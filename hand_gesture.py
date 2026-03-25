import cv2
import mediapipe as mp
import winsound
import threading

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)

played = False

history = []
history_size = 10

def play_sound():
    winsound.Beep(1000, 500)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    gesture = "none"

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)

            lm = handLms.landmark

            # coordinates
            thumb_tip = lm[4].x
            thumb_ip = lm[3].x

            index_tip = lm[8].y
            index_pip = lm[6].y

            middle_tip = lm[12].y
            middle_pip = lm[10].y

            ring_tip = lm[16].y
            ring_pip = lm[14].y

            pinky_tip = lm[20].y
            pinky_pip = lm[18].y

            # states
            index_up = index_tip < index_pip
            middle_up = middle_tip < middle_pip
            ring_up = ring_tip < ring_pip
            pinky_up = pinky_tip < pinky_pip

            thumb_up = thumb_tip > thumb_ip

            # gestures
            thumbs_up = (thumb_up and not index_up and not middle_up and not ring_up and not pinky_up)

            open_palm = (thumb_up and index_up and middle_up and ring_up and pinky_up)

            two_fingers = (not thumb_up and index_up and middle_up and not ring_up and not pinky_up)

            if thumbs_up:
                gesture = "thumbs_up"
            elif open_palm:
                gesture = "open_palm"
            elif two_fingers:
                gesture = "two_fingers"

    # --------- SMOOTHING ---------
    history.append(gesture)

    if len(history) > history_size:
        history.pop(0)

    current = max(set(history), key=history.count)

    # --------- ACTIONS ---------
    if current == "thumbs_up" and not played:
        threading.Thread(target=play_sound).start()
        played = True

    elif current == "open_palm":
        played = False

    elif current == "two_fingers":
        print("Play video here")

    # --------- DISPLAY ---------
    cv2.imshow("Gesture Control", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()