#!/usr/bin/python
import numpy as np
import cv2


class Library():
    """A class for storing all the images to be used
    """
    def __init__(self):
        pass

    def add(self, frame):
        pass

    def find_nearest(self, frame):
        return frame
        

class Mirror():

    def __init__(self, window_name="mirror", camera_number=0):
        self.window_name = window_name
        cv2.namedWindow(self.window_name)
        self.video_capture = cv2.VideoCapture(camera_number)
        self.library = Library()
        self.XX = 729
        self.YY = 729

    def display(self):
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


    def normalize(self, frame):
        """Convert it to the expected size"""
        return cv2.resize(frame, (self.XX,self.YY))


    def frame(self):
        ok, frame = self.video_capture.read()  # frame is 720x1280x3
        frame = self.normalize(frame)
        self.store_frame(frame)
        processed = self.process_frame(frame)
        cv2.imshow(self.window_name, processed)
        return ok

    def store_frame(self,frame):
        self.library.add(frame)

    def process_chunk(self, chunk):
        average_color = chunk.mean(axis=0).mean(axis=0)  # 3x1 vector
        output = np.zeros(chunk.shape) + average_color
        #print "input: %s" % str(chunk.shape)
        #print "output: %s" % str(output.shape)
        return output

    def process_frame(self,frame):
        for x in range(0, self.XX, 81):
            for y in range(0, self.YY, 81):
                chunk = frame[x:x+81,y:y+81]
                frame[x:x+81,y:y+81] = self.process_chunk(chunk)
        #print "frame is %s" % str(frame.shape)
        return frame


def main():
    mirror = Mirror()
    mirror.display()
    mirror.shutdown()

if __name__ == "__main__":
    main()
