import os

from constants import *
from chunk import Chunk
from ihdr import IHDR
from plte import PLTE
from idat import IDAT
from signature import check_signature


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


class File:
    def __init__(self, pathname):
        self.file_name = None
        self.chunk_type = None
        self.size = None
        self.byte_data = None
        self.chunks_indices = None
        self.chunks = {}
        self.get_name(pathname)
        self.load_data(pathname)
        self.find_chunks()
        self.init_chunks()
        if self.chunks["IHDR"].color_type == 3:
            self.chunks["IDAT"].apply_palette(self.chunks["PLTE"].palettes)

    def get_name(self, pathname):
        self.file_name = os.path.basename(pathname)

    def load_data(self, pathname):
        png_file = open(pathname, "rb")
        self.byte_data = png_file.read()
        if check_signature(self.byte_data):
            print(f'{self.file_name} loaded correctly\n')
        else:
            print(f'{self.file_name} is not a png file!')
            exit()
        self.size = len(self.byte_data)
        png_file.close()

    def print_info(self):
        print('File info:')
        print("name:", self.file_name)
        print("size: {formatted} ({bytes} bytes)".format(formatted=format_size(self.size), bytes=self.size))
        print("chunks:")
        for key in self.chunks_indices.keys():
            for chunk in self.chunks_indices[key].keys():
                print("  * {}".format(chunk))

    # TODO - write this better

    def find_chunks(self):
        found_chunks = {"CRITICAL": {}, "ANCILLARY": {}}
        i = 0
        while self.byte_data[i:i + 1]:
            if 65 < self.byte_data[i] < 90 and self.byte_data[i:i + 4] in chunks_types:
                chunk_type = self.byte_data[i:i + 4].decode("utf-8")
                found_chunks["CRITICAL"][chunk_type] = i
                i += 4
            elif 97 < self.byte_data[i] < 122 and self.byte_data[i:i + 4] in chunks_types:
                chunk_type = self.byte_data[i:i + 4].decode("utf-8")
                found_chunks["ANCILLARY"][chunk_type] = i
                i += 4
            else:
                i += 1
        self.chunks_indices = found_chunks

    # def find_chunks(self):
    #     found_chunks = {"CRITICAL": {}, "ANCILLARY": {}}
    #     i = 0
    #     while i < len(self.byte_data):
    #         chunk_type = self.byte_data[i:i + 4].decode("utf-8")
    #         if chunk_type in chunks_types:
    #             if 65 < self.byte_data[i] < 90:
    #                 found_chunks["CRITICAL"][chunk_type] = i
    #             elif 97 < self.byte_data[i] < 122:
    #                 found_chunks["ANCILLARY"][chunk_type] = i
    #             i += 4
    #         else:
    #             i += 1
    #     self.chunks_indices = found_chunks

    def get_chunk_data(self, chunk_type, index):
        if chunk_type == "IEND":
            self.chunks["IEND"] = Chunk(0, "IEND", None)
        else:
            length = int.from_bytes(self.byte_data[index - 4:index], "big")
            index += 4
            data = self.byte_data[index:index + length]
            index += length
            crc = self.byte_data[index:index + 4]
            if chunk_type == "IHDR": 
                self.chunks[chunk_type] = IHDR(length, data, crc)
            elif chunk_type == "PLTE":
                self.chunks[chunk_type] = PLTE(length, data, crc, self.chunks["IHDR"].color_type)
            elif chunk_type == "IDAT":
                self.chunks[chunk_type] = IDAT(length, data, crc, self.chunks["IHDR"].width, self.chunks["IHDR"].height, self.chunks["IHDR"].color_type)
            else:
                self.chunks[chunk_type] = Chunk(length, chunk_type, crc)

    # Write this better TODO

    # def get_chunk_data(self, chunk_type, index):
    #     if chunk_type == "IEND":
    #         self.chunks["IEND"] = Chunk(0, "IEND", None)
    #     else:
    #         length = int.from_bytes(self.byte_data[index - 4:index], "big")
    #         index += 4
    #         data = self.byte_data[index:index + length]
    #         index += length
    #         crc = self.byte_data[index:index + 4]
    #         switcher = {
    #             "IHDR": IHDR(length, data, crc),
    #             "PLTE": PLTE(length, data, crc, self.chunks["IHDR"].color_type),
    #             "IDAT": IDAT(length, data, crc, self.chunks["IHDR"].width, self.chunks["IHDR"].height, self.chunks["IHDR"].color_type)
    #         }
    #         self.chunks[chunk_type] = switcher.get(chunk_type, Chunk(length, chunk_type, crc))

    def init_chunks(self):
        for key, chunks in self.chunks_indices.items():
            for chunk_type, chunk_index in chunks.items():
                self.get_chunk_data(chunk_type, chunk_index)

    def print_chunks(self):
        for chunk in self.chunks.values():
            chunk.print_basic_info()
