from src.chunk import Chunk


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
        self.interlace_method = None
        self.filter_method = None
        self.compression_method = None
        self.color_type = None
        self.bit_depth = None
        self.height = None
        self.width = None
        self.analyse_header()

    def details(self):
        self.print_basic_info()
        print(f'Width: {self.width}')
        print(f'Height: {self.height}')
        print(f'Bit depth: {self.bit_depth}')
        print(f'Color type: {self.color_type}')
        print(f'Compression method: {self.compression_method} ')
        print(f'Filter method: {self.filter_method}')
        print(f'Interlace method: {self.interlace_method}\n')

    def analyse_header(self):
        if self.length != 13:
            raise Exception('IHDR chunk length is invalid')

        data = self.data
        self.width = int.from_bytes(data[0:4], byteorder='big')
        self.height = int.from_bytes(data[4:8], byteorder='big')
        self.bit_depth = int.from_bytes(data[8:9], byteorder='big')
        self.color_type = int.from_bytes(data[9:10], byteorder='big')
        self.compression_method = int.from_bytes(data[10:11], byteorder='big')
        filter_method_code = int.from_bytes(data[11:12], byteorder='big')
        self.filter_method = IHDR.FILTER_METHODS.get(filter_method_code)
        self.interlace_method = 'No interlace' if int.from_bytes(data[12:13], byteorder='big') == 0 else 'Adam7 interlace'
