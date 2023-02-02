import pyautogui
import time

i = 0
while True:
  if i%2 == 0:
    pyautogui.moveTo(300,500)
    pyautogui.click()
  else:
    pyautogui.moveTo(800,500)
    pyautogui.click()
  i+=1
  time.sleep(30)