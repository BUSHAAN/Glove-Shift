import cv2
import time
import HandTrackingModule as htm
import KeyboardInput as ki


wCam,hCam = 320,240

cap = cv2.VideoCapture(0)
cap.set(3,wCam)
cap.set(4,hCam)


detector = htm.handDetector(detectionCon=0.9)

def sendinput(keys,img):
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
        
def steering(fps):
    success, img = cap.read()
    img = cv2.flip(img,1)
    img = detector.findHands(img)
    lmList = detector.findPosition(img)
    img = cv2.flip(img,1)
    cv2.putText(img,'FPS:'+ str(int(fps)), (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1,
                (0, 0, 255), 2)
    if len(lmList)!=0:
        THUMBTIPx1,THUMBTIPy1   = lmList[4][1], lmList[4][2]
        INDEXBASEx1,INDEXBASEy1 = lmList[5][1], lmList[5][2]
        MIDBASEx1,MIDBASEy1     = lmList[9][1], lmList[9][2]
        MIDTIPx1,MIDTIPy1       = lmList[12][1], lmList[12][2]
        RINGBASEx1,RINGBASEy1   = lmList[13][1], lmList[13][2]
        RINGTIPx1,RINGTIPy1     = lmList[16][1], lmList[16][2]
        PINKYBASEx1,PINKYBASEy1 = lmList[17][1], lmList[17][2]
        

        if(INDEXBASEx1<PINKYBASEx1): #to check if its a right hand
            if (INDEXBASEx1<THUMBTIPx1 & MIDBASEy1<MIDTIPy1):
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('brake left')
                    sendinput(['s','a'],img)
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('brake right')
                    sendinput(['s','d'],img)
                else:
                    print("brake")
                    sendinput(['s'],img)
            elif (INDEXBASEx1<THUMBTIPx1):
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('brake left')
                    sendinput(['s','a'],img)
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('brake right')
                    sendinput(['s','d'],img)
                else:
                    print("brake")
                    sendinput(['s'],img)
            elif(MIDBASEy1<MIDTIPy1):
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('accelerate left')
                    sendinput(['w','a'],img)
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('accelerate right')
                    sendinput(['w','d'],img)
                else:
                    print('accelerate')
                    sendinput(['w'],img)
            else:
                if(INDEXBASEy1-PINKYBASEy1>20):
                    print('neutral left')
                    sendinput(['a'],img)
                elif(INDEXBASEy1-PINKYBASEy1<-25):
                    print('neutral right')
                    sendinput(['d'],img)
                else:
                    print("neutral")
                    sendinput([],img)
        else:
            print('use right hand')
            sendinput([],img)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
        

def cleanup():
    cap.release()
    cv2.destroyAllWindows()
