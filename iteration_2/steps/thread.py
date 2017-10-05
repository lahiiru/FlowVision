import threading
import time
import cv2
from Queue import Queue

mutex = threading.Lock()
main_frames = Queue()
frame_q1 = Queue()
start = 0


class CamReader(threading.Thread):
    frameNo = 0
    cap = cv2.VideoCapture(1)

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):

        start = time.time()
        while True:
            r, img = self.cap.read()
            # print '[CamReader', self.counter, '] queueSize', main_frames.qsize()
            if (main_frames.qsize() == 100):
                print 'time : ', time.time() - start
                for i in main_frames.queue: frame_q1.put(i)
                main_frames.queue.clear()

            main_frames.put(img)
            CamReader.frameNo = CamReader.frameNo + 1


class ImageWriter(threading.Thread):
    frameNo = 0

    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        while True:

            mutex.acquire()
            ImageWriter.frameNo = ImageWriter.frameNo + 1
            local_frameNo = ImageWriter.frameNo

            try:
                # print '[ImageWriter', self.counter, '] queueSize', frame_q1.qsize()
                if (frame_q1.empty()):
                    continue
                img = frame_q1.get()
            except:
                pass
            finally:
                mutex.release()
                time.sleep(0.1)
            cv2.imwrite('real_frames/' + str(local_frameNo) + '.jpg', img)


# Create new threads
thread1 = CamReader(1, "Thread-1", 1)
thread2 = ImageWriter(2, "Thread-1", 1)
thread3 = ImageWriter(3, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
thread3.start()
