from chunk import Chunk
import zlib
import matplotlib.pyplot as plt
import numpy as np

# https://pyokagan.name/blog/2019-10-14-png/

BYTES_PER_PIXEL = {
    0: 1,
    2: 3,
    3: 1,
    4: 2,
    6: 4,
    'default': 'Not found'
}


def paeth_predictor(a, b, c):
    p = a + b - c
    pa = abs(p - a)
    pb = abs(p - b)
    pc = abs(p - c)
    if pa <= pb and pa <= pc:
        Pr = a
    elif pb <= pc:
        Pr = b
    else:
        Pr = c
    return Pr


class IDAT(Chunk):
    def __init__(self, length, data, crc, width, height, color_type, palette=None):
        super().__init__(length, "IDAT", crc)
        self.palette = palette
        self.recon_data = None
        self.data = data
        self.width = width
        self.height = height
        self.color_type = color_type
        self.bytes_per_pixel = BYTES_PER_PIXEL.get(color_type)
        self.analyse()

    def analyse(self):
        self.data = zlib.decompress(self.data)
        self.recon_data = []
        stride = self.width * self.bytes_per_pixel
        i = 0
        for r in range(self.height):
            filter_type = self.data[i]
            i += 1
            for c in range(stride):
                filt_x = self.data[i]
                i += 1
                if filter_type == 0:  # None
                    recon_x = filt_x
                elif filter_type == 1:  # Sub
                    recon_x = filt_x + self.recon_a(r, c, stride)
                elif filter_type == 2:  # Up
                    recon_x = filt_x + self.recon_b(r, c, stride)
                elif filter_type == 3:  # Average
                    recon_x = filt_x + (self.recon_a(r, c, stride) + self.recon_b(r, c, stride)) // 2
                elif filter_type == 4:  # Paeth
                    recon_x = filt_x + paeth_predictor(
                        self.recon_a(r, c, stride),
                        self.recon_b(r, c, stride),
                        self.recon_c(r, c, stride)
                    )
                else:
                    raise Exception("Unknown filter type: " + str(filter_type))
                self.recon_data.append(recon_x & 0xff)  # truncation to byte

    def recon_a(self, r, c, stride):
        return self.recon_data[r * stride + c - self.bytes_per_pixel] if c >= self.bytes_per_pixel else 0

    def recon_b(self, r, c, stride):
        return self.recon_data[(r - 1) * stride + c] if r > 0 else 0

    def recon_c(self, r, c, stride):
        return self.recon_data[(r - 1) * stride + c - self.bytes_per_pixel] if r > 0 and c >= self.bytes_per_pixel else 0

    def apply_palette(self, palette):
        self.recon_data = [pixel for pixel_i in self.recon_data for pixel in palette[pixel_i]]
        self.bytes_per_pixel = 3

    def print_info(self):
        self.print_basic_info()

    def check_correctness(self):
        plt.imshow(np.array(self.recon_data).reshape((self.height, self.width, self.bytes_per_pixel)))
        plt.show()
