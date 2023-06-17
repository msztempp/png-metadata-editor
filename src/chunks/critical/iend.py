from src.chunk import Chunk


class IEND(Chunk):
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)

    def details(self):
        self.print_basic_info()
        print('This is the last chunk in the file and should be empty.')
