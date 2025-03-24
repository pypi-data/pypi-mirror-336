# jas/bitstream.py

class BitWriter:
    def __init__(self):
        self.bits = ""

    def write_bits(self, bit_str):
        self.bits += bit_str

    def get_bytes(self):
        padding = (8 - len(self.bits) % 8) % 8
        self.bits += "0" * padding
        byte_array = bytearray()
        for i in range(0, len(self.bits), 8):
            byte = self.bits[i:i+8]
            byte_array.append(int(byte, 2))
        return bytes([padding]) + bytes(byte_array)  # Store padding as first byte


class BitReader:
    def __init__(self, data):
        self.padding = data[0]
        self.bits = "".join(f"{byte:08b}" for byte in data[1:])
        if self.padding:
            self.bits = self.bits[:-self.padding]
        self.index = 0

    def read_bit(self):
        if self.index >= len(self.bits):
            return ""
        bit = self.bits[self.index]
        self.index += 1
        return bit

    def is_end(self):
        return self.index >= len(self.bits)