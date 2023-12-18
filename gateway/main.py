import threading
import pub
import sub
import queue

buffer_receive = queue.Queue()
mutex_buff_rcv = threading.Condition()

def init_threads():
    threading.Thread(target=thread_reception).start()
    threading.Thread(target=thread_decode).start()

def thread_reception():
    rcv_link = sub.RecvLink()
    while True:
        msg = rcv_link.receive()
        if len(msg) > 0:
            mutex_buff_rcv.acquire()
            buffer_receive.put(msg)
            mutex_buff_rcv.release()

def thread_decode():
    while True:
        mutex_buff_rcv.acquire()
        if(not(buffer_receive.empty())):
            msg = buffer_receive.get()
        mutex_buff_rcv.release()




if __name__ == "__main__":
    init_threads()
