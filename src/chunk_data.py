import os

KILO = 1000
MEGA = 1000000
GIGA = 1000000000


def check_ext(pathname):
    if pathname[-3:].lower() != "png":
        raise Exception("INCORRECT FILE FORMAT!\nThis program is strictly for analyzing PNG files.")


def get_name(pathname):
    file_name = os.path.basename(pathname)
    return os.path.splitext(file_name)[0]


def format_size(size_bytes):
    if size_bytes < KILO:
        return str(size_bytes) + " B"
    elif size_bytes < MEGA:
        kilo = size_bytes // KILO
        bytes = round(size_bytes % KILO, -2)
        return str(kilo) + ',' + str(bytes)[0] + " KB"
    elif size_bytes < GIGA:
        mega = size_bytes // MEGA
        # kilo = round(size_bytes // KILO, -3)
        kilo = round((size_bytes % MEGA) // KILO, -2)
        return str(mega) + ',' + str(kilo)[0] + " MB"


def load_data(pathname):
    name = get_name(pathname)
    png_file = open(pathname, "rb")  # open file in read bytes mode
    byte_string = png_file.read()  # read all of it's data bytes
    png_file.close()  # close file
    size = len(byte_string)
    return name, size, byte_string


def file_info(name, size):
    print("> NAME: ", name)
    print("> SIZE: {formatted} ({bytes} bytes)".format(formatted=format_size(size), bytes=size))


def parse_data(byte_string, chunk_type):
    if chunk_type == b"IEND":
        return 0, None, None

    i = byte_string.find(chunk_type)
    if i == -1:
        raise Exception("Couldn't find {} chunk!".format(chunk_type))
    length = int(byte_string[i - 4:i].replace(b"\x00", b"").hex(), 16)
    i += 4
    data = byte_string[i:i + length]
    i += length
    crc = byte_string[i:i + 4]
    return length, data, crc
