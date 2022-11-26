import time

import camera
import numpy as np
# create a flask app with a button that prints "Hello World" when clicked

from flask import Flask, render_template, request, redirect, Response
import cv2
import mediapipe as mp



app = Flask(__name__, template_folder='templates')


def check_squat1(parts):
    lankle = parts[0]
    rankle = parts[1]
    lknee = parts[2]
    rknee = parts[3]
    lhip = parts[4]
    rhip = parts[5]
    lwrist = parts[6]
    rwrist = parts[7]
    lshoulder = parts[8]
    rshoulder = parts[9]
    lelbow = parts[10]
    relbow = parts[11]
    if lelbow[1] < lshoulder[1] and relbow[1] < rshoulder[1]:
        return True
    return False


def show_video(img):
    cv2.imshow("Image", img)
    cv2.waitKey(1)


cap = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0


def check2(parts):  # check if knees are below hips
    lankle = parts[0]
    rankle = parts[1]
    lknee = parts[2]
    rknee = parts[3]
    lhip = parts[4]
    rhip = parts[5]
    lwrist = parts[6]
    rwrist = parts[7]
    lshoulder = parts[8]
    rshoulder = parts[9]
    lelbow = parts[10]
    relbow = parts[11]
    if lhip[1] > lknee[1] and rhip[1] > rknee[1]:
        return True
    return False


def lengthforearm(parts):
    lankle = parts[0]
    rankle = parts[1]
    lknee = parts[2]
    rknee = parts[3]
    lhip = parts[4]
    rhip = parts[5]
    lwrist = parts[6]
    rwrist = parts[7]
    lshoulder = parts[8]
    rshoulder = parts[9]
    lelbow = parts[10]
    relbow = parts[11]
    angle = calculate_angle(lshoulder, lelbow, lwrist)
    stage = None
    counter = 0
    if angle < 170:
        stage = 1
    if angle < 30:
        stage = 1
        counter += 1
    if stage == 1:
        return True
    return False


def checkPullup(parts):  # check if knees are below hips
    lankle = parts[0]
    rankle = parts[1]
    lknee = parts[2]
    rknee = parts[3]
    lhip = parts[4]
    rhip = parts[5]
    lwrist = parts[6]
    rwrist = parts[7]
    lshoulder = parts[8]
    rshoulder = parts[9]
    lelbow = parts[10]
    relbow = parts[11]
    lear = parts[13]
    rear = parts[12]
    # if lelbow[1] >= lshoulder[1] and relbow[1] >= rshoulder[1]:
    if lengthforearm(parts):
        return False
    return True


def checkPullup2(parts):  # aka squats 2
    lankle = parts[0]
    rankle = parts[1]
    lknee = parts[2]
    rknee = parts[3]
    lhip = parts[4]
    rhip = parts[5]
    lwrist = parts[6]
    rwrist = parts[7]
    lshoulder = parts[8]
    rshoulder = parts[9]
    lelbow = parts[10]
    relbow = parts[11]
    lear = parts[13]
    rear = parts[12]
    if lelbow[1] >= lshoulder[1] and relbow[1] >= rshoulder[1]:
        return False
    return True


def checkPushUps(parts):  # check if knees are below hips
    lankle = parts[0]
    rankle = parts[1]
    lknee = parts[2]
    rknee = parts[3]
    lhip = parts[4]
    rhip = parts[5]
    lwrist = parts[6]
    rwrist = parts[7]
    lshoulder = parts[8]
    rshoulder = parts[9]
    lelbow = parts[10]
    relbow = parts[11]
    lear = parts[13]
    rear = parts[12]
    # if lelbow[1] >= lshoulder[1] and relbow[1] >= rshoulder[1]:
    if lengthforearm(parts):
        return False
    return True


def calculate_angle(a, b, c):
    a = np.array(a)  # First
    b = np.array(b)  # Mid
    c = np.array(c)  # End

    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)

    if angle > 180.0:
        angle = 360 - angle

    return angle


stage = None


def gen_frames():
    counter = 0
    reset = 0
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            ret, buffer = cv2.imencode('.jpg', frame)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                lankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y]
                rankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].z]
                lknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].z]
                rknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].z]
                lhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z]
                rhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z]
                lwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].z]
                rwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].z]
                lshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].z]
                rshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].z]
                lelbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].z]
                relbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].z]
                lear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].y]
                rear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].y]
                parts = [lankle, rankle, lknee, rknee, lhip, rhip, lwrist, rwrist, lshoulder, rshoulder, lelbow, relbow,
                         rear, lear]

                angle = calculate_angle(lshoulder, lelbow, lwrist)
                # if angle > 160:
                #     stage = "down"
                # if angle < 30 and stage == 'down':
                #     stage = "up"
                #     counter += 1
                #     print(counter)

                cTime = time.time()
                if check_squat1(parts):
                    reset += 1

                if reset > 20:
                    counter += 1
                    reset = 0
                    print(counter)

                show_video(frame)
            # trebuie sa fie pana deasupra capului lESGOOOO
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_framesSquats():
    counter = 0
    reset = 0
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            ret, buffer = cv2.imencode('.jpg', frame)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                lankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y]
                rankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].z]
                lknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].z]
                rknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].z]
                lhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z]
                rhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z]
                lwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].z]
                rwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].z]
                lshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].z]
                rshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].z]
                lelbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].z]
                relbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].z]
                lear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].y]
                rear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].y]
                parts = [lankle, rankle, lknee, rknee, lhip, rhip, lwrist, rwrist, lshoulder, rshoulder, lelbow, relbow,
                         rear, lear]

                angle = calculate_angle(lshoulder, lelbow, lwrist)
                # if angle > 160:
                #     stage = "down"
                # if angle < 30 and stage == 'down':
                #     stage = "up"
                #     counter += 1
                #     print(counter)

                cTime = time.time()
                window_name = 'Image'
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (50, 50)
                # fontScale
                fontScale = 1
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2

                # Using cv2.putText() method
                image = cv2.putText(frame, str(counter), org, font, fontScale, color, thickness, cv2.LINE_AA)

                if checkPullup2(parts):
                    reset += 1

                if reset > 20:
                    counter += 1
                    reset = 0
                    print(counter)

                show_video(frame)
            # trebuie sa fie pana deasupra capului lESGOOOO
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_framesPushUps():
    counter = 0
    reset = 0
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            ret, buffer = cv2.imencode('.jpg', frame)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                lankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y]
                rankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].z]
                lknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].z]
                rknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].z]
                lhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z]
                rhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z]
                lwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].z]
                rwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].z]
                lshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].z]
                rshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].z]
                lelbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].z]
                relbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].z]
                lear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].y]
                rear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].y]
                parts = [lankle, rankle, lknee, rknee, lhip, rhip, lwrist, rwrist, lshoulder, rshoulder, lelbow, relbow,
                         rear, lear]

                angle = calculate_angle(lshoulder, lelbow, lwrist)
                # if angle > 160:
                #     stage = "down"
                # if angle < 30 and stage == 'down':
                #     stage = "up"
                #     counter += 1
                #     print(counter)

                cTime = time.time()
                if checkPullup(parts):
                    reset += 1

                if reset > 15:
                    counter += 1
                    reset = 0
                    print(counter)
                window_name = 'Image'
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (50, 50)
                # fontScale
                fontScale = 1
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2

                # Using cv2.putText() method
                image = cv2.putText(frame, str(counter), org, font, fontScale, color, thickness, cv2.LINE_AA)
                show_video(frame)
            # trebuie sa fie pana deasupra capului lESGOOOO
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_framesBIceps():
    counter = 0
    reset = 0
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            ret, buffer = cv2.imencode('.jpg', frame)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                lankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y]
                rankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].z]
                lknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].z]
                rknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].z]
                lhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z]
                rhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z]
                lwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].z]
                rwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].z]
                lshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].z]
                rshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].z]
                lelbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].z]
                relbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].z]
                lear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].y]
                rear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].y]
                parts = [lankle, rankle, lknee, rknee, lhip, rhip, lwrist, rwrist, lshoulder, rshoulder, lelbow, relbow,
                         rear, lear]
                landmarks = results.pose_landmarks.landmark

                shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                            landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
                elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
                wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                         landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]

                angle = calculate_angle(shoulder, elbow, wrist)
                cv2.putText(image, str(angle),
                            tuple(np.multiply(elbow, [640, 480]).astype(int)),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA
                            )

                if angle > 160:
                    stage = "down"
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                    print(counter)
                cTime = time.time()
                if checkPullup(parts):
                    reset += 1

                if reset > 15:
                    counter += 1
                    reset = 0
                    print(counter)
                window_name = 'Image'
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (50, 50)
                # fontScale
                fontScale = 1
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2
                # Render curl counter
                # Setup status box
                cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)

                # Rep data
                cv2.putText(image, 'REPS', (15, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, str(counter),
                            (10, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                # Stage data
                cv2.putText(image, 'STAGE', (65, 12),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
                cv2.putText(image, stage,
                            (60, 60),
                            cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)

                # Render detections
                mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                          mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2),
                                          mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2)
                                          )

                cv2.imshow('Mediapipe Feed', image)

                # Using cv2.putText() method
                image = cv2.putText(frame, str(counter), org, font, fontScale, color, thickness, cv2.LINE_AA)
                show_video(frame)
            # trebuie sa fie pana deasupra capului lESGOOOO
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


def gen_framesBIceps2():
    counter = 0
    reset = 0
    stage = None
    while True:
        success, frame = cap.read()  # read the camera frame
        if not success:
            break
        else:
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            ret, buffer = cv2.imencode('.jpg', frame)
            imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)
            if results.pose_landmarks:
                mpDraw.draw_landmarks(frame, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
                lankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y]
                rankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].z]
                lknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].z]
                rknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y,
                         results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].z]
                lhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z]
                rhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z]
                lwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].z]
                rwrist = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].z]
                lshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].z]
                rshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y,
                             results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].z]
                lelbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].z]
                relbow = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y,
                          results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].z]
                lear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_EAR].y]
                rear = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].x,
                        results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_EAR].y]
                parts = [lankle, rankle, lknee, rknee, lhip, rhip, lwrist, rwrist, lshoulder, rshoulder, lelbow, relbow,
                         rear, lear]

                angle = calculate_angle(lshoulder, lelbow, lwrist)
                if angle > 160:
                    stage = "down"
                if angle < 30 and stage == 'down':
                    stage = "up"
                    counter += 1
                    reset += 1
                    print(counter)

                cTime = time.time()

                if reset > 15:
                    counter += 1
                    reset = 0
                    print(counter)
                window_name = 'Image'
                # font
                font = cv2.FONT_HERSHEY_SIMPLEX
                # org
                org = (50, 50)
                # fontScale
                fontScale = 1
                # Blue color in BGR
                color = (255, 0, 0)
                # Line thickness of 2 px
                thickness = 2

                # Using cv2.putText() method
                image = cv2.putText(frame, str(counter), org, font, fontScale, color, thickness, cv2.LINE_AA)
                show_video(frame)
            # trebuie sa fie pana deasupra capului lESGOOOO
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result


@app.route('/ShoulderPushups')
def video_feed():
    return Response(gen_framesPushUps(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def loginPage():
    return render_template('LoginPage.html')


@app.route('/Nutrition')
def nutrition():
    return render_template('NutritionPlan2.html')


@app.route('/WorkoutPlan')
def workkkk():
    return render_template('Questions.html')


@app.route('/Squat')
def squat():
    return Response(gen_framesSquats(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/Biceps')
def biceps():
    return Response(gen_framesBIceps2(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)
