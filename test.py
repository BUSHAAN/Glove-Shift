import cv2


i = 100
wCam,hCam = 320,240
cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)

while True:
    success, img = cap.read()
    winname="winname"
    cv2.namedWindow(winname)        # Create a named window
    cv2.moveWindow(winname, 1200,10)  # Move it to (40,30)
    cv2.imshow(winname, img)
    cv2.waitKey(1)
