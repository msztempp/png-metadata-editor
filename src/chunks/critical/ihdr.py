from chunk import Chunk


class IHDR(Chunk):
    FILTER_METHODS = {
        0: 'None',
        1: 'Sub',
        2: 'Up',
        3: 'Average',
        4: 'Paeth',
        'default': 'Not found'
    }

    def __init__(self, chunk_bytes):
        super().__init__(chunk_bytes)
        self.length = None
        self.data = None
        self.width = None
        self.height = None
        self.bit_depth = None
        self.color_type = None
        self.compression_method = None
        self.filter_method = None
        self.interlace_method = None
        self.analyse()

    def print_ihdr_info(self):
        print(f'Width: {self.width}')
        print(f'Height: {self.height}')
        print(f'Bit depth: {self.bit_depth}')
        print(f'Color type: {self.color_type}')
        print(f'Compression method: {self.compression_method} ')
        print(f'Filter method: {self.filter_method}')
        print(f'Interlace method: {self.interlace_method}')

    def analyse(self):
        if self.length != 13:
            raise ValueError('IHDR chunk length is invalid')
        self.width = int.from_bytes(self.data[:4], 'big')
        self.height = int.from_bytes(self.data[4:8], 'big')
        self.bit_depth = int.from_bytes(self.data[8:9], 'big')
        self.color_type = int.from_bytes(self.data[9:10], 'big')
        self.compression_method = int.from_bytes(self.data[10:11], 'big')
        self.filter_method = IHDR.FILTER_METHODS.get(int.from_bytes(self.data[11:12], 'big'), IHDR.FILTER_METHODS['default'])
        self.interlace_method = 'No interlace' if int.from_bytes(self.data[12:13], 'big') == 0 else 'Adam7 interlace'
