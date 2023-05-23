class Chunk:
    def __init__(self, length, chunk_type, data, crc, next_index):
        self.length = length
        self.chunk_type = chunk_type
        self.data = data
        self.crc = crc
        self.next_index = next_index

        self.calculate_next_chunk_index()

    # check the last chunk type to see if it is IHEND
    def calculate_next_chunk_index(self):
        if bytearray(self.chunk_type).decode('utf-8') == 'IHEND':
            self.next_index = -1

        # calculate next chunk index
        # if next chunk index is -1, then there is no next chunk

    def get_next_chunk_index(self):
        return bytearray(self.length).decode('utf-8')

    def get_chunk_length(self):
        return len(self.length)

    def get_chunk_as_list(self):
        chunk_list = [self.length, self.chunk_type, self.data, self.crc]
        return bytearray(chunk_list)


def read_chunk(self, start_index):
    chunk_iterator = start_index
    length = [self[chunk_iterator + i] for i in range(4)]
    chunk_iterator += 4
    chunk_type = [self[chunk_iterator + i] for i in range(4)]
    chunk_iterator += 4
    data = [self[chunk_iterator + i] for i in range(4)]
    chunk_iterator += 4
    crc = [self[chunk_iterator + i] for i in range(4)]
    chunk_iterator += 4

    return Chunk(length, chunk_type, data, crc, chunk_iterator)
