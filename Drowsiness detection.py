import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2

import time

import winsound

import mediapipe as mp

import numpy as np

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

if not cap.isOpened():

print("Camera not opening ❌")

exit()

LEFT_EYE = [33, 160, 158, 133, 153, 144]

RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):

A = np.linalg.norm(eye[1] - eye[5])

B = np.linalg.norm(eye[2] - eye[4])

C = np.linalg.norm(eye[0] - eye[3])

return (A + B) / (2.0 * C)

eye_closed_start = None

ALERT_TIME = 5

alarm_on = False

🔥 smoothing buffer

ear_history = []

while True:

ret, frame = cap.read()

if not ret:

    continue



frame = cv2.resize(frame, (480, 360))

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



results = face_mesh.process(rgb)



status = "Detecting..."

color = (255, 255, 255)

confidence = 0



if results.multi_face_landmarks:

    for face_landmarks in results.multi_face_landmarks:



        h, w, _ = frame.shape



        left_eye = []

        right_eye = []



        for idx in LEFT_EYE:

            left_eye.append([

                int(face_landmarks.landmark[idx].x * w),

                int(face_landmarks.landmark[idx].y * h)

            ])



        for idx in RIGHT_EYE:

            right_eye.append([

                int(face_landmarks.landmark[idx].x * w),

                int(face_landmarks.landmark[idx].y * h)

            ])



        left_eye = np.array(left_eye)

        right_eye = np.array(right_eye)



        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2



        # 🔥 smoothing EAR

        ear_history.append(ear)

        if len(ear_history) > 10:

            ear_history.pop(0)



        smooth_ear = sum(ear_history) / len(ear_history)



        # 🎯 Threshold

        if smooth_ear > 0.25:

            status = "Eyes Open"

            color = (0, 255, 0)

            confidence = min(int((smooth_ear - 0.25) * 400), 100)



            eye_closed_start = None

            alarm_on = False

        else:

            status = "Eyes Closed"

            color = (0, 0, 255)

            confidence = max(0, int((0.25 - smooth_ear) * 400))



            if eye_closed_start is None:

                eye_closed_start = time.time()



# Time tracking

if eye_closed_start is not None:

    elapsed = time.time() - eye_closed_start

else:

    elapsed = 0



# Display

cv2.putText(frame, status, (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)



cv2.putText(frame, f"Confidence: {confidence}%", (20, 80),

            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)



# 🔴 ALERT (continuous beep)

if elapsed >= ALERT_TIME:

    cv2.putText(frame, "DROWSINESS ALERT!", (20, 130),

                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)



    if not alarm_on:

        for _ in range(3):  # 🔊 louder alert

            winsound.Beep(2500, 300)

        alarm_on = True

else:

    alarm_on = False



cv2.imshow("Drowsiness Detection (Final)", frame)



if cv2.waitKey(1) & 0xFF == ord('q'):

    break

cap.release()

cv2.destroyAllWindows()
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import cv2

import time

import winsound

import mediapipe as mp

import numpy as np

mp_face_mesh = mp.solutions.face_mesh

face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

cap = cv2.VideoCapture(0)

if not cap.isOpened():

print("Camera not opening ❌")

exit()

LEFT_EYE = [33, 160, 158, 133, 153, 144]

RIGHT_EYE = [362, 385, 387, 263, 373, 380]

def eye_aspect_ratio(eye):

A = np.linalg.norm(eye[1] - eye[5])

B = np.linalg.norm(eye[2] - eye[4])

C = np.linalg.norm(eye[0] - eye[3])

return (A + B) / (2.0 * C)

eye_closed_start = None

ALERT_TIME = 5

alarm_on = False

🔥 smoothing buffer

ear_history = []

while True:

ret, frame = cap.read()

if not ret:

    continue



frame = cv2.resize(frame, (480, 360))

rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)



results = face_mesh.process(rgb)



status = "Detecting..."

color = (255, 255, 255)

confidence = 0



if results.multi_face_landmarks:

    for face_landmarks in results.multi_face_landmarks:



        h, w, _ = frame.shape



        left_eye = []

        right_eye = []



        for idx in LEFT_EYE:

            left_eye.append([

                int(face_landmarks.landmark[idx].x * w),

                int(face_landmarks.landmark[idx].y * h)

            ])



        for idx in RIGHT_EYE:

            right_eye.append([

                int(face_landmarks.landmark[idx].x * w),

                int(face_landmarks.landmark[idx].y * h)

            ])



        left_eye = np.array(left_eye)

        right_eye = np.array(right_eye)



        ear = (eye_aspect_ratio(left_eye) + eye_aspect_ratio(right_eye)) / 2



        # 🔥 smoothing EAR

        ear_history.append(ear)

        if len(ear_history) > 10:

            ear_history.pop(0)



        smooth_ear = sum(ear_history) / len(ear_history)



        # 🎯 Threshold

        if smooth_ear > 0.25:

            status = "Eyes Open"

            color = (0, 255, 0)

            confidence = min(int((smooth_ear - 0.25) * 400), 100)



            eye_closed_start = None

            alarm_on = False

        else:

            status = "Eyes Closed"

            color = (0, 0, 255)

            confidence = max(0, int((0.25 - smooth_ear) * 400))



            if eye_closed_start is None:

                eye_closed_start = time.time()



# Time tracking

if eye_closed_start is not None:

    elapsed = time.time() - eye_closed_start

else:

    elapsed = 0



# Display

cv2.putText(frame, status, (20, 40),

            cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)



cv2.putText(frame, f"Confidence: {confidence}%", (20, 80),

            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 0), 2)

# 🔴 ALERT (continuous beep)

if elapsed >= ALERT_TIME:

    cv2.putText(frame, "DROWSINESS ALERT!", (20, 130),

                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)



    if not alarm_on:

        for _ in range(3):  # 🔊 louder alert

            winsound.Beep(2500, 300)

        alarm_on = True

else:

    alarm_on = False



cv2.imshow("Drowsiness Detection (Final)", frame)



if cv2.waitKey(1) & 0xFF == ord('q'):

    break

cap.release()

cv2.destroyAllWindows
  


