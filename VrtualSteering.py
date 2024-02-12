import cv2
import time
import HandTrackingModule as htm
import keyboard
import KeyboardInput as ki
import ctypes



wCam,hCam = 320,240

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)


detector = htm.handDetector(detectionCon=0.9)
def sendinput(keys):
    charlist = ['w','s','a','d']
    for i in charlist:
        if i in keys:
            ki.press_key(i)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
        else:
            ki.release_key(i)
            cv2.imshow("Image", img)
            cv2.waitKey(1)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
        

while True:
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)

    if len(lmList)!=0:
        
        THUMBTIPx1,THUMBTIPy1   = lmList[4][1], lmList[4][2]
        INDEXBASEx1,INDEXBASEy1 = lmList[5][1], lmList[5][2]
        MIDBASEx1,MIDBASEy1     = lmList[9][1], lmList[9][2]
        MIDTIPx1,MIDTIPy1       = lmList[12][1], lmList[12][2]
        RINGBASEx1,RINGBASEy1   = lmList[13][1], lmList[13][2]
        RINGTIPx1,RINGTIPy1     = lmList[16][1], lmList[16][2]
        PINKYBASEx1,PINKYBASEy1 = lmList[17][1], lmList[17][2]
        

        if(INDEXBASEx1<PINKYBASEx1):
            if (INDEXBASEx1<THUMBTIPx1 & MIDBASEy1<MIDTIPy1):
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('brake left')
                    sendinput(['s','a'])
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('brake right')
                    sendinput(['s','d'])
                else:
                    print("brake")
                    sendinput(['s'])
            elif (INDEXBASEx1<THUMBTIPx1):
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('brake left')
                    sendinput(['s','a'])
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('brake right')
                    sendinput(['s','d'])
                else:
                    print("brake")
                    sendinput(['s'])
            elif(MIDBASEy1<MIDTIPy1):
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('accelerate left')
                    sendinput(['w','a'])
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('accelerate right')
                    sendinput(['w','d'])
                else:
                    sendinput(['w'])
            else:
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('neutral left')
                    sendinput(['a'])
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('neutral right')
                    sendinput(['d'])
                else:
                    print("neutral")
                    sendinput([])
        else:
            print('use right hand')
            sendinput([])
    cv2.imshow("Image", img)
    cv2.waitKey(1)

