# Path: main.py
#gym workout motion tracker

import cv2
import mediapipe as mp
import time

cap = cv2.VideoCapture(0)

mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils

pTime = 0

# check if the person is doin a squat correctly
def squat_check(lankle, rankle, lknee, rknee, lhip, rhip):
    # check if the knees are below the ankles
    if lknee[1] > lankle[1] and rknee[1] > rankle[1]:
        # check if the hips are below the knees
        if lhip[1] > lknee[1] and rhip[1] > rknee[1]:
            return True
    return False


while True:

    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(imgRGB)
    # print(results.pose_landmarks)
    if results.pose_landmarks:
        mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
        # for id, lm in enumerate(results.pose_landmarks.landmark):
        #     # print(id, lm)
        #     h, w, c = img.shape
        #     cx, cy = int(lm.x * w), int(lm.y * h)
        #     print(id, cx, cy)
        #     cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

        # get the coordinates of the landmarks
        lankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y]
        rankle = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y]
        lknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y]
        rknee = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y]
        lhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y]
        rhip = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y]

        # check if the person is doin a squat correctly
        if squat_check(lankle, rankle, lknee, rknee, lhip, rhip):
            print("Squatting correctly")
        else:
            print("Squatting incorrectly")

        # check if



# check if the person is doin a push-up correctly 
def pushup_check(lankle, rankle, lknee, rknee, lhip, rhip):
    # check if the knees are below the ankles
    if lknee[1] > lankle[1] and rknee[1] > rankle[1]:
        # check if the hips are above the knees
        if lhip[1] < lknee[1] and rhip[1] < rknee[1]:
            return True
    return False





    





