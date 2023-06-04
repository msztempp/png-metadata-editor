from src.chunk import Chunk


def bytes_per_pixel(color_type):
    switcher = {
        0: 2,
        2: 6,
        3: 1,
    }
    return switcher[color_type]


class TRNS(Chunk):
    def __init__(self, raw_bytes, color_type, bit_depth):
        super().__init__(raw_bytes)
        self.transparency_data = None
        self.organise_data(color_type)

    def organise_data(self, color_type):
        self.transparency_data = [self.data[i:i + bytes_per_pixel(color_type)] for i in range(0, len(self.data), bytes_per_pixel(color_type))]
        self.transparency_data = [int.from_bytes(pixel, "big") for pixel in self.transparency_data]

    def details(self):
        self.basic_info()
        print("> TRANSPARENT PIXELS:\n  [ ID: VALUE ]\n  ------------")
        for i, pixel in enumerate(self.transparency_data, 1):
            if pixel != 255: print("  * {id}: {value}".format(id=i, value=pixel))
        print()
