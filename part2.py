import cv2 as cv
from math import sqrt
import time

video = cv.VideoCapture('testt.mp4')

leftCounter = 0
rightCounter = 0

summCx = 0
summCy = 0

while True:
    ret, frame = video.read()
    if not ret:
        break

    height = frame.shape[0]
    width = frame.shape[1]

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv.threshold(gray, 165, 255, cv.THRESH_BINARY_INV)

    contours, hierarchy = cv.findContours(thresh, 
                                            cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    if (len(contours) > 0):
        c = max(contours, key = cv.contourArea)
        x, y, w, h = cv.boundingRect(c)

        cx = int(x + w/2)
        cy = int(y + h/2)
        summCx += cx
        summCy += cy
        print("Center: x=" + str(cx) + ", y=" + str(cy))
        cv.putText(frame, "Center: x=" + str(cx) + ", y=" + str(cy),
                    (5, 15), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

        cv.putText(frame, "Distance to image center: " + 
                    str("%.2f" % sqrt((width / 2 - cx) * (width / 2 - cx) + 
 (height / 2 - cy) * (height / 2 - cy))), 
 (5, 30), cv.FONT_HERSHEY_PLAIN,
                                    1, (0, 0, 0))

        centered = False
        if (abs(width / 2 - cx) < 100) and (abs(height / 2 - cy) < 100):
            centered = True

        left = False
        if (cx < width / 2):
            left = True
            leftCounter += 1
        else:
            rightCounter += 1

        cv.putText(frame, "Left: " + str(leftCounter), 
 (5, 45), cv.FONT_HERSHEY_PLAIN, 1, 
 (0, 0, 255) if left else (0, 0, 0))

        cv.putText(frame, "Right: " + str(rightCounter),
 (5, 60), cv.FONT_HERSHEY_PLAIN, 1, 
 (255, 0, 0) if not left else (0, 0, 0))

        cv.circle(frame, (cx, cy), int(sqrt(w * w / 4 + h * h / 4)), 
 (0, 255, 0) if centered else (0, 0, 255), 2)

        cv.line(frame, (cx, 0), (cx, height), (255, 0, 0), 1)
        cv.line(frame, (0, cy), (width, cy), (255, 0, 0), 1)

        cv.putText(frame, "Sobj/Simg: " + 
                    str("%.2f" % (w * h / width / height * 100)) + "%", 
 (5, 90), cv.FONT_HERSHEY_PLAIN, 1, (0, 0, 0))

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)

print("Avg center: x=" + str("%.2f" % (summCx / (leftCounter + rightCounter + 1))) +
        ", y=" + str("%.2f" % (summCy / (leftCounter + rightCounter + 1))))

video.release()
cv.destroyAllWindows()