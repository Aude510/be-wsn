import zmq

class SendLink:
  def __init__(self, port: str):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.PUB)
    self.socket.bind("tcp://*:%s" % port)

  def send(self, data: bytes):
    self.socket.send(data)
