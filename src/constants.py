KILO = 1024
MEGA = KILO * KILO
GIGA = MEGA * KILO
TERA = GIGA * KILO

# https://www.w3.org/TR/png/#4Concepts.FormatTypes

chunks_types = [b'IHDR', b'PLTE', b'IDAT', b'IEND',
                b'cHRM', b'gAMA', b'iCCP', b'sBIT', b'sRGB', b'bKGD', b'hIST', b'tRNS', 'pHYs',
                b'sPLT', b'tIME', b'iTXt', b'tEXt', b'zTXt']
