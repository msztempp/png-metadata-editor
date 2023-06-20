class Chunk:
    def __init__(self, chunk_bytes=None, is_chunk_list=None):

        self.crc = None
        self.data = None
        self.chunk_type = None
        self.length = None
        self.raw_data = None

        if chunk_bytes and not is_chunk_list:
            self.single_chunk_init(chunk_bytes)
        elif not chunk_bytes and is_chunk_list:
            self.multiple_chunk_init(is_chunk_list)
        else:
            raise Exception('Invalid input')

    def single_chunk_init(self, chunk_bytes):
        self.length = int.from_bytes(chunk_bytes[:4], 'big')
        self.chunk_type = chunk_bytes[4:8].decode('utf-8')
        self.data = chunk_bytes[8:8 + self.length]
        self.crc = chunk_bytes[-4:]
        self.raw_data = chunk_bytes
        
    def multiple_chunk_init(self, chunk_list):
        self.length = [chunk.length for chunk in chunk_list]
        self.chunk_type = chunk_list[0].chunk_type
        self.data = [chunk.data for chunk in chunk_list]
        self.crc = [chunk.crc for chunk in chunk_list]
        self.raw_data = [chunk.raw_data for chunk in chunk_list]

    def is_critical(self):
        return self.chunk_type[0].isupper()

    def print_basic_info(self):
        print('Chunk info:')
        print('Type:', self.chunk_type)
        print('Length:', self.length, 'chunk_bytes')
        print('CRC:', self.crc)
        print('Is chunk critical:', self.is_critical())
        print()

    def details(self):
        print('To be implemented')
