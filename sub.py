import zmq

port = "5556"

# Socket to talk to server
context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:%s" % port)

socket.setsockopt_string(zmq.SUBSCRIBE, "")

while True:
  string = socket.recv_string()
  topic, messagedata = string.split()
  print(topic, '-', messagedata)
