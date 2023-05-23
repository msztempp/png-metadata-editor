class Chunk:
    def __init__(self, length_array, type_array, data_array, crc_array, next_chunk_index):
        self.length_array = length_array
        self.type_array = type_array
        self.data_array = data_array
        self.crc_array = crc_array
        self.next_chunk_index = next_chunk_index

        self.calculate_next_chunk_index()

    def calculate_next_chunk_index(self):
        if bytearray(self.type_array).decode('utf-8') == 'IHEND':
            self.next_chunk_index = -1

        # calculate next chunk index
        # if next chunk index is -1, then there is no next chunk

    def get_next_chunk_index(self):
        return bytearray(self.length_array).decode('utf-8')

    def get_chunk_length(self):
        return len(self.data_array)

    def get_chunk_as_list(self):
        chunk_list = [self.length_array, self.type_array, self.data_array, self.crc_array]
        return bytearray(chunk_list)

    def read_chunk(self, start_index):
        chunk_iterator = start_index
        length_array = []
        type_array = []
        data_array = []
        crc_array = []

        length_byte = 0
        while length_byte < 4:
            length_array.append(self[chunk_iterator])
            chunk_iterator += 1
            length_byte += 1

        data_byte = 0
        while data_byte < 4:
            type_array.append(self[chunk_iterator])
            chunk_iterator += 1
            data_byte += 1

        crc_byte = 0
        while crc_byte < 4:
            crc_array.append(self[chunk_iterator])
            chunk_iterator += 1
            crc_byte += 1

        return Chunk(length_array, type_array, data_array, crc_array, chunk_iterator)
