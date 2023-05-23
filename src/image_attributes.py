class PNGImageAttributes:
    # https://en.wikipedia.org/wiki/PNG
    # width (4 bytes)
    # height (4 bytes)
    # bit depth (1 byte, values 1, 2, 4, 8, or 16)
    # color type (1 byte, values 0, 2, 3, 4, or 6)
    # compression method (1 byte, value 0)
    # filter method (1 byte, value 0)
    # interlace method (1 byte, values 0 "no interlace" or 1 "Adam7 interlace") (13 data bytes total).

    def __init__(self, width, height, bit_depth, color_type, compression_method, filter_method, interlace_method):
        self.width = width
        self.height = height
        self.bit_depth = bit_depth
        self.color_type = color_type
        self.compression_method = compression_method
        self.filter_method = filter_method
        self.interlace_method = interlace_method

    def display_info(self):
        print(f"Width: {self.width}")
        print(f"Height: {self.height}")
        print(f"Bit depth: {self.bit_depth}")
        print(f"Color type: {self.color_type}")
        print(f"Compression method: {self.compression_method}")
        print(f"Filter method: {self.filter_method}")
        print(f"Interlace method: {self.interlace_method}")
