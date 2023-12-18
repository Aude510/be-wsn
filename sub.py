import zmq

class RecvLink:
  def __init__(self, port: str, timeout: int = 0):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.SUB)
    self.socket.setsockopt_string(zmq.SUBSCRIBE, "")
    if timeout > 0:
      self.socket.setsockopt(zmq.RCVTIMEO, timeout)
    self.socket.connect("tcp://localhost:%s" % port)

  def receive(self):
    try:
      packet = self.socket.recv()
    except:
      packet = None
    return packet
