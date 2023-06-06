from src.chunk import Chunk


class TRNS(Chunk):
    def __init__(self, raw_bytes, color_type, bit_depth):
        super().__init__(raw_bytes)
        self.organise_data(color_type)

    def organise_data(self, color_type):
        pass
