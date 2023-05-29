import os
from constants import *
from chunk import Chunk
from src.idat import IDAT
from src.ihdr import IHDR
from src.plte import PLTE


def format_size(size_bytes):
    if size_bytes < KILO:
        return f'{size_bytes} B'
    elif size_bytes < MEGA:
        kilo = size_bytes / KILO
        chunk_bytes = size_bytes % KILO
        return f'{kilo},{chunk_bytes} B'
    elif size_bytes < GIGA:
        mega = size_bytes // MEGA
        kilo = (size_bytes % MEGA) // KILO
        return f'{mega},{kilo} MB'


def get_name(pathname):
    file_name = os.path.basename(pathname)
    return os.path.splitext(file_name)[0]


class File:
    def __init__(self, pathname):
        self.chunks_indices = None
        self.size = None
        self.chunk_bytes = None
        self.name = None
        self.extension = 'PNG'
        self.chunks = {}
        self.name = get_name(pathname)
        self.load_data(pathname)
        self.find_chunks()
        self.init_chunks()
        if self.chunks['IHDR'].color_type == 3:
            self.chunks['IDAT'].apply_palette(self.chunks['PLTE'].palettes)

    def load_data(self, pathname):
        self.name = get_name(pathname)
        with open(pathname, 'rb') as png_file:
            self.chunk_bytes = png_file.read()
        self.size = len(self.chunk_bytes)

    def find_chunks(self):
        found_chunks = {'Critical': {}, 'Ancillary': {}}
        i = 0
        while i < len(self.chunk_bytes):
            chunk_type_bytes = self.chunk_bytes[i:i + 4]
            chunk_type = chunk_type_bytes.decode('utf-8')
            if chunk_type_bytes[0] in range(66, 90) and chunk_type in chunks_types:
                found_chunks['Critical'][chunk_type] = i
                i += 4
            elif chunk_type_bytes[0] in range(98, 122) and chunk_type in chunks_types:
                found_chunks['Ancillary'][chunk_type] = i
                i += 4
            else:
                i += 1
        self.chunks_indices = found_chunks

    def get_chunk_data(self, chunk_type, chunk_index):
        switcher = {
            'IHDR': lambda: IHDR(data_len, chunk_data, crc),
            'PLTE': lambda: PLTE(data_len, chunk_data, crc, self.chunks['IHDR'].color_type),
            'IDAT': lambda: IDAT(data_len, chunk_data, crc, self.chunks['IDAT'].width, self.chunks['IHDR'].height, self.chunks['IHDR'].color_type)
        }

        if chunk_type == 'IEND':
            self.chunks['IEND'] = Chunk(0, 'IEND', None)
        else:
            data_len = int.from_bytes(self.chunk_bytes[chunk_index - 4:chunk_index], 'big')
            chunk_data = self.chunk_bytes[chunk_index + 4:chunk_index + 4 + data_len]
            crc = self.chunk_bytes[chunk_index + 4 + data_len:chunk_index + 8 + data_len]

            self.chunks[chunk_type] = switcher.get(chunk_type, lambda: Chunk(data_len, chunk_data, crc))()

    def file_info(self):
        print('> NAME:', self.name)
        print('> EXTENSION:', self.extension)
        print('> SIZE: {formatted} ({bytes} bytes)'.format(formatted=format_size(self.size), bytes=self.size))
        print('> CHUNKS: ')
        for key, chunks in self.chunks_indices.items():
            print('  ', end='')
            print(' {} '.format(key).center(50, '-'))
            for chunk_type in chunks:
                print('  * {}'.format(chunk_type))
        print()

    def init_chunks(self):
        for key, chunks in self.chunks_indices.items():
            for chunk_type, chunk_index in chunks.items():
                self.get_chunk_data(chunk_type, chunk_index)

    def print_chunks(self):
        for chunk_type, chunk in self.chunks.items():
            chunk.print_info()
