# Preamble byte
PREAMBLE = 0b01010101

# Code for indicating that packet contains ACK
CODE_ACK = 0b00000001
# Code for indicating that packet contains data
CODE_DATA_INT = ord('i')
CODE_DATA_FLOAT = ord('f')

ADDR_GATEWAY = 0x01