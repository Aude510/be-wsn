import sys

sys.path.append('../')

import threading
import zmq_links
import queue
import decoder
import encoder
import constantsMAC

buffer_send = queue.Queue()
mutex_buff_send = threading.Condition()
addr_node = 0x02


def init_threads():
    threading.Thread(target=thread_send).start()
    threading.Thread(target=thread_add_data).start()

def thread_send():
    seq = 0
    max_retransmit = 15
    send_link = zmq_links.SendLink("5557")
    rcv_link = zmq_links.RecvLink("5558")
    while True:
        ##TODO timer et resend
        data = None
        mutex_buff_send.acquire()
        if not buffer_send.empty():
          data = buffer_send.get()
        mutex_buff_send.release()
        if data is None:
          continue
        sendPacket = encoder.Encoder(seq, constantsMAC.ADDR_GATEWAY, addr_node, data)
        send_link.send(sendPacket.bytes())
        ack_received = False
        nb_retransmit = 0
        while not ack_received or nb_retransmit < max_retransmit:    
            packet = rcv_link.receive() ##TODO tester si packet est vide ou pas
            if(packet != None):
                ack = decoder.Decoder(packet)
                if(ack.dst_addr() != addr_node):
                    nb_retransmit+=1
                    continue
                if(ack.is_ack() and ack.seq() == seq):
                    seq += 1
                    ack_received = True
                nb_retransmit += 1


def thread_add_data():
    while True:
        msg = input("Data to send ? ")
        if(isInt(msg)):
           data = int(msg)
        elif(isFloat(msg)):
           data = float(msg)
        else:
           print("Error invalid type: please enter int or float")
           continue
        mutex_buff_send.acquire()
        buffer_send.put(data)
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
    addr_node = int(input("Quelle est l'adresse du device ? "))
    init_threads()
