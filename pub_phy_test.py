from gateway.pub import SendLink
import time

link = SendLink("5556")

while True:
  link.send(b'hello')
  time.sleep(1)
