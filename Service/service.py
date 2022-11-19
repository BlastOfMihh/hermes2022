# Path: main.py
#gym workout motion tracker

import cv2
import mediapipe as mp
import time
from enum import Enum

import argparse

# exercise enum
class exercise_type(Enum):
    SQUAT = 0
    PUSHUP = 1

    # check if the person is doin a squat correctly
def squat_check(lankle, rankle, lknee, rknee, lhip, rhip):
    # check if the knees are below the ankles
    if lknee[1] > lankle[1] and rknee[1] > rankle[1]:
        # check if the hips are below the knees
        if lhip[1] > lknee[1] and rhip[1] > rknee[1]:
            return True
    return False

    # check if the person is doin a push-up correctly 
def pushup_check(lankle, rankle, lknee, rknee, lhip, rhip):
    # check if the knees are below the ankles
    if lknee[1] > lankle[1] and rknee[1] > rankle[1]:
        # check if the hips are above the knees
        if lhip[1] < lknee[1] and rhip[1] < rknee[1]:
            return True
    # (x,y,z) = lankle
    # print(x,y,z)
    return False

def show_video(img):
    cv2.imshow("Image", img)
    cv2.waitKey(1)

def check_squat1(parts):
    lankle = parts[0]
    rankle = parts[1]
    lknee = parts[2]
    rknee = parts[3]
    lhip = parts[4]
    rhip = parts[5]
    lwrist= parts[6]
    rwrist= parts[7]
    lshoulder = parts[8]
    rshoulder = parts[9]
    lelbow = parts[10]
    relbow = parts[11]
    if lelbow[1]<lshoulder[1] and relbow[1]<rshoulder[1]:
        return True
    return False 



def video_capture():
    cap = cv2.VideoCapture(0)

    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    mpDraw = mp.solutions.drawing_utils

    pTime = 0
    while True:
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
            cTime = time.time()
            if check_squat1(parts):
                print(cTime,"Squat")
            show_video(img)



video_capture()