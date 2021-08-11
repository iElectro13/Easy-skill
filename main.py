import cv2 as cv
import numpy as np
from windowcapture import WindowCapture
from vision import Vision
import pytesseract
import pyautogui
import time
import random
from threading import Thread

pyautogui.FAILSAFE = False
pytesseract.pytesseract.tesseract_cmd = r"F:\Program Files\Tesseract-OCR\tesseract"

class Bot:
    contador = 0
    wait_time = 1
    window_change = False
    
    def attack(self, x_click, y_click):
        if not self.window_change:
            pyautogui.moveTo(x_click, y_click, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(random.randint(322, 1038), random.randint(58, 583), self.wait_time, pyautogui.easeOutQuad)
        else:
            self.window_changer()
            pyautogui.moveTo(x_click, y_click, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(random.randint(322, 1038), random.randint(58, 583), self.wait_time, pyautogui.easeOutQuad)
            self.window_changer()

    def go_spot(self, x, y):
        if not self.window_change:
            pyautogui.moveTo(x, y, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(random.randint(322, 1038), random.randint(58, 583), self.wait_time, pyautogui.easeOutQuad)
        else:
            self.window_changer()
            pyautogui.moveTo(x, y, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(random.randint(322, 1038), random.randint(58, 583), self.wait_time, pyautogui.easeOutQuad)
            self.window_changer()

    def go_lure_spot(self, x_spot, y_spot):
        if not self.window_change:
            pyautogui.moveTo(x_spot, y_spot, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(random.randint(322, 1038), random.randint(58, 583), self.wait_time, pyautogui.easeOutQuad)
        else:
            self.window_changer()
            pyautogui.moveTo(x_spot, y_spot, self.wait_time, pyautogui.easeOutQuad)
            pyautogui.click()
            pyautogui.moveTo(random.randint(322, 1038), random.randint(58, 583), self.wait_time, pyautogui.easeOutQuad)
            self.window_changer()

    def exura(self):
        if not self.window_change:
            pyautogui.press("f3")
            time.sleep(1)
            self.contador += 1
        else:
            self.window_changer()
            pyautogui.press("f3")
            time.sleep(1)
            self.contador += 1
            self.window_changer()

    def eat(self):
        if not self.window_change:
            pyautogui.press("f4")
            time.sleep(1)
            self.contador = 0
        else:
            self.window_changer()
            pyautogui.press("f4")
            time.sleep(1)
            self.contador = 0
            self.window_changer()

    def pot(self):
        if not self.window_change:
            pyautogui.press("f1")
            time.sleep(1)
        else:
            self.window_changer()
            pyautogui.press("f1")
            time.sleep(1)
            self.window_changer()

    def mp(self):
        if not self.window_change:
            pyautogui.press("f2")
            time.sleep(1)
        else:
            self.window_changer()
            pyautogui.press("f2")
            time.sleep(1)
            self.window_changer()

    def window_changer(self):
        pyautogui.keyDown("alt")
        pyautogui.press("tab")
        pyautogui.keyUp("alt")

# Inicializar capturadora y visión
wincap = WindowCapture()
vision = Vision(200, 95)
bot = Bot() 


is_bot_in_action = False

def acciones():
    global is_bot_in_action

    if not vision.is_on_spot and not vision.is_attacking:
        bot.go_spot(x,y)
        for i in range(3):
            if not vision.is_on_spot:
                time.sleep(3)
            elif vision.is_on_spot:
                break

    if not vision.is_attacking and not vision.is_on_spot and vision.is_mob_on_screen:
        bot.attack(x_click, y_click)

    if not vision.is_attacking and vision.is_on_spot and vision.is_mob_on_screen:
        bot.attack(x_click, y_click)

    try:
        if vision.hp < 570:
            bot.exura()
    except:
        pass

    if bot.contador == 3:
        bot.eat()
    
    try:
        if vision.hp < 50:
            bot.pot()
            time.sleep(1)
    except:
        pass

    try:
        if vision.mana < 39:
            bot.mp()
    except:
        pass

    '''
    if not vision.is_mob_on_screen:
        bot.go_lure_spot(x_spot, y_spot)
        time.sleep(5)
    '''
    is_bot_in_action = False

time.sleep(4)
while True:
    # Obtener frame y frame blanco y negro
    screenshot = wincap.get_video()

    vision.get_attacking_state(screenshot)
    vision.get_pos(screenshot)
    vision.mob_on_screen(screenshot)
    x, y = vision.get_spot(screenshot)
    x_click, y_click = vision.get_click_pos(screenshot)
    vision.get_hp(screenshot)
    vision.get_mana(screenshot)
    if not is_bot_in_action:
        is_bot_in_action = True
        hilo1 = Thread(target=acciones)
        hilo1.start()

    cv.imshow("Easy", screenshot)

    # Tecla de salida
    # Esperar 1ms entre cada loop para procesar la tecla pulsada
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

'''
while True:
    # Obtener frame y frame blanco y negro
    screenshot = wincap.get_video()
    vision.get_stats(screenshot)

    print(vision.get_battlelist(screenshot))
    print(vision.hp, vision.mana, vision.soul, vision.capacity, vision.speed, vision.food)
    cv.imshow("Easy", screenshot)

    # Tecla de salida
    # Esperar 1ms entre cada loop para procesar la tecla pulsada
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break
    '''