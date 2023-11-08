import cv2 as cv
import time

video = cv.VideoCapture('testt.mp4')

while True:
    ret, frame = video.read()
    if not ret:
        break

    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (21, 21), 0)

    ret, thresh = cv.threshold(gray, 165,255, cv.THRESH_BINARY_INV)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    if (len(contours) > 0):
        c = max(contours, key = cv.contourArea)
        x, y, w, h = cv.boundingRect(c)
        cv.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    cv.imshow('frame', frame)
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

    time.sleep(0.1)

video.release()
cv.destroyAllWindows()