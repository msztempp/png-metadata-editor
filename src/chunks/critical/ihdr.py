from src.chunk import Chunk
from src.clear_terminal import clear_terminal


class IHDR(Chunk):
    FILTER_METHODS = {
        0: 'None',  # No filter
        1: 'Sub',  # filter that uses the value of the pixel on the left
        2: 'Up',  # filter that uses the value of the pixel above
        3: 'Average',  # filter that uses the average of the pixel on the left and the pixel above
        4: 'Paeth',  # filter that uses a linear function of the pixel to the left and the pixel above
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
        clear_terminal()
        self.print_basic_info()
        print('IHDR chunk info:')
        print(' Width:', self.width)
        print(' Height:', self.height)
        print(' Bit depth:', self.bit_depth)
        print(' Color type:', self.color_type)
        print(' Compression method:', self.compression_method)
        print(' Filter method:', self.filter_method)
        print(' Interlace method:', self.interlace_method)
        print()

    def analyse_header(self):
        if self.length is not 13:
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
