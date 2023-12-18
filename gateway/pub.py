import zmq

class SendLink:
  def __init__(self, port):
    self.context = zmq.Context()
    self.socket = self.context.socket(zmq.PUB)
    self.socket.bind("tcp://*:%s" % port)

  def send(self, topic, data):
    self.socket.send_string("%d %d" % (topic, data))
