from crc import Calculator, Crc8
from constantsMAC import *

class Encapsulator:

  def __init__(self, addr_src):
    # Sequence number
    self.sequence = 0x00
    # Calculator for computing CRC
    self.calculator = Calculator(Crc8.CCITT, optimized=True)
    # MAC address of device (source)
    self.addr_src = addr_src
    
  def encapsulate(self, addr_dst, code, data = 0, sequence = -1):
    '''
    Returns an encapsulated message.

            Parameters:

                    addr_dst (byte):      The address of the device that must receive the message.
                    code (byte): Indicate the type of data sent(CODE_ACK, CODE_DATA_INT, CODE_DATA_FLOAT).
                    data (int/float): Data to be transmitted.
                    sequence (byte): Optional sequence number, used by gateways to send ACKs.
                    
            Returns:
                    msg (str): Packet to be transmitted (ACK or data).
    '''
    msg = ""
    # Preamble
    msg += chr(PREAMBLE)
    # Code
    msg += chr(code)
    # Sequence
    if sequence == -1:
      msg += chr(self.sequence)
    else:
      msg += chr(sequence)
    # Destination Address
    msg += chr(addr_dst)
    # Source Address
    msg += chr(self.addr_src)

    if code != CODE_ACK:
      # Message
      for c in [(data >> i & 0xff) for i in (24,16,8,0)]:
        msg += chr(c)
    # CRC
    msg += chr(self.calculator.checksum(bytes(msg[1:], 'utf-8')))
    return msg
  
  def incr_sequence(self):
    self.sequence += 1

if __name__ == "__main__":
  e = Encapsulator(0xBB)
  s = e.encapsulate(0xAB, CODE_DATA_INT, 0x12345678)
  for c in s:
    print(hex(ord(c)))