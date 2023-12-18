import zmq

class RecvLink:
  def __init__(self, port):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.SUB)
    self.socket.setsockopt(zmq.RCVTIMEO,1000)
    self.socket.connect("tcp://localhost:%s" % port)

  def receive(self):
    packet = self.socket.recv()
    return packet
