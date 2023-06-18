from src.chunk import Chunk
from src.clear_terminal import clear_terminal


class PHYS(Chunk):
    UNIT_SPECIFIER_TYPES = {
        0: 'Relative dimensions',
        1: 'Metres'
    }

    def __init__(self, chunk_bytes):
        super().__init__(chunk_bytes)
        self.pixels_per_unit_x = None
        self.pixels_per_unit_y = None
        self.unit_specifier = None
        self.analyse()

    def analyse(self):
        if self.length != 9:
            raise Exception('pHYs chunk length is invalid')

        data = self.data
        self.pixels_per_unit_x = int.from_bytes(data[0:4], byteorder='big')
        self.pixels_per_unit_y = int.from_bytes(data[4:8], byteorder='big')
        self.unit_specifier = int.from_bytes(data[8:9], byteorder='big')

    def get_unit_specifier(self):
        return self.UNIT_SPECIFIER_TYPES[self.unit_specifier]

    def details(self):
        clear_terminal()
        self.print_basic_info()
        print('pHYs chunk info: ')
        print(' Pixels per unit, X-axis:', self.pixels_per_unit_x)
        print(' Pixels per unit, Y-axis:', self.pixels_per_unit_y)
        print(' Unit specifier:', self.get_unit_specifier())
        print()
