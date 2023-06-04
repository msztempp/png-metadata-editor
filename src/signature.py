# https://www.w3.org/TR/png/#5PNG-file-signature
# The first eight bytes of a PNG datastream always contain the following (decimal) values:

def check_signature(chunk_byte):
    signature = [137, 80, 78, 71, 13, 10, 26, 10]  # PNG signature

    for i, byte in enumerate(signature):
        if chunk_byte[i] != byte:
            return False
    return True
