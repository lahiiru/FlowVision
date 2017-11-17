from multiprocessing.connection import Client
import numpy as np
while True:
    conn = Client(('localhost', 6001), authkey=b'secret password')
    print(conn.recv())                  # => [2.25, None, 'junk', float]

    conn.send(52)
    conn.close()