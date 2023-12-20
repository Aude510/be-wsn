from crc import Calculator, Crc8
import struct

# Packet structure
# Preamble | Code  |  Seq  | @dst  | @src  |  Data  |  CRC
#  1byte   | 1byte | 1byte | 1byte | 1byte | 4bytes | 1byte
class Decoder:
  def __init__(self, data: bytes):
    self.data = data
    calculator = Calculator(Crc8.CCITT)
    if data[1] != 0:
      assert calculator.checksum(data[0:9]) == data[9]
    else:
      assert calculator.checksum(data[0:5]) == data[5]

  def is_ack(self):
    return self.data[1] == 0

  def dst_addr(self):
    return self.data[3]

  def src_addr(self):
    return self.data[4]
  
  def seq(self):
    return self.data[2]
  
  def value(self):
    code = chr(self.data[1])
    if code != 0:
      value = self.data[5:9]
      return struct.unpack(code, value)[0]

# packet = Decoder(bytes.fromhex("0066000102c3f548403d"))
# print('packet from', packet.src_addr(), 'to', packet.dst_addr(), 'with data', packet.value())
