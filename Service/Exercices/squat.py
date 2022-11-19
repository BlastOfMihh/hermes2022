from enum import Enum
import time 

count=0
stack=[]

def check1(parts): # check if elbows are above shoulders
    lankle     = parts[0]
    rankle     = parts[1]
    lknee      = parts[2]
    rknee      = parts[3]
    lhip       = parts[4]
    rhip       = parts[5]
    lwrist     = parts[6]
    rwrist     = parts[7]
    lshoulder  = parts[8]
    rshoulder  = parts[9]
    lelbow     = parts[10]
    relbow     = parts[11]
    if lelbow[1]<lshoulder[1] and relbow[1]<rshoulder[1]:
        return True
    return False 


def check2(parts): # check if knees are below hips
    lankle     = parts[0]
    rankle     = parts[1]
    lknee      = parts[2]
    rknee      = parts[3]
    lhip       = parts[4]
    rhip       = parts[5]
    lwrist     = parts[6]
    rwrist     = parts[7]
    lshoulder  = parts[8]
    rshoulder  = parts[9]
    lelbow     = parts[10]
    relbow     = parts[11]
    if lhip[1]>lknee[1] and rhip[1]>rknee[1]:
        return True
    return False 


def handle(parts):
    if check2(parts):
        if len(stack)==0: 
            
        stack.append(2)
    else:
        stack.clear()
