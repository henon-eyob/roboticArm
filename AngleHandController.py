import math
from cvzone.HandTrackingModule import HandDetector
import cv2
import time
import numpy as np
import HandTrackingModule as htm
import pyfirmata
import PoseModule as pm
from pyfirmata import Arduino, SERVO
wCam, hCam = 1000, 700
cap = cv2.VideoCapture(0)
cap.set(3, wCam)
cap.set(4, hCam)
pTime = 0

port = "COM8"
board = pyfirmata.Arduino(port)
it = pyfirmata.util.Iterator(board)
it.start()
servoPinHand = board.get_pin('d:5:s')  # pin 5 Arduino
servoPinBottom = board.get_pin('d:4:s')  # pin 4 Arduino
servoPinJointUp = board.get_pin('d:3:s')  # pin 3 Arduino
servoPinJointBottom = board.get_pin('d:2:s')  # pin 2 Arduino

detector = htm.handDetector(detectionCon=0.7, maxHands=1)
ano = HandDetector(detectionCon=0.8, maxHands=1)
minHand, maxHand = 20, 250
minBar, maxBar = 400, 150
minAngle, maxAngle = 180, 0
minAngle2, maxAngle2 = 0, 180
pmDetector = pm.PoseDetector()
while True:
    success, img = cap.read()
    img = detector.handsFinder(img)
    lmList = detector.positionFinder(img, draw=False)
    if len(lmList) != 0:
        #print(lmList[4], lmList[8])
        x1, y1 = lmList[4][1], lmList[4][2]
        x2, y2 = lmList[8][1], lmList[8][2]
        cx, cy = (x1 + x2)//2, (y1 + y2)//2
        cv2.circle(img, (x1, y1), 15, (255, 0, 255), cv2.FILLED)
        cv2.circle(img, (x2, y2), 15, (255, 0, 255), cv2.FILLED)
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 255), 3)
        cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

        length = math.hypot(x2-x1, y2-y1)
        servoValHand = np.interp(length, [minHand, maxHand], [180, 70])
        servoPinHand.write(servoValHand)

        bar = np.interp(length, [minHand, maxHand], [minBar, maxBar])
        cTime = time.time()
        fps = 1/(cTime - pTime)
        pTime = cTime
        cv2.rectangle(img, (1180, 150), (1215, 400), (255, 0, 0), 3)
        cv2.rectangle(img, (1180, int(bar)), (1215, 400), (0, 255, 0), cv2.FILLED)

    img = pmDetector.findPose(img, False)
    lmListPm = pmDetector.findPosition(img, draw=False)
    if len(lmListPm) != 0:
        angleBottom = pmDetector.findAngle(img, 11, 12, 14)
        servoValBottom = np.interp(angleBottom, [minHand, maxHand], [minAngle, maxAngle])
        servoPinBottom.write(servoValBottom)
        print(servoValBottom)

        angleJointUp = pmDetector.findAngle(img, 12, 14, 16)
        servoValJointUp = np.interp(angleJointUp, [minHand, maxHand], [30, 150])
        servoPinJointUp.write(servoValJointUp)

        angleJointBottom = pmDetector.findAngle(img, 14, 16, 22)
        servoValJointBottom = np.interp(angleJointBottom, [minHand, maxHand], [160, 180])
        servoPinJointBottom.write(servoValJointBottom)

    cv2.imshow("img", img)
    cv2.waitKey(1)
