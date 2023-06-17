from src.chunk import Chunk


class IHDR(Chunk):
    FILTER_METHODS = {
        0: 'None',  # No filter
        1: 'Sub',  # filter that uses the value of the pixel on the left
        2: 'Up',  # filter that uses the value of the pixel above
        3: 'Average',  # filter that uses the average of the pixel on the left and the pixel above,
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
        self.width = int.from_bytes(data[0:4], byteorder='big')  # width of image in pixels
        self.height = int.from_bytes(data[4:8], byteorder='big')  # height of image in pixels
        self.bit_depth = int.from_bytes(data[8:9], byteorder='big')  # number of bits per sample
        self.color_type = int.from_bytes(data[9:10], byteorder='big')  # color type
        self.compression_method = int.from_bytes(data[10:11], byteorder='big')  # compression method
        filter_method_code = int.from_bytes(data[11:12], byteorder='big')
        self.filter_method = IHDR.FILTER_METHODS.get(filter_method_code)
        self.interlace_method = 'No interlace' if int.from_bytes(data[12:13], byteorder='big') == 0 else 'Adam7 interlace'
        # With interlace method 0, the null method, pixels are extracted sequentially from left to right, and scanlines sequentially from top to bottom.
        # The interlaced PNG image is a single reduced image.
        # Interlace method 1, known as Adam7, defines seven distinct passes over the image. Each pass transmits a subset of the pixels in the reference image.
        # The pass in which each pixel is transmitted (numbered from 1 to 7) is defined
        # by replicating the following 8-by-8 pattern over the entire image, starting in the upper left corner:
