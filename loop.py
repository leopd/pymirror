#!/usr/bin/python
import numpy as np
import cv2
import time


class Library():
    """A class for storing all the images to be used
    """
    def __init__(self, size=81, coarseness=5):
        self.s = size
        self.lib = {}
        self.coarseness = coarseness


    def shrink(self, frame):
        return cv2.resize(frame, (self.s,self.s))


    def index(self, img):
        i = int( img.mean() / self.coarseness ) * self.coarseness
        return i


    def add(self, frame):
        mini = self.shrink(frame)
        i = self.index(mini)
        self.lib[i] = mini


    def missing_image(self,idx):
        return np.zeros((self.s,self.s,3)) + idx


    def find_nearest(self, frame):
        mini = self.shrink(frame)
        i = self.index(mini)
        try:
            return self.lib[i]
        except KeyError:
            return self.missing_image(i)


class ColorLibrary(Library):

    def index(self, img):
        avg_color = img.mean(axis=0).mean(axis=0)
        i = str(list(np.around(avg_color/self.coarseness)*self.coarseness))
        return i

    def missing_image(self,idx):
        color = np.asarray(eval(idx))
        return np.zeros((self.s,self.s,3)) + color



class Tile():
    def __init__(self, y1, y2, x1, x2):
        self.y1 = y1
        self.y2 = y2
        self.x1 = x1
        self.x2 = x2


    def extract(self, img):
        """Extracts the tile"""
        return img[self.y1:self.y2, self.x1:self.x2]


    def replace(self, base, newtile):
        """Places newtile into base"""
        base[self.y1:self.y2, self.x1:self.x2] = newtile



class Mirror():

    def __init__(self, window_name="mirror", camera_number=0):
        self.window_name = window_name
        cv2.namedWindow(self.window_name)
        self.video_capture = cv2.VideoCapture(camera_number)
        self.XX = 729
        self.YY = 729
        self.s = 40
        self.library = Library(self.s)

        self.output = np.zeros((self.XX,self.YY,3))


    def display(self):
        if not self.video_capture.isOpened(): # try to get the first frame
            print "Failed to open camera."
            return

        start = time.time()
        frame_cnt = 0

        while True:
            ok = self.tick()
            if not ok:
                return
            frame_cnt += 1
            key = cv2.waitKey(10)  # Needed for some reason.
            if( time.time() - start > 5 ):
                # Every 5 seconds, print fps.
                fps = frame_cnt / (time.time() - start)
                print "%.1f fps" % fps
                frame_cnt = 0
                start = time.time()
                

    def shutdown(self):
        cv2.destroyWindow(self.window_name)


    def normalize(self, frame):
        """Convert it to the expected size"""
        f = cv2.resize(frame, (self.XX,self.YY))
        f = cv2.flip(f,1)
        return f


    def tick(self):
        """Called once per frame.  Main logic here."""
        ok, frame = self.video_capture.read()  # frame is 720x1280x3
        frame = self.normalize(frame)
        self.store_frame(frame)
        processed = self.process_frame(frame)
        cv2.imshow(self.window_name, processed)
        return ok


    def store_frame(self,frame):
        self.library.add(frame)


    def process_chunk(self, chunk):
        nearest = self.library.find_nearest(chunk)
        return np.resize(nearest, chunk.shape)


    def tiles(self):
        s = self.s
        for x in range(0, self.XX, s):
            for y in range(0, self.YY, s):
                yield Tile(y,y+s,x,x+s)


    def process_frame(self,frame):
        for t in self.tiles():
            chunk = t.extract(frame)
            t.replace(frame, self.process_chunk(chunk))
        #print "frame is %s" % str(frame.shape)
        return frame



def main():
    mirror = Mirror()
    mirror.display()
    mirror.shutdown()

if __name__ == "__main__":
    main()

