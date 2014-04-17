#!/usr/bin/python
import cv2

class Mirror():

    def __init__(self, window_name="mirror", camera_number=0):
        self.window_name = window_name
        cv2.namedWindow(self.window_name)
        self.video_capture = cv2.VideoCapture(camera_number)

    def loop(self):
        if not self.video_capture.isOpened(): # try to get the first frame
            return

        while True:
            self.frame()
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                break

    def frame(self):
        rval, frame = self.video_capture.read()  # frame is 720x1280x3
        cv2.imshow(self.window_name, frame)

    def shutdown(self):
        cv2.destroyWindow(self.window_name)


def main():
    mirror = Mirror()
    mirror.loop()
    mirror.shutdown()

if __name__ == "__main__":
    main()
