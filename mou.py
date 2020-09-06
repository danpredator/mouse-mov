import cv2
import numpy as np
from pynput.mouse import Button, Controller

mouse=Controller()
import tkinter as tk

root = tk.Tk()

sx = root.winfo_screenwidth()
sy = root.winfo_screenheight()
root.quit()
(camx,camy)=(320,240)

#import time

#lower_red1 = np.array([0,50,50])
#upper_red1 = np.array([10,255,255])

#lower_red2 = np.array([160,100,100])
#upper_red2 = np.array([180,255,255])
lower_red1= np.array([30,150,50])
upper_red1 = np.array([255,255,180])
#l = np.array([17, 15, 100])	 
#u = np.array([50, 56, 200])

cm = cv2.VideoCapture(0)
mouseLoc_1=np.array((0,0))
alpha=0.85
press=0
cd=c=0
#status=start=0
while(True):
    _,img = cm.read()
    img=cv2.resize(img,(camx,camy))

    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    #cv2.imshow("hsv",hsv)

    mask = cv2.inRange(hsv,lower_red1,upper_red1)
    #$mask1 = cv2.inRange(hsv,lower_red2,upper_red2)
    #mask = mask0# + mask1

    kernelopen = np.ones((5,5))
    kernelclose = np.ones((20,20))

    mask_op = cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernelopen)
    mask_cl = cv2.morphologyEx(mask_op,cv2.MORPH_CLOSE,kernelclose)

    #cv2.imshow("tswt",mask_cl)
    '''percent=(np.count_nonzero(mask_cl!=0)/mask_cl.size)*100
    
    if(percent > 0.1):
        if(start!=0):
            end=time.time()-start
            if(end>5 and end <10):
                print("clicked")
        else:
            start=1
    else:
        start=time.time()
        
    '''
    conts,h=cv2.findContours(mask_cl.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(img,conts,-1,(255,0,0),3)
    #circles = cv2.HoughCircles(mask_cl,cv2.HOUGH_GRADIENT,3.5,15)
                               #param1=100,param2=100,minRadius=0,maxRadius=0)
    '''for i in range(len(conts)):
        x,y,w,h=cv2.boundingRect(conts[i])
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255), 2)'''
        #cv2.putText(img, str(i+1),(x,y+h),font,1,(0,255,255),2)

    if(len(conts)==1):
        if(press==1):
            press=0
            mouse.release(Button.left)
        
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(64,235,52),2)
        
        cx=int(x1+w1/2)
        cy=int(y1+h1/2)
        cv2.circle(img, (cx,cy),2,(0,0,255),2)
        mouseLoc_2=np.array((sx-(cx*sx/camx), cy*sy/camy))
        mouseLoc_1=mouseLoc=alpha*mouseLoc_2+(1-alpha)*mouseLoc_1
        
        mouse.position=tuple(mouseLoc)
        
        
        
        
    elif(len(conts)==2):
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(64,235,52),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(64,235,52),2)
        cx1=int(x1+w1/2)
        cy1=int(y1+h1/2)
        cx2=int(x2+w2/2)
        cy2=int(y2+h2/2)
        cx=int((cx1+cx2)/2)
        cy=int((cy1+cy2)/2)
        cv2.line(img, (cx1,cy1),(cx2,cy2),(255,0,0),2)
        cv2.circle(img, (cx,cy),2,(0,0,255),2) #cursor cx cy
        mouseLoc_2=np.array((sx-(cx*sx/camx), cy*sy/camy))
        mouseLoc_1=mouseLoc=alpha*mouseLoc_2+(1-alpha)*mouseLoc_1
        
        mouse.position=tuple(mouseLoc)
        if(press==0):
            mouse.click(Button.left, 2)
            press=1
            c=cd=0
        else:
            if(c<5):
                c+=1
            else:
                press=0
    
    elif(len(conts)==3):
        x1,y1,w1,h1=cv2.boundingRect(conts[0])
        x2,y2,w2,h2=cv2.boundingRect(conts[1])
        x3,y3,w3,h3=cv2.boundingRect(conts[2])
        cv2.rectangle(img,(x1,y1),(x1+w1,y1+h1),(64,235,52),2)
        cv2.rectangle(img,(x2,y2),(x2+w2,y2+h2),(64,235,52),2)
        cv2.rectangle(img,(x3,y3),(x3+w3,y3+h3),(64,235,52),2)
        
        cx1=int(x1+w1/2)
        cy1=int(y1+h1/2)
        cx2=int(x2+w2/2)
        cy2=int(y2+h2/2)
        cx3=int(x3+w3/2)
        cy3=int(y3+h3/2)
        
        cx=int((cx1+cx2+cx3)/3)
        cy=int((cy1+cy2+cy3)/3)
        
        cv2.line(img, (cx,cy),(cx1,cy1),(255,0,0),2)
        cv2.line(img, (cx,cy),(cx2,cy2),(255,0,0),2)
        cv2.line(img, (cx,cy),(cx3,cy3),(255,0,0),2)
        
        cv2.circle(img, (cx,cy),2,(0,0,255),2) #cursor
        
        mouseLoc_2=np.array((sx-(cx*sx/camx), cy*sy/camy))
        mouseLoc_1=mouseLoc=alpha*mouseLoc_2+(1-alpha)*mouseLoc_1
        
        mouse.position=tuple(mouseLoc)
        mouse.press(Button.left)
#        if(cd==0):
#            cd+=3
#        else:
#            if(cd>3):
#                mouse.press(Button.left)
                
        


    cv2.imshow("outPut",img)



    if(cv2.waitKey(1)==ord('q')):
        break


cm.release()
cv2.destroyAllWindows()
