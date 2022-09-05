import tkinter
import serial
import cv2
import numpy
import torch
from tkinter import *
from PIL import ImageTk,Image
import tkinter.ttk as tk
import PIL.Image,PIL.ImageTk
import time

model = torch.hub.load("ultralytics/yolov5","custom",path = "best_3_500.pt")

#data = serial.Serial("COM3",115200)

def detection():
    global  ketqua,do_cxac
    count = 1
    count1 = 1
    count2 = 1
    #part = "F:\PLSP_ok\\sua.jpg"
    cap = cv2.VideoCapture(1)
    while True:
        ret,img = cap.read()
        #img = cv2.imread(part)
        img = cv2.resize(img,(400,400))
        detection = model(img)
        rusult = detection.pandas().xyxy[0].to_dict(orient = "records")
        x = numpy.array(rusult)
        if len(x):
            for result in rusult:
                confidence = round(result['confidence'],2)
                name = result["name"]
                clas = result["class"]
                if confidence > 0.5:
                            x1 = int(result["xmin"])
                            y1 = int(result["ymin"])
                            x2 = int(result["xmax"])
                            y2 = int(result["ymax"])
                            #print(x1,y1,x2,y2)

                            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
                            cv2.putText(img,name,(x1+3,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),1)
                            #ketqua.config(text = "RESULT:  " + name)
                            #do_cxac.config(text = "CONFIDENCE:  " + str(confidence))
                            #clas = str(clas)
                print(name)
                print(confidence)
                #if name == "hop_sua":
                    #print(name)
                    #while count < 100:
                        #print(count)
                        #count += 1
                        #break
                    #time.sleep(5)
        cv2.imshow('frame', img)
        cv2.waitKey(1)
        #return img
def run():
    global  ketqua,do_cxac
    #part = "F:\PLSP_ok\\sua.jpg"
    cap = cv2.VideoCapture(1)
    while True:
        ret,img = cap.read()
        #img = cv2.imread(part)
        img = cv2.resize(img,(400,400))
        detection = model(img)
        rusult = detection.pandas().xyxy[0].to_dict(orient = "records")
        x = numpy.array(rusult)
        if len(x):
            count = 0
            for result in rusult:
                confidence = round(result['confidence'],2)
                name = result["name"]
                clas = result["class"]
                if confidence > 0.5:
                            x1 = int(result["xmin"])
                            y1 = int(result["ymin"])
                            x2 = int(result["xmax"])
                            y2 = int(result["ymax"])
                            #print(x1,y1,x2,y2)

                            cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,0),2)
                            cv2.putText(img,name,(x1+3,y1-10),cv2.FONT_HERSHEY_COMPLEX,0.8,(0,255,0),1)
                            #ketqua.config(text = "RESULT:  " + name)
                            #do_cxac.config(text = "CONFIDENCE:  " + str(confidence))
                            #clas = str(clas)
                #if name != "":
                    #if name == "hop_sua":
                print(name)
                print(confidence)
                        #output = data.write('1'.encode())
                        #time.sleep(5)
                        #output = data.write(name.encode())
                        #print("ok")

        cv2.imshow('frame', img)
        cv2.waitKey(1)

detection()
#run()
#print(detection())