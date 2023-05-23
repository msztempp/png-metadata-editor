def check_signature(byte_data):
    # The first eight bytes of a PNG datastream always contain the following (decimal) values:
    signature = [137, 80, 78, 71, 13, 10, 26, 10]  # PNG signature
    signature_byte = 0

    while signature_byte < 8:
        if signature[signature_byte] != byte_data[signature_byte]:
            return False

        signature_byte += 1
    print("PNG file detected.")
    return True


def get_png_signature_as_byte():
    signature = [137, 80, 78, 71, 13, 10, 26, 10]  # PNG sygnature
    return bytearray(signature)

