import sys

sys.path.append('../')

import threading
import zmq_links
import queue
import decoder
import encoder
import constantsMAC
import requests

buffer_receive = queue.Queue()
mutex_buff_rcv = threading.Condition()
sequence = {}

def init_threads():
    threading.Thread(target=thread_reception).start()
    threading.Thread(target=thread_decode).start()

def thread_reception():
    rcv_link = zmq_links.RecvLink("5557")
    while True:
        msg = rcv_link.receive()
        if len(msg) > 0:
            mutex_buff_rcv.acquire()
            buffer_receive.put(msg)
            mutex_buff_rcv.release()

def thread_decode():
    send_link = zmq_links.SendLink("5558")
    while True:
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
                if(packet.code() == constantsMAC.CODE_DATA_INT):
                    requests.post('https://api.is-grandma-alive.obrulez.fr/mamie-debout',json={"debout":str(packet.value())})
                    print("Call API mamie-debout, value : " + str(packet.value()))
                elif(packet.code() == constantsMAC.CODE_DATA_FLOAT):
                    requests.post('https://api.is-grandma-alive.obrulez.fr/mamie-asphyxie',json={"asphyxie":str(packet.value())})
                    print("Call API mamie-asphyxie, value : " + str(packet.value()))
                else:
                    print("Code received not recognized")
            elif(packet.dst_addr == constantsMAC.ADDR_GATEWAY and sequence[packet.src_addr()]<packet.seq()):
                sequence[packet.src_addr()] = packet.seq()
                print("Numéro de séquence de futur")
                print("La valeur dans le paquet est : " + str(packet.value()))
                if(packet.code() == constantsMAC.CODE_DATA_INT):
                    requests.post('https://api.is-grandma-alive.obrulez.fr/mamie-debout',json={"debout":str(packet.value())})
                    print("Call API mamie-debout, value : " + str(packet.value()))
                elif(packet.code() == constantsMAC.CODE_DATA_FLOAT):
                    requests.post('https://api.is-grandma-alive.obrulez.fr/mamie-asphyxie',json={"asphyxie":str(packet.value())})
                    print("Call API mamie-asphyxie, value : " + str(packet.value()))
                else:
                    print("Code received not recognized")
            ack = encoder.Encoder(packet.seq(), packet.src_addr(), packet.dst_addr(), None, True).bytes()
            dec_ack = decoder.Decoder(ack)
            send_link.send(ack)                
        mutex_buff_rcv.release()




if __name__ == "__main__":
    init_threads()
