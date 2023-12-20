from zmq_links import SendLink, RecvLink
from encoder import Encoder
from decoder import Decoder
import time

link1 = SendLink("5557")
link2 = RecvLink("5558", 2000)

i = 0
while True:
  packet1 = Encoder(i, 1, 2, i+1)
  link1.send(packet1.bytes())
  print('SENT', packet1.bytes().hex())
  res = link2.receive()
  if res != None:
    packet2 = Decoder(res)
    if packet2.is_ack():
      print('ACK')
      i += 1
  time.sleep(1)
