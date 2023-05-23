# https://www.w3.org/TR/png/#5PNG-file-signature
from signature import get_png_signature_as_byte


def anonymize_chunks(chunks_array, file_name):
    is_next_IDAT = False
    was_previous_IDAT = False

    # Open the file in write binary mode
    file = open(file_name, 'wb')

    # Write the PNG signature to the file
    file.write(get_png_signature_as_byte())

    # all critcal chunks are IHDR(Image header), PLTE(Palette), IDAT(Image data), IEND(Image End)
    # Save only specific chunks
    chunk_iterator = 0
    while chunk_iterator < len(chunks_array):
        # Check if the chunk type is IHDR, PLTE, IDAT, or IEND
        chunk_type = chunks_array[chunk_iterator].getChunkTypeText()
        if chunk_type == 'IHDR' or chunk_type == 'PLTE' or chunk_type == 'IDAT' or chunk_type == 'IEND':
            if chunk_type == 'IDAT' and not was_previous_IDAT:
                is_next_IDAT = True
                was_previous_IDAT = True

            if chunk_type != 'IDAT' and is_next_IDAT:
                is_next_IDAT = False

            if chunk_type != 'IDAT':
                file.write(chunks_array[chunk_iterator].getChunkAsList())
            elif is_next_IDAT:
                file.write(chunks_array[chunk_iterator].getChunkAsList())

        chunk_iterator += 1
