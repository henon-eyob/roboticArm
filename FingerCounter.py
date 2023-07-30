import asyncio

import cv2
from cvzone.HandTrackingModule import HandDetector
import time
import websockets

detector = HandDetector(maxHands=1, detectionCon=0.8)
video = cv2.VideoCapture(0)


async def main():
    url = "ws://192.168.0.3:80/CarInput"
    async with websockets.connect(url) as ws:
        print("connected")
        while True:
            _, img = video.read()
            img = cv2.flip(img, 1)
            hand = detector.findHands(img, draw=False)
            if hand:
                lmlist = hand[0]
                if lmlist:
                    fingerup = detector.fingersUp(lmlist)
                    if fingerup == [0, 0, 0, 0, 0]:
                        print("0")
                        await ws.send("s")
                        cv2.putText(img, f'Stop: {int(0)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [0, 1, 0, 0, 0]:
                        print("1")
                        cv2.putText(img, f'Incorrect command {int(3)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [0, 1, 1, 0, 0]:
                        print("2")
                        await ws.send("l")
                        cv2.putText(img, f'Turn Left: {int(2)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [0, 1, 1, 1, 0]:
                        print("3")
                        cv2.putText(img, f'Incorrect command {int(3)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [0, 1, 1, 1, 1]:
                        print("4")
                        await ws.send("r")
                        cv2.putText(img, f'Turn Right: {int(4)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [1, 1, 1, 1, 1]:
                        print("5")
                        await ws.send("b")
                        cv2.putText(img, f'Turn Backward: {int(5)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [1, 0, 0, 0, 0]:
                        print("6")
                        cv2.putText(img, f'Incorrect command {int(6)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [1, 1, 0, 0, 0]:
                        print("7")
                        cv2.putText(img, f'Incorrect command: {int(7)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [1, 1, 1, 0, 0]:
                        print("8")
                        cv2.putText(img, f'Incorrect command: {int(8)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)
                    if fingerup == [1, 1, 1, 1, 0]:
                        print("9")
                        cv2.putText(img, f'Incorrect command: {int(9)}', (200, 70), cv2.FONT_HERSHEY_PLAIN,
                                    3, (255, 255, 0), 3)

            cv2.imshow("Video", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(0)

    video.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    asyncio.run(main())
