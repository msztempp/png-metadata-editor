from src.chunk import Chunk


def bytes_per_pixel(color_type):
    return {
        0: 2,
        2: 6,
        3: 1,
    }[color_type]


class TRNS(Chunk):
    def __init__(self, raw_bytes, color_type, bit_depth):
        super().__init__(raw_bytes)
        self.bit_depth = bit_depth
        self.transparency_data = None
        self.organise_data(color_type)

    def organise_data(self, color_type):
        byte_size = bytes_per_pixel(color_type)
        self.transparency_data = [int.from_bytes(self.data[i:i + byte_size], "big") for i in range(0, len(self.data), byte_size)]

    def details(self):
        self.print_basic_info()
        print("> TRANSPARENT PIXELS:\n  [ ID: VALUE ]\n  ------------")
        for i, pixel in enumerate(self.transparency_data, 1):
            if pixel != 255:
                print(f"  * {i}: {pixel}")
        print()
