import cv2 as cv
import pytesseract
import numpy as np
from windowcapture import WindowCapture

pytesseract.pytesseract.tesseract_cmd = r"F:\Program Files\Tesseract-OCR\tesseract"

wincap = WindowCapture()
screenshot = wincap.get_video()
spot = screenshot[3:117, 1190:1301]
cv.imwrite("spot.png", spot)
target = screenshot[513:534, 4:24]
cv.imwrite("target.png", target)
click_target = screenshot[513:527, 25:125]
cv.imwrite("click_target.png", click_target)

class Vision:
    hp = 0
    mana = 0
    soul = 0
    capacity = 0
    speed = 0
    food = 0
    is_hungry = True
    is_attacking = False
    is_on_spot = False
    is_mob_on_screen = False
    spot = cv.imread("spot.png", cv.IMREAD_UNCHANGED)
    target = cv.imread("target.png", cv.IMREAD_UNCHANGED)
    target = target[:,:,:3]
    spot_mark = cv.imread("spot_mark.png", cv.IMREAD_UNCHANGED)
    lure_mark = cv.imread("lure_mark.png", cv.IMREAD_UNCHANGED)
    click_mark = cv.imread("click_target.png", cv.IMREAD_UNCHANGED)
    umbral = 0.99
    true_counter = 0
    false_counter = 0
    target_umbral = 0.87
    spot_umbral = 0.72
    mob_on_screen_umbral = 0.2
    h = 767
    w = 1359

    def __init__(self, max_hp, max_mana):
        self.max_hp = max_hp
        self.max_mana = max_mana

    def get_attacking_state(self, screenshot):
        battle_list = screenshot[513:556, 4:24]
        battle_list = battle_list[:,:,:3]
        res = cv.matchTemplate(battle_list, self.target, cv.TM_CCOEFF_NORMED)
        self.min_val, self.max_val, self.min_loc, self.max_loc = cv.minMaxLoc(res)
        if self.max_val < self.target_umbral:
            if self.false_counter < 2:
                self.false_counter += 1
            elif self.false_counter >= 2:
                self.is_attacking = False
        elif self.max_val > self.target_umbral:
            self.false_counter = 0
            self.is_attacking = True

    def get_pos(self, screenshot):
        map = screenshot[3:117, 1190:1301]
        map = map[:,:,:3]
        res2 = cv.matchTemplate(map, self.spot, cv.TM_CCOEFF_NORMED)
        self.min_val2, self.max_val2, self.min_loc2, self.max_loc2 = cv.minMaxLoc(res2)
        if self.max_val2 >= self.umbral:
            if self.true_counter < 2:
                self.true_counter += 1
            elif self.true_counter >= 2:
                self.is_on_spot = True
        elif self.max_val2 < self.umbral:
            self.true_counter = 0
            self.is_on_spot = False

    def get_spot(self, screenshot):
        res3 = cv.matchTemplate(screenshot, self.spot_mark, cv.TM_CCOEFF_NORMED)
        self.min_val3, self.max_val3, self.min_loc3, self.max_loc3 = cv.minMaxLoc(res3)
        x = self.max_loc3[0] + 5
        y = self.max_loc3[1] + 25
        return x, y

    def get_lure_spot(self, screenshot):
        res5 = cv.matchTemplate(screenshot, self.lure_mark, cv.TM_CCOEFF_NORMED)
        self.min_val5, self.max_val5, self.min_loc5, self.max_loc5 = cv.minMaxLoc(res5)
        x_spot = self.max_loc5[0] + 5
        y_spot = self.max_loc5[1] + 25
        return x_spot, y_spot

    def mob_on_screen(self, screenshot):
        sprite = screenshot[513:534, 4:24]
        sprite = sprite[:,:,:3]
        res4 = cv.matchTemplate(sprite, self.target, cv.TM_CCOEFF_NORMED)
        self.min_val4, self.max_val4, self.min_loc4, self.max_loc4 = cv.minMaxLoc(res4)
        if self.max_val4 < self.mob_on_screen_umbral:
            self.is_mob_on_screen = False
        elif self.max_val4 > self.mob_on_screen_umbral:
            self.is_mob_on_screen = True

    def get_click_pos(self, screenshot):
        area = screenshot[513:554, 24:130]
        area = area[:,:,:3]
        res6 = cv.matchTemplate(area, self.click_mark, cv.TM_CCOEFF_NORMED)
        self.min_val6, self.max_val6, self.min_loc6, self.max_loc6 = cv.minMaxLoc(res6)
        if self.max_loc6[0] == 1 and self.max_loc6[1] == 0:
            x_click = 14
            y_click = 546
        elif self.max_loc6[0] == 1 and self.max_loc6[1] == 22:
            x_click = 14
            y_click = 566
        else:
            x_click = 14
            y_click = 650
        return x_click, y_click

    def get_battlelist(self, screenshot):
        battle_list = screenshot[514:740, 24:140]
        battle_list = pytesseract.image_to_string(battle_list, config=r'--oem 3 --psm 6')
        battle_list = battle_list.splitlines()
        for char in battle_list:
            if char == "":
                battle_list.remove(char)
        return battle_list

    def get_stats(self, screenshot):
        stats = screenshot[87:172, 113:157]
        stats = pytesseract.image_to_string(stats, config="digits")
        stats = stats.split()
        for stat in stats:
            try:
                stat = int(stat)
            except:
                pass
        self.hp = stats[0]
        self.mana = stats[1]
        self.soul = stats[2]
        self.capacity = stats[3]
        self.speed = stats[4]
        self.food = stats[5]