import threading
import pub
import sub
import queue
import Encapsulator
import constantsMAC
import encoder

buffer_send = queue.Queue()
mutex_buff_send = threading.Condition()

def init_threads():
    threading.Thread(target=thread_send).start()
    threading.Thread(target=thread_add_data).start()

def thread_send():
    send_link = pub.SendLink()
    rcv_link = sub.RecvLink()
    while True:
        ##TODO timer et resend
        ack_received = False
        while ack_received:    
            mutex_buff_send.acquire()
            data = buffer_send.get()
            mutex_buff_send.release()
            send_link.send(data)
            packet = rcv_link.receive() ##TODO tester si packet est vide ou pas




def thread_add_data():
    
    while True:
        msg = input("Data to send ?")
        mutex_buff_send.acquire()
        if(isFloat(msg)):
            data = float(msg)
        elif(isInt(msg)):
            data = int(msg)
        else:
            print("Error invalid type: please enter int or float")
            continue
        packet = encoder.Encoder(0,constantsMAC.ADDR_GATEWAY,0x01,data)
        buffer_send.put(packet.bytes())
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