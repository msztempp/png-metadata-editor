import os
from constants import KILO, MEGA, GIGA


def get_name(pathname):
    file_name = os.path.basename(pathname)
    return os.path.splitext(file_name)[0]


def format_size(size_bytes):
    if size_bytes < KILO:
        return f'{size_bytes} B'
    elif size_bytes < MEGA:
        kilo = size_bytes // KILO
        chunk_bytes = size_bytes % KILO
        return f'{kilo},{chunk_bytes} B'
    elif size_bytes < GIGA:
        mega = size_bytes // MEGA
        kilo = (size_bytes % MEGA) // KILO
        return f'{mega},{kilo} MB'


def load_data(pathname):
    name = get_name(pathname)
    with open(pathname, 'rb') as png_file:
        byte_string = png_file.read()
    size = len(byte_string)
    return name, size, byte_string


def file_info(name, size):
    print('> NAME:', name)
    print('> SIZE: {formatted} ({bytes} bytes)'.format(formatted=format_size(size), bytes=size))


def parse_data(byte_string, chunk_type):
    if chunk_type == b'IEND':
        return 0, None, None

    i = byte_string.find(chunk_type)
    if i == -1:
        raise Exception('Couldnt find {} chunk!'.format(chunk_type))
    length = int(byte_string[i - 4:i].replace(b'\x00', b'').hex(), 16)
    i += 4
    data = byte_string[i:i + length]
    i += length
    crc = byte_string[i:i + 4]
    return length, data, crc
