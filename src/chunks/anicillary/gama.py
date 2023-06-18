from src.chunk import Chunk
from src.clear_terminal import clear_terminal


class GAMMA(Chunk):
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.gamma_value = None
        self.check_gamma()

    def check_gamma(self):
        self.gamma_value = int.from_bytes(self.data, byteorder='big') / 100000

    def details(self):
        clear_terminal()
        self.print_basic_info()
        print('gAMA chunk info: ')
        print(' Gamma value:', self.gamma_value)
        print()
