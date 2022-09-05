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

#ket noi camera

#tao cua so windown
windown = Tk()
windown.title("MAIN INTERFACE")
windown.geometry("830x550")
#tao label chua hinh anh
label1 = Label(windown,bd = 5,relief  = "sunken")
label2 = Label(windown,bd = 5,relief  = "sunken")

#tao fram chua  khung ten
fram = LabelFrame(windown,relief  = "sunken",bd =2,padx =20,pady =50,bg ="cyan",highlightthickness = 3,highlightbackground = "blue")
fram.grid(row = 1, column =1,pady = 5 )
fram1 = LabelFrame(windown)
fram1.grid(row = 0,column = 0,columnspan = 2)
fram2 = LabelFrame(fram,bg ="cyan",bd = 0)
fram2.pack(padx = 10,pady = 0)
fram3 = LabelFrame(fram,bg = "cyan",bd = 0)
fram3.pack(pady = 5)
fram4 = LabelFrame(fram,bg = "cyan",bd =0)
fram4.pack(pady  =5,side = LEFT)
fram5 = LabelFrame(fram,bg = "cyan",bd =0)
fram5.pack(pady  =5)
#tao cac tham so
i = 0
option = ["SELEC COM","COM1","COM2","COM3","COM4","COM6"]
# ket noi voi arduino qua serial
data = serial.Serial("COM3",115200)
#load model
#lon_bia: 0 / hop_sua : 1 /
model = torch.hub.load("ultralytics/yolov5","custom",path = "last_2_run.pt")

def detection():
    global  ketqua,do_cxac,so_luong_hop_sua
    #part = "F:\PLSP_ok\\sua.jpg"
    cap = cv2.VideoCapture(1)
    while True:
        ret,img = cap.read()
        #img = cv2.imread(part)
        img = cv2.resize(img,(400,400))
        #img = creat_img()
        #img = cv2.resize(img,None,fx=0.3,fy=0.3)
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
                    ketqua.config(text = "RESULT:  " + name)
                    do_cxac.config(text = "CONFIDENCE:  " + str(confidence))
                #print(confidence)
                #print(name)
                #if name != "":
                    if name == "hop_sua":
                        print(name)
                        output = data.write('1'.encode())
                        data_in = data.readline().decode("ascii")
                        print(data_in)
                        print(output)
                        time.sleep(1)
                        so_luong_hop_sua.config(text="1")
                        #print("ok")
                    if name == "lon_bia":
                        print(name)
                        output = data.write('2'.encode())
                        print(output)
                        time.sleep(5)
                        #output = data.write('2'.encode())
                        #print("ok")
        cv2.imshow('frame', img)
        cv2.waitKey(1)
        #cv2.imshow('frame', img)
        #cv2.waitKey(1)

    #print(dc)
        return img

    #cap.release()
    #cv2.destroyAllWindows()

def show_img():
    global i
    # Get the latest frameơ and convert into Image
    img = detection()
    img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    img = Image.fromarray(img)

    # Convert image to PhotoImage
    imgtk = ImageTk.PhotoImage(image=img)
    label1.imgtk = imgtk
    label1.configure(image=imgtk)
    label1.grid(row = 1, column = 0,pady =10)

def startdc():
    data.write("5".encode())

def stopdc():
    data.write("6".encode())

def TTKETNOI():
    global trang_thai,data
    data.baudrate = 115200
    if cmb.get() == "COM3":
        data.port = cmb.get()
        time.sleep(1)
        trang_thai.config(text = "TT: Connected..")
    else:
        time.sleep(1)
        trang_thai.config(text="TT: Error..!")

part = "F:\PLSP_ok\\sua.jpg"
img_from = cv2.imread(part)
img_from = cv2.resize(img_from,(400,400))
img_from = cv2.cvtColor(img_from,cv2.COLOR_BGR2RGB)
canvas = Canvas(windown,width = 400,height = 400,bg = "red",relief  = "sunken")
canvas.grid(row = 1, column = 0,pady =10)
photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img_from))

def updatefram():
    global canvas,photo

    if data.in_waiting:
        #time.sleep(0.8)
        fram = detection()
        #data.write(dc.encode())
        fram = cv2.cvtColor(fram,cv2.COLOR_BGR2RGB)
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(fram))


    canvas.create_image(0,0, image = photo,anchor = NW)
    windown.after(500,updatefram)

#creat GUI with tkinter

#hien thi khung va logo
# logo = Label(fram1,image = icon ).grid(row = 0, column = 0)

tieu_de = Label(fram1,text = "ĐỒ ÁN TỐT NGHIỆP \n Đề Tài : Thiết kế chế tạo mô hình hệ thống phân loại rác thải tự động ứng dụng trí tuệ nhân tạo ",font = ("Helvetica",28),fg = "black",padx = 20,pady =10,relief  = "sunken",bd = 5,bg = "yellow")
tieu_de.grid(row = 0,column = 1)

# lable = Label(windown,text = "ANH DETECTION",fg = "blue",font = ("Helvetica",20),relief  = "sunken")
# lable.grid(row = 2,column = 0)

start = Button(fram2,text = "START",width = 5,padx = 10,pady =10,height  = 1,relief  = "sunken",bd =2,bg = "green",fg = "black",font = ("Helvetica",20),command = startdc)
start.grid(row = 0,column = 0,padx =20,pady =10)

stop = Button(fram2,text = "STOP",padx = 10,pady =10,width = 5,height  = 1,relief  = "sunken",bd =2,bg = "red",fg = "black",font = ("Helvetica",20),command = stopdc)
stop.grid(row = 0,column = 1,padx =20,pady =10)
# ket noi voi arrduino
cmb = tk.Combobox(fram3,value = option,font = ("Helvetica",15))
cmb.set(option[0])
cmb.grid(row = 0,column =0,padx = 10)

connect = Button(fram3, text = "Connect",font = ("Helvetica",15),relief  = "sunken",command = TTKETNOI)
connect.grid(row = 0,column = 1,padx = 10,pady = 5)

trang_thai = Label(fram3,text = "TT: ",font = ("Helvetica",15),relief  = "sunken",bd =2)
trang_thai.grid(row = 1,column = 0,columnspan = 2,padx =10,pady = 5)
#hien thi ket qua va do chinh xac
ketqua = Label(fram4,text = "RESULT : ",fg="blue", font=("Helvetica", 15),bg ="cyan")
ketqua.grid(row = 0, column = 0,pady = 5 ,sticky = W,padx = 50)

do_cxac = Label(fram4,text = "CONFIDENCE : ",fg="blue", font=("Helvetica", 15),bg ="cyan")
do_cxac.grid(row = 1, column = 0,pady = 5,sticky = W)
#hien thi so luong
#so_luong_hop_sua = Label(fram4,text = "RESULT : ",fg="blue", font=("Helvetica", 15),bg ="cyan")
#so_luong_hop_sua.grid(row=2 ,column = 0, pady= 5)

#call funcion

updatefram()
#detection()
#print(detection())

windown.mainloop()
