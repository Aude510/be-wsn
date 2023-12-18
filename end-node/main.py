import threading
import zmq_links
import queue
import constantsMAC
import encoder
import decoder

buffer_send = queue.Queue()
mutex_buff_send = threading.Condition()
seq = 0
addr_node = 0x02
def init_threads():
    threading.Thread(target=thread_send).start()
    threading.Thread(target=thread_add_data).start()

def thread_send():
    send_link = zmq_links.SendLink()
    rcv_link = zmq_links.RecvLink()
    while True:
        ##TODO timer et resend
        mutex_buff_send.acquire()
        data = buffer_send.get()
        mutex_buff_send.release()
        send_link.send(data)
        ack_received = False
        while not(ack_received):    
            packet = rcv_link.receive() ##TODO tester si packet est vide ou pas
            if(packet != None):
                ack = decoder.Decoder(packet)
                if(ack.dst_addr != addr_node):
                    continue
                if(ack.is_ack() and ack.seq() == seq):
                    seq = seq + 1
                    ack_received = True





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
        packet = encoder.Encoder(seq,constantsMAC.ADDR_GATEWAY,0x01,data)
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
    addr_node = input("Quelle est l'adresse du device ?")
    init_threads()