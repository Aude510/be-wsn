from crc import Calculator, Crc8
import struct

# Packet structure
# Preamble | Code  |  Seq  | @dst  | @src  |  Data  |  CRC
#  1byte   | 1byte | 1byte | 1byte | 1byte | 4bytes | 1byte
class Encoder:
  def __init__(self, seq: int, dst: int, src: int, data, is_ack = False):
    calculator = Calculator(Crc8.CCITT)
    code = 0 if is_ack else ord('f') if type(data) == float else ord('i')
    self.data = bytearray(10 if code != 0 else 6)
    self.data[0] = 0
    self.data[1] = code
    self.data[2] = seq
    self.data[3] = dst
    self.data[4] = src
    if code != 0:
      self.data[5:9] = struct.pack(chr(code), data)
      self.data[9] = calculator.checksum(self.data[0:9])
    else:
      self.data[5] = calculator.checksum(self.data[0:5])

  def bytes(self):
    return self.data

packet = Encoder(0, 1, 2, 3.14)
print(packet.bytes().hex())

packet = Encoder(0, 1, 2, 0, True)
print(packet.bytes().hex())
  
  
#packet = Decoder(bytes.fromhex("0069010201db0f4940f7"))
#print('packet from', packet.src_addr(), 'to', packet.dst_addr(), 'with data', packet.value())
