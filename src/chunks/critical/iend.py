from src.chunk import Chunk
from src.clear_terminal import clear_terminal


class IEND(Chunk):
    def __init__(self,  raw_chunk_bytes):
        super().__init__(raw_chunk_bytes)

    def details(self):
        clear_terminal()
        self.print_basic_info()
        print('IEND chunk info:')
        print('This is the last chunk in the file and should be empty.')
        print()
