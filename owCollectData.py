import cv2 as cv2
import numpy as np
import os
import keyboard
import time
from mss import mss
from PIL import Image

mon = {'left': 560, 'top': 240, 'width': 800, 'height': 600}

with mss() as sct:
   while True:
        loop_time = time.time()
        supp = cv2.waitKey(1) & 0xFF
        screenShot = sct.grab(mon)
        img = Image.frombytes('RGB', (screenShot.width, screenShot.height), screenShot.rgb, )
        cv2.imshow('test', np.array(img))

        if keyboard.is_pressed('k'):
            break
        elif keyboard.is_pressed('r'):
            cv2.imwrite("data//Positive_new//{}.jpg".format(loop_time), np.array(img))
            time.sleep(0.5)
        elif keyboard.is_pressed('t'):
            cv2.imwrite("data//Negative_new//{}.jpg".format(loop_time), np.array(img))
            time.sleep(0.5)
