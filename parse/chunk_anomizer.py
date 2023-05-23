def get_png_sygnature_as_byte():
    sygnature = [137, 80, 78, 71, 13, 10, 26, 10]  # PNG sygnature
    return bytearray(sygnature)


def anominize_chunks(chunks_array, file_name):
    is_IDAT_chain = False
    was_IDAT = False

    file = open(file_name, 'wb')

    file.write(get_png_sygnature_as_byte())

    # save only critical chunks
    chunk_iterator = 0
    while chunk_iterator < len(chunks_array):
        if (chunks_array[chunk_iterator].getChunkTypeText() == 'IHDR' or
                chunks_array[chunk_iterator].getChunkTypeText() == 'PLTE' or
                chunks_array[chunk_iterator].getChunkTypeText() == 'IDAT' or
                chunks_array[chunk_iterator].getChunkTypeText() == 'IEND'):

            if chunks_array[chunk_iterator].getChunkTypeText() == 'IDAT' and was_IDAT == False:
                is_IDAT_chain = True
                was_IDAT = True

            if chunks_array[chunk_iterator].getChunkTypeText() != 'IDAT' and is_IDAT_chain:
                is_IDAT_chain = False

            if chunks_array[chunk_iterator].getChunkTypeText() != 'IDAT':
                file.write(chunks_array[chunk_iterator].getChunkAsList())
            elif is_IDAT_chain:
                file.write(chunks_array[chunk_iterator].getChunkAsList())

        chunk_iterator += 1
