import cv2
import time
import mediapipe as mp
import paho.mqtt.publish as publish

MQTT_SERVER = "192.168.1.4"
MQTT_PATH = "hand"

pTime = 0
start_time = time.time()

mp_draw = mp.solutions.drawing_utils
mp_hand = mp.solutions.hands

tipIds = [4, 8, 12, 16, 20]

cap = cv2.VideoCapture(0)

with mp_hand.Hands(min_detection_confidence=0.5,
                   min_tracking_confidence=0.5) as hands:
    while True:
        ret, image = cap.read()
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image_rgb)

        lmList = []
        fingers = []

        if results.multi_hand_landmarks:
            myHands = results.multi_hand_landmarks[0]

            for id, lm in enumerate(myHands.landmark):
                h, w, _ = image.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([id, cx, cy])

            mp_draw.draw_landmarks(image, myHands, mp_hand.HAND_CONNECTIONS)

            if lmList:
                fingers.append(1 if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1] else 0)

                for id in range(1, 5):
                    fingers.append(1 if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2] else 0)

                finger_counter = fingers.count(1)

                publish.single(MQTT_PATH, finger_counter, hostname=MQTT_SERVER)

                if finger_counter in [0, 1, 2, 4, 5]:
                    directions = {0: 'Stop', 1: 'Left', 2: 'Right', 4: 'Backward', 5: 'Forward'}
                    direction_text = f"{finger_counter} - {directions.get(finger_counter, '')}"
                    cv2.putText(image, direction_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2,
                                cv2.LINE_4)

        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        print(f"FPS: {fps:.2f}")
        cv2.putText(image,f"FPS: {int(fps)}", (450, 70),cv2.FONT_HERSHEY_PLAIN,3,(255,0,0),3)

       # end_time = time.time()
       # execution_time = end_time - start_time
       # print(f"Thời gian chạy của chương trình: {execution_time} giây")

        cv2.imshow("HANDS", image)
        k = cv2.waitKey(1)
        if k == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()