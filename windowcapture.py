import cv2 as cv

class WindowCapture:
    def get_video(self):
        screenshot = cv.VideoCapture(0, cv.CAP_DSHOW)
        screenshot.set(3, 1360)
        screenshot.set(4, 768)
        # Capture frame-by-frame
        ret, frame = screenshot.read()
        return frame
    def make_visible(self, screenshot):
        # Escala de grises
        visible_frame = cv.cvtColor(screenshot, cv.COLOR_BGR2GRAY)
        return visible_frame