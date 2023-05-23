import image_attributes


def decode_chunks(chunksArray):
    chunkIterator = 0
    mergedIdatChunkData = []




def decode_IHDR(ihdrChunk):

    print("\nIHDR: ")

    width = ihdrChunk.dataArray[3] | (ihdrChunk.dataArray[2]<<8) | (ihdrChunk.dataArray[1]<<16) | (ihdrChunk.dataArray[0]<<24)
    height = ihdrChunk.dataArray[7] | (ihdrChunk.dataArray[6]<<8) | (ihdrChunk.dataArray[5]<<16) | (ihdrChunk.dataArray[4]<<24)
    bitDepth = ihdrChunk.dataArray[8]
    colorType = ihdrChunk.dataArray[9]
    compressionMethod = ihdrChunk.dataArray[10]
    filterMethod = ihdrChunk.dataArray[11]
    interlaceMethod = ihdrChunk.dataArray[12]

    print("Width = " + str(width))
    print("Height = " + str(height))
    print("Bit Depth = " + str(bitDepth) + " bits per sample/palette index")
    decode_IHDRcolorType(colorType, bitDepth)
    print(decode_IHDRcompressionMethod(compressionMethod))
    print(decode_IHDRfilterMethod(filterMethod))
    print(decode_IHDRinterlaceMethod(interlaceMethod))

    return (image_attributes.ImageAtributes(width, height, bitDepth, colorType, compressionMethod, filterMethod, interlaceMethod))


def decode_IHDRcolorType(colorType, bitDepth):
    allowedBitDepth = {}
    sampleDepth = bitDepth

    if(colorType == 0):
        print("Color type = Each pixel is a grayscale sample")
        allowedBitDepth = {1, 2, 4, 8, 16}
    elif(colorType == 2):
        print("Color type = Each pixel is an R,G,B triple")
        allowedBitDepth = {8, 16}
    elif(colorType == 3):
        print("Color type = Each pixel is a palette index; a PLTE chunk must appear")
        allowedBitDepth = {1, 2, 4, 8}
        sampleDepth = 8
    elif(colorType == 4):
        print("Color type = Each pixel is a grayscale sample, followed by an alpha sample")
        allowedBitDepth = {8, 16}
    elif(colorType == 6):
        print("Color type = Each pixel is an R,G,B triple, followed by an alpha sample")
        allowedBitDepth = {8, 16}
    else:
        print("Color type = Invalid color type")

    if bitDepth in allowedBitDepth:
        print("Bit Depth correct!")
        print("Sample Depth = " + str(sampleDepth) + " bits")
    else:
        print("Bit Depth INCORRECT. May pose problems with compression.")

def decode_IHDRcompressionMethod(compressionMethod):
    switcher = {
        0: "Compression method = Compression Method 0 (deflate/inflate)"
    }
    return switcher.get(compressionMethod, "Compression method = INVALID (not yet implemented)")

def decode_IHDRfilterMethod(filterMethod):
    switcher = {
        0: "Filter method = Filter Method 0 (adaptive filtering with five basic filter types)"
    }
    return switcher.get(filterMethod, "Filter method = INVALID (not yet implemented)")

def decode_IHDRinterlaceMethod(interlaceMethod):
    switcher = {
        0: "Interlace method = No interlace",
        1: "Interlace method = Adam7 interlace"
    }
    return switcher.get(interlaceMethod, "Interlace method = INVALID")

