from src.chunk import Chunk
from src.clear_terminal import clear_terminal


class TRNS(Chunk):
    def __init__(self, chunk_bytes, color_type, entries):
        super().__init__(chunk_bytes)
        self.alpha_index = []
        if color_type == 0:
            self.grey_sample = None
        elif color_type == 2:
            self.red_sample = None
            self.green_sample = None
            self.blue_sample = None
        elif color_type == 3:
            for i in range(0, entries):
                self.alpha_index.append(None)
        self.color_type = color_type
        self.entries = entries
        self.analyse()

    def analyse(self):
        if self.color_type == 0 and self.length != 2:
            raise Exception('tRNS chunk length is invalid')
        elif self.color_type == 2 and self.length != 6:
            raise Exception('tRNS chunk length is invalid')
        elif self.color_type == 3 and self.length > self.entries:
            raise Exception('tRNS chunk length is invalid')

        data = self.data
        if self.color_type == 0:
            self.grey_sample = int.from_bytes(data[0:2], byteorder='big')
        elif self.color_type == 2:
            self.red_sample = int.from_bytes(data[0:2], byteorder='big')
            self.green_sample = int.from_bytes(data[2:6], byteorder='big')
            self.blue_sample = int.from_bytes(data[4:6], byteorder='big')
        elif self.color_type == 3:
            if self.entries < self.length:
                for i in range(self.entries, self.length):
                    self.alpha_index[i] = 255
            for i in range(0, self.entries):
                self.alpha_index[i] = int.from_bytes(data[i:i + 1], byteorder='big')

    def details(self):
        clear_terminal()
        self.print_basic_info()
        print('tRNS chunk info: ')
        if self.color_type == 0:
            print(' Grey sample value:', self.grey_sample)
        elif self.color_type == 2:
            print(' Red sample value:', self.red_sample)
            print(' Green sample value:', self.green_sample)
            print(' Blue sample value:', self.blue_sample)
        elif self.color_type == 3:
            for i in range(0, self.length):
                print(' Alpha for palette index', i, ':', self.alpha_index[i])
