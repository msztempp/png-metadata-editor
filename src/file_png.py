import os.path

from chunk import Chunk
from src.chunks.critical.ihdr import IHDR
from src.chunks.critical.plte import PLTE
from src.chunks.critical.idat import IDAT


class FilePNG:
    def __init__(self, pathname):
        self.chunks_indices = None
        self.byte_data = None
        self.name = None
        self.chunks = {}
        self.load_and_get_name(pathname)
        self.find_chunks()
        self.init_chunks()

    def load_and_get_name(self, pathname):
        pathname = pathname.lower()
        filename = os.path.basename(pathname)
        self.name = filename

        png_file = open(pathname, 'rb')
        self.byte_data = png_file.read()
        if not check_signature(self.byte_data):
            raise Exception('Incorrect file format\nThis program is strictly for analyzing PNG files.')
        png_file.close()

    ####### TODO: make it more efficient

    def find_chunks(self):
        found_chunks = {'critical': {}, 'ancillary': {}}
        i = 0
        while self.byte_data[i:i + 1]:
            if 65 < self.byte_data[i] < 90 and self.byte_data[i:i + 4] in chunks_types:
                chunk_type = self.byte_data[i:i + 4].decode('utf-8')
                if chunk_type in found_chunks['critical'].keys():
                    found_chunks['critical'][chunk_type].append(i - 4)
                else:
                    found_chunks['critical'][chunk_type] = [i - 4]
                i += 4
            elif 97 < self.byte_data[i] < 122 and self.byte_data[i:i + 4] in chunks_types:
                chunk_type = self.byte_data[i:i + 4].decode('utf-8')
                if chunk_type in found_chunks['ancillary'].keys():
                    found_chunks['ancillary'][chunk_type].append(i - 4)
                else:
                    found_chunks['ancillary'][chunk_type] = [i - 4]
                i += 4
            else:
                i += 1
        self.chunks_indices = found_chunks

    def get_chunk_data(self, index):
        start = index
        length = int.from_bytes(self.byte_data[start:start + 4], 'big')
        end = start + length + 12
        return self.byte_data[start:end]

    def get_chunks(self):
        for chunks_dict in self.chunks_indices.values():
            for chunk_type in chunks_dict.keys():
                for instance_index in chunks_dict[chunk_type]:
                    if chunk_type in self.chunks.keys():
                        if type(self.chunks[chunk_type]) != list:
                            self.chunks[chunk_type] = [self.chunks[chunk_type]]
                        self.chunks[chunk_type].append(self.get_chunk_data(instance_index))
                    else:
                        self.chunks[chunk_type] = self.get_chunk_data(instance_index)

    def init_chunks(self):
        self.get_chunks()  # Initialize self.chunks with raw_bytes

        for chunk_type, chunk_value in self.chunks.items():
            if chunk_type == 'IHDR':
                self.chunks[chunk_type] = IHDR(chunk_value)
            elif chunk_type == 'PLTE':
                self.chunks[chunk_type] = PLTE(chunk_value, self.chunks['IHDR'].color_type)
            elif chunk_type == 'IDAT':
                if isinstance(chunk_value, list):
                    chunk_list = [Chunk(chunk) for chunk in chunk_value]
                    self.chunks[chunk_type] = IDAT(chunk_list, self.chunks['IHDR'].width,
                                                   self.chunks['IHDR'].height, self.chunks['IHDR'].color_type)
                else:
                    self.chunks[chunk_type] = IDAT(chunk_value, self.chunks['IHDR'].width,
                                                   self.chunks['IHDR'].height, self.chunks['IHDR'].color_type)
            else:
                if isinstance(chunk_value, list):
                    chunk_list = [Chunk(chunk) for chunk in chunk_value]
                    self.chunks[chunk_type] = Chunk(is_chunk_list=chunk_list)
                else:
                    self.chunks[chunk_type] = Chunk(chunk_value)

    def print_chunks(self):
        for chunk in self.chunks.values():
            chunk.print_basic_info()

    def print_to_file(self):
        folder_path = '../img-anonymized'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        new_name = os.path.join(folder_path, '{}_anonymized.png'.format(self.name))
        tmp_png = open(new_name, 'wb')
        tmp_png.write(self.byte_data[:8])
        for chunk_type in self.chunks_indices['critical'].values():
            for instance_index in chunk_type:
                chunk_data = self.get_chunk_data(instance_index)
                tmp_png.write(chunk_data)
        print('Saved only with critical chunks to: ', new_name)
        tmp_png.close()

    def perform_fft(self):
        pass


# https://www.w3.org/TR/png/#5PNG-file-signature
# The first eight bytes of a PNG datastream always contain the following (decimal) values:
def check_signature(chunk_byte):
    signature = [137, 80, 78, 71, 13, 10, 26, 10]  # PNG signature

    for i, byte in enumerate(signature):
        if chunk_byte[i] != byte:
            return False
    return True


chunks_types = [b'IHDR', b'PLTE', b'IDAT', b'IEND',
                b'cHRM', b'gAMA', b'iCCP', b'sBIT', b'sRGB', b'bKGD', b'hIST', b'tRNS', 'pHYs',
                b'sPLT', b'tIME', b'iTXt', b'tEXt', b'zTXt']
