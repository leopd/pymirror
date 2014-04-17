#!/usr/bin/python
import cv2


class Library():
    """A class for storing all the images to be used
    """
    def __init__(self):
        pass

    def add(self, frame):
        pass
        

class Mirror():

    def __init__(self, window_name="mirror", camera_number=0):
        self.window_name = window_name
        cv2.namedWindow(self.window_name)
        self.video_capture = cv2.VideoCapture(camera_number)
        self.library = Library()

    def loop(self):
        if not self.video_capture.isOpened(): # try to get the first frame
            return

        while True:
            ok = self.frame()
            if not ok:
                return
            key = cv2.waitKey(20)
            if key == 27: # exit on ESC
                return

    def shutdown(self):
        cv2.destroyWindow(self.window_name)

    def frame(self):
        ok, frame = self.video_capture.read()  # frame is 720x1280x3
        self.store_frame(frame)
        processed = self.process_frame(frame)
        cv2.imshow(self.window_name, processed)
        return ok

    def store_frame(self,frame):
        self.library.add(frame)

    def process_frame(self,frame):
        return frame


def main():
    mirror = Mirror()
    mirror.loop()
    mirror.shutdown()

if __name__ == "__main__":
    main()
