import threading
import zmq_links
import queue
import decoder
import encoder
import constantsMAC

buffer_receive = queue.Queue()
mutex_buff_rcv = threading.Condition()
sequence = {}

def init_threads():
    threading.Thread(target=thread_reception).start()
    threading.Thread(target=thread_decode).start()

def thread_reception():
    rcv_link = zmq_links.RecvLink()
    while True:
        msg = rcv_link.receive()
        if len(msg) > 0:
            mutex_buff_rcv.acquire()
            buffer_receive.put(msg)
            mutex_buff_rcv.release()

def thread_decode():
    while True:
        send_link = zmq_links.SendLink()
        mutex_buff_rcv.acquire()
        if(not(buffer_receive.empty())):
            packet = decoder.Decoder(buffer_receive.get())
            if(not(packet.src_addr() in sequence.keys())):
                sequence[packet.src_addr()] = 0
            if(packet.dst_addr() != constantsMAC.ADDR_GATEWAY):
                mutex_buff_rcv.release()
                continue
            if(sequence[packet.src_addr()]==packet.seq()):
                sequence[packet.src_addr()]+=1
                pass
                ## TODO : faire un call API
            elif(packet.dst_addr== constantsMAC.ADDR_GATEWAY and sequence[packet.src_addr()]<packet.seq()):
                sequence[packet.src_addr()] = packet.seq()
                ## TODO faire aussi un call API
            ack = encoder.Encoder(packet.seq(),packet.src_addr(),packet.dst_addr(),None,True)
            send_link.send(ack)                
        mutex_buff_rcv.release()




if __name__ == "__main__":
    init_threads()
