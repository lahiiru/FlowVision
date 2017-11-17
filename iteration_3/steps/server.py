from multiprocessing.connection import Listener
import numpy as np

listener1 = Listener(('localhost', 6000), authkey=b'secret password')
listener2 = Listener(('localhost', 6001), authkey=b'secret password')
x = [np.random.randn(640*480*3)]*100
while True:
    conn1 = listener1.accept()
    print('connection accepted from', listener1.last_accepted)
    conn1.send([x])
    conn2 = listener2.accept()
    print('connection accepted from', listener2.last_accepted)
    conn2.send([x])
    print conn1.recv()
    print conn2.recv()

conn1.close()
listener1.close()

conn2.close()
listener2.close()