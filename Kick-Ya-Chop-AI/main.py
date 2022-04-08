import cv2 as cv
import numpy as np
from mss import mss
import keyboard as kb
from time import sleep
import pyautogui as pg


class KickYaChopAI:
    def __init__(self, x_left=340, x_right=600, y=900):

        # set constants
        pg.PAUSE = 0
        self.y = y
        self.x_left = x_left
        self.x_right = x_right

        # set variables
        self.left = True
        self.x = x_left

        # initiate screenshotter
        self.sct = mss()

        # load images for template matching
        self.wood_left = cv.imread('wood-left.jpg')
        self.wood_right = cv.imread('wood-right.jpg')

        # get width and height of images
        self.w = self.wood_left.shape[1]
        self.h = self.wood_right.shape[0]

    def look_and_punch(self, left=254, right=549,
                       top=650, width=183, height=170,
                       saw_branch=False):

        if self.left:
            scr = np.array(self.sct.grab({
                'left': left,
                'top': top,
                'width': width,
                'height': height
            }))
            wood = self.wood_left
        else:
            scr = np.array(self.sct.grab({
                'left': right,
                'top': top,
                'width': width,
                'height': height
            }))
            wood = self.wood_right

        scr_no_alpha = scr[:, :, :3]

        result = cv.matchTemplate(scr_no_alpha, wood, cv.TM_CCOEFF_NORMED)

        _, max_val, _, max_loc = cv.minMaxLoc(result)

        # if branch observed
        if max_val > .85:
            saw_branch = True
            self.left = not self.left
            if self.left:
                self.x = self.x_left
            else:
                self.x = self.x_right

            cv.rectangle(scr, max_loc, (max_loc[0] + self.w, max_loc[1] + self.h),
                         (0, 255, 255), 2)

        cv.imshow('screenshot', scr)
        cv.setWindowProperty('screenshot', cv.WND_PROP_TOPMOST, 1)
        cv.waitKey(1)
        pg.click(x=self.x, y=self.y)

        return saw_branch


if __name__ == '__main__':

    # initiate AI
    ai = KickYaChopAI()

    # instructions
    print("Press 's' to start playing.")
    print("Once started, press 'q' to quit.")
    kb.wait('s')

    restart_count = 0
    break_count = 0
    while True:
        break_count += 1
        restart_count += 1

        # if branch observed
        if ai.look_and_punch():
            restart_count = 0

        # if branch not observed for a while..
        if restart_count > 1000:
            sleep(1)
            restart_count = 0
            # ..click restart button
            pg.click(x=460, y=1000)

        if break_count > 1000:
            sleep(1)
            break_count = 0
            ai.look_and_punch(top=700)

        if kb.is_pressed('q'):
            break
