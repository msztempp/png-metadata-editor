import re

from constants import *
from chunk import Chunk
from src.chunks.anicillary.text import TEXT
from src.chunks.anicillary.trns import TRNS
from src.chunks.critical.ihdr import IHDR
from src.chunks.critical.plte import PLTE
from src.chunks.critical.idat import IDAT
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
        self.chunks_indices = None
        self.size = None
        self.byte_data = None
        self.file_name = None
        self.extension = "PNG"
        self.chunks = {}
        self.pathname = pathname
        self.get_name(pathname)
        self.load_data(pathname)
        self.find_chunks()
        self.init_chunks()

    def get_name(self, pathname):
        pathname = pathname.lower()
        full_file_name = re.search(r'\w+\.png', pathname)
        self.file_name = full_file_name.group(0)[:-4]

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

    def get_chunk_data(self, index):
        start = index
        length = int.from_bytes(self.byte_data[start:start + 4], "big")
        end = index + length + 12
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
        self.get_chunks()  # init self.chunks with raw_bytes
        for chunk_type in self.chunks.keys():  # this loop inits chunks
            if chunk_type == "IHDR":
                self.chunks[chunk_type] = IHDR(self.chunks[chunk_type])
            elif chunk_type == "PLTE":
                self.chunks[chunk_type] = PLTE(self.chunks[chunk_type], self.chunks["IHDR"].color_type)
            elif chunk_type == "IDAT":
                if type(self.chunks[chunk_type]) == list:
                    for i in range(len(self.chunks[chunk_type])):
                        self.chunks[chunk_type][i] = Chunk(self.chunks[chunk_type][i])
                    self.chunks[chunk_type] = IDAT(self.chunks[chunk_type],
                                                   self.chunks["IHDR"].width,
                                                   self.chunks["IHDR"].height,
                                                   self.chunks["IHDR"].color_type)
                else:
                    self.chunks[chunk_type] = IDAT(self.chunks[chunk_type],
                                                   self.chunks["IHDR"].width,
                                                   self.chunks["IHDR"].height,
                                                   self.chunks["IHDR"].color_type)
            elif chunk_type == "tRNS":
                self.chunks[chunk_type] = TRNS(self.chunks[chunk_type],
                                               self.chunks["IHDR"].color_type,
                                               self.chunks["IHDR"].bit_depth)
            elif chunk_type == "tEXt":
                if type(self.chunks[chunk_type]) == list:
                    for i in range(len(self.chunks[chunk_type])):
                        self.chunks[chunk_type][i] = Chunk(self.chunks[chunk_type][i])
                    self.chunks[chunk_type] = TEXT(self.chunks[chunk_type])
                else:
                    self.chunks[chunk_type] = TEXT(self.chunks[chunk_type])
            else:
                if type(self.chunks[chunk_type]) == list:
                    for i in range(len(self.chunks[chunk_type])):
                        self.chunks[chunk_type][i] = Chunk(self.chunks[chunk_type][i])
                    self.chunks[chunk_type] = Chunk(chunk_list=self.chunks[chunk_type])
                else:
                    self.chunks[chunk_type] = Chunk(self.chunks[chunk_type])

    def print_chunks(self):
        for chunk in self.chunks.values():
            chunk.print_basic_info()

    def print_to_file(self):
        new_file_name = "../png_files/{}_crit.png".format(self.file_name)
        tmp_png = open(new_file_name, "wb")
        tmp_png.write(self.byte_data[:8])
        for chunk_type in self.chunks_indices["CRITICAL"].values():
            for instance_index in chunk_type:
                chunk_data = self.get_chunk_data(instance_index)
                tmp_png.write(chunk_data)
        print("saved only with critical chunks: ", new_file_name)
