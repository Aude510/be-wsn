import threading
import pub
import sub
import queue

buffer_send = queue.Queue()
mutex_buff_send = threading.Condition()

def init_threads():
    threading.Thread(target=thread_receive).start()
    threading.Thread(target=thread_send).start()
    threading.Thread(target=thread_add_data).start()

def thread_receive():
    rcv_link = sub.RecvLink()

def thread_send():
    send_link = pub.SendLink()
    while True:
        ##TODO timer et resend
        mutex_buff_send.acquire()
        send_link.send()
        mutex_buff_send.release()


def thread_add_data():
    while True:
        msg = input("Data to send ?")
        mutex_buff_send.acquire()
        if(isFloat(msg)):
            ##encode int data and put in buffer
            data = float(msg)
        elif(isInt(msg)):
            ## encode float data and put in buffer
            data = int(msg)
        else:
            print("Error invalid type: please enter int or float")
        mutex_buff_send.release()
    

def isFloat(msg):
    try:
        float(msg)
        return True
    except:
        return False

def isInt(msg):
    try:
        int(msg)
        return True
    except:
        return False
    
if __name__ == "__main__":
    init_threads()