import cv2 as cv
import numpy as np
from mss import mss
import keyboard as kb
import pyautogui as pg
from time import time, sleep


pg.PAUSE = 0

print("Press 's' to start playing.")
print("Once started, press 'q' to quit.")
kb.wait('s')

left = True
x = 340
y = 900

sct = mss()

dimensions_left = {
  'left': 254,
  'top': 650,
  'width': 183,
  'height': 160
  }

dimensions_right = {
  'left': 549,
  'top': 650,
  'width': 183,
  'height': 160
  }

wood_left = cv.imread('wood-left.jpg')
wood_right = cv.imread('wood-right.jpg')

w = wood_left.shape[1]
h = wood_left.shape[0]

fps_time = time()
count = 0

while True:
  count += 1

  if left:
    scr = np.array(sct.grab(dimensions_left))
    wood = wood_left
  else:
    scr = np.array(sct.grab(dimensions_right))
    wood = wood_right

  scr_no_alpha = scr[:,:,:3]

  result = cv.matchTemplate(scr_no_alpha, wood, cv.TM_CCOEFF_NORMED)

  _, max_val, _, max_loc = cv.minMaxLoc(result)

  if max_val > .85:
    count = 0
    left = not left
    if left:
      x=340
    else:
      x=600

    cv.rectangle(scr, max_loc, (max_loc[0] + w, max_loc[1] + h), (0,255,255), 2)
    
  if count > 200:
    pg.click(x=460,y=1000)
    sleep(1)

  cv.imshow('screenshot', scr)
  cv.setWindowProperty('screenshot', cv.WND_PROP_TOPMOST, 1)
  cv.waitKey(1)
  pg.click(x=x, y=y)
  if kb.is_pressed('q'):
    break

  fps_time = time()
