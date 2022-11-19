# Path: main.py
#gym workout motion tracker

import cv2
import mediapipe as mp
import time
import Exercices.squat as squat


def show_video(img):
    cv2.imshow("Image", img)
    cv2.waitKey(1)


def video_capture():
    cap = cv2.VideoCapture(0)

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    while True:
        cTime = time.time()
        success, img = cap.read()
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        if results.pose_landmarks:
            mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
            lankle    = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ANKLE].z]
            rankle    = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ANKLE].z]
            lknee     = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_KNEE].z]
            rknee     = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_KNEE].z]
            lhip      = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_HIP].z]
            rhip      = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_HIP].z]
            lwrist    = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_WRIST].z]
            rwrist    = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_WRIST].z]
            lshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_SHOULDER].z]
            rshoulder = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_SHOULDER].z]
            lelbow    = [results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.LEFT_ELBOW].z]
            relbow    = [results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].x, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].y, results.pose_landmarks.landmark[mpPose.PoseLandmark.RIGHT_ELBOW].z]
            parts = [lankle, rankle, lknee, rknee, lhip, rhip, lwrist, rwrist, lshoulder, rshoulder, lelbow, relbow]
            squat.handle(parts)
            show_video(img)



video_capture()