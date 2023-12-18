import zmq

class RecvLink:
  def __init__(self, port):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.SUB)
    self.socket.connect("tcp://localhost:%s" % port)

  def receive(self):
    string = self.socket.recv_string()
    return string.split()
