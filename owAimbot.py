import cv2 as cv2
import numpy as np
import os
import keyboard
import time
from mss import mss
from PIL import Image
from vision import Vision
import win32api, win32con 
import math
import tkinter as tk


Charecter, Aim, Binds = "", "", {}
mon = {'left': 560, 'top': 240, 'width': 800, 'height': 600}

def AimBot():

    cascade_ow = cv2.CascadeClassifier("cascadeV2/cascade.xml")
    vision_ow = Vision(None)

    Active = True

    prevDiffMax = math.sqrt(960**2 + 540**2)

    def AlwaysAim(x,y):
        win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y)

    def AimWhenShoot(x,y):
        if win32api.GetKeyState(0x01) == -127 or win32api.GetKeyState(0x01) == -128:
            win32api.mouse_event(win32con.MOUSEEVENTF_MOVE | win32con.MOUSEEVENTF_ABSOLUTE, x, y)
    
    with mss() as sct:
        while True:
            loop_time = time.time()
            supp = cv2.waitKey(1) & 0xFF

            screenShot = sct.grab(mon)
            img = np.array(Image.frombytes('RGB', (screenShot.width, screenShot.height), screenShot.rgb, ))

            rectangles = cascade_ow.detectMultiScale(img)
            detection_image = vision_ow.draw_rectangles(img, rectangles)

            cv2.imshow('test', detection_image)
            
            if (len(rectangles)>0 and Active):
                targets = vision_ow.get_click_points(rectangles)
                prevDiff = prevDiffMax
                target = None
                for currTarget in targets:
                    pos_x = (currTarget[0] + mon['left'])
                    pos_y = (currTarget[1] + mon['top'])
                    diff = math.sqrt((960-pos_x)**2 + (540-pos_y)**2)
                    if (diff < prevDiff):
                        target = currTarget
                        prevDiff = diff
                pos_x = (target[0] + mon['left'])
                pos_y = (target[1] + mon['top'])
            
                if (Aim == "Always"):
                    AlwaysAim(pos_x, pos_y)
                else:
                    AimWhenShoot(pos_x, pos_y)

            if keyboard.is_pressed(Binds["Kill"]):
                break
            elif keyboard.is_pressed(Binds["OnOff"]):
                if Active:
                    Active = False
                else:
                    Active = True
                time.sleep(0.5)
            elif keyboard.is_pressed(Binds["Capture"]):
                detection_image = vision_ow.draw_rectangles(img, rectangles)
                cv2.imwrite("data//Inspect//{}.jpg".format(loop_time), detection_image)
                time.sleep(0.5)
    

def UI():
    root = tk.Tk()
    ws = root.winfo_screenwidth() 
    hs = root.winfo_screenheight() 

    w = 400
    h = 300

    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)

    root.geometry('%dx%d+%d+%d' % (w, h, x, y))
    root.resizable(False,False)

    background_image=tk.PhotoImage(file = "data//WallPaper//BackGround.png",)
    background_label = tk.Label(root, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    Title = tk.Label(text="Configure AimBot", fg="white", bg="black")
    Title.config(font=("Ariel", 15))
    Title.pack()
    
    charecterLabel = tk.Label(root, text="Select Hero:",fg="white", bg="black")
    charecterLabel.pack( side = tk.LEFT)
    charecterLabel.place(x = 0, y = 50)

    aimLabel = tk.Label(root, text="Select Aim Mode:",fg="white", bg="black")
    aimLabel.pack( side = tk.LEFT)
    aimLabel.place(x = 154, y = 50)

    captureLabel = tk.Label(root, text="Select Capture HotKey:",fg="white", bg="black")
    captureLabel.pack( side = tk.LEFT)
    captureLabel.place(x = 90, y = 100)

    onOffLabel = tk.Label(root, text="Select On/Off HotKey:",fg="white", bg="black")
    onOffLabel.pack( side = tk.LEFT)
    onOffLabel.place(x = 90, y = 150)

    killLabel = tk.Label(root, text="Select Close HotKey:",fg="white", bg="black")
    killLabel.pack( side = tk.LEFT)
    killLabel.place(x = 90, y = 200)

    # Setting the variables
    def set(CharSelected, AimSelected, BindsSelected):
        ok = True
        try:
            if (len(BindsSelected["Capture"][0]) == 1 and len(BindsSelected["OnOff"][0]) == 1 and len(BindsSelected["Kill"][0]) == 1):
                ok = True
        except:
            ok = False

        if (ok and len(BindsSelected["Capture"][0]) == 1 and len(BindsSelected["OnOff"][0]) == 1 and len(BindsSelected["Kill"][0]) == 1):
            global Charecter, Aim, Binds
            Charecter = CharSelected
            Aim = AimSelected
            Binds = {"Capture": BindsSelected["Capture"][0],
                    "OnOff": BindsSelected["OnOff"][0],
                    "Kill": BindsSelected["Kill"][0],
                    }
            root.destroy()
        else:
            WarningLabel = tk.Label( root, text="All HotKeys must be one charecter")
            WarningLabel.configure(bg = "BLACK", fg = "RED",font=("Courier", 10))
            WarningLabel.pack()
            WarningLabel.place(x = 70, y = 280)
        
    # Charecter Select
    CharOptions = [
        "Any",
        "Widow",
        "Ash",
        "Sojuron",
        "Genji"
    ]

    CharClicked = tk.StringVar()
    CharClicked.set("Any")

    CharDrop = tk.OptionMenu( root , CharClicked , *CharOptions )
    CharDrop.configure(bg = "BLACK", fg = "WHITE",font=("Courier", 8))
    CharDrop.pack()
    CharDrop.place(x = 72, y = 46)

    #Aim Options Select
    AimOptions = [
        "Always",
        "When Shooting"
    ]
        
    AimClicked = tk.StringVar()
    AimClicked.set("Always")

    AimDrop = tk.OptionMenu( root , AimClicked , *AimOptions)
    AimDrop.configure(bg = "BLACK", fg = "WHITE",font=("Courier", 8))
    AimDrop.pack()
    AimDrop.place(x = 256, y = 46)
        
    # Binds
    border_color = tk.Frame(root, background="red")

    Capture = tk.Text(root, height = 1, width = 2)
    Capture.configure(bg = "BLACK", fg = "WHITE",bd = 3 ,font=("Courier", 10))
    Capture.pack()
    Capture.insert(tk.END,"r")
    Capture.place(x = 220, y = 101)

    OnOff = tk.Text(root, height = 1, width = 2)
    OnOff.configure(bg = "BLACK", fg = "WHITE",bd = 3 ,font=("Courier", 10))
    OnOff.pack()
    OnOff.insert(tk.END,"j")
    OnOff.place(x = 215, y = 150)

    Kill = tk.Text(root, height = 1, width = 2)
    Kill.configure(bg = "BLACK", fg = "WHITE",bd = 3 ,font=("Courier", 10))
    Kill.pack()
    Kill.insert(tk.END,"k")
    Kill.place(x = 206, y = 200)

    # Confirm button
    Configbutton = tk.Button( root , text = "CONFIRM" , command = lambda *args : set(CharClicked.get(), AimClicked.get(),
    {"Capture": Capture.get("1.0",tk.END).split(), "OnOff": OnOff.get("1.0",tk.END).split(), "Kill": Kill.get("1.0",tk.END).split()}))
    Configbutton.configure(bg = "BLACK", fg = "WHITE",font=("Courier",12))
    Configbutton.pack()
    Configbutton.place(x = 155, y = 240)

    root.mainloop()

if __name__ == "__main__":
    UI()
    if (Charecter and Aim and Binds):
        AimBot()

