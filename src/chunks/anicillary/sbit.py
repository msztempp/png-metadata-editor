from src.chunk import Chunk
from src.clear_terminal import clear_terminal


class SBIT(Chunk):
    COLOR_TYPES = {
        0: 'Greyscale',
        2: 'True_colour',
        3: 'Indexed-colour',
        4: 'Greyscale with alpha',
        6: 'True_colour with alpha'
    }

    def __init__(self, raw_chunk_bytes, color_type, sample_depth):
        super().__init__(raw_chunk_bytes)
        self.color_type = color_type
        self.sample_depth = sample_depth
        self.significant_bits = None
        self.analyse()

    def analyse(self):
        if self.length != self.get_required_length():
            raise Exception('sBIT chunk length is invalid')

        data = self.data
        if self.color_type == 0:
            self.significant_bits = int.from_bytes(data[0:1], byteorder='big')
        elif self.color_type == 2:
            self.significant_bits = [
                int.from_bytes(data[i:i + 1], byteorder='big') for i in range(0, 3)
            ]
        elif self.color_type == 3:
            self.significant_bits = [
                int.from_bytes(data[i:i + 1], byteorder='big') for i in range(0, 2)
            ]
        elif self.color_type == 4:
            self.significant_bits = int.from_bytes(data[0:1], byteorder='big')
        elif self.color_type == 6:
            self.significant_bits = [
                int.from_bytes(data[i:i + 1], byteorder='big') for i in range(0, 4)
            ]

    def get_required_length(self):
        if self.color_type in [0, 4]:
            return 1
        elif self.color_type in [2, 3]:
            return 3
        elif self.color_type == 6:
            return 4

    def details(self):
        clear_terminal()
        self.print_basic_info()
        print('sBIT chunk info: ')
        print(' Color type:', SBIT.COLOR_TYPES.get(self.color_type))
        print(' Sample depth:', self.sample_depth)
        if self.color_type == 0:
            print(' Significant greyscale bits:', self.significant_bits)
        elif self.color_type == 2:
            print(' Significant red bits:', self.significant_bits[0])
            print(' Significant green bits:', self.significant_bits[1])
            print(' Significant blue bits:', self.significant_bits[2])
        elif self.color_type == 3:
            print(' Significant greyscale bits:', self.significant_bits[0])
            print(' Significant alpha bits:', self.significant_bits[1])
        elif self.color_type == 4:
            print(' Significant greyscale bits:', self.significant_bits)
        elif self.color_type == 6:
            print(' Significant red bits:', self.significant_bits[0])
            print(' Significant green bits:', self.significant_bits[1])
            print(' Significant blue bits:', self.significant_bits[2])
            print(' Significant alpha bits:', self.significant_bits[3])
