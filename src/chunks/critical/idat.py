from chunk import Chunk
import zlib
import matplotlib.pyplot as plt
import numpy as np


def byte_per_pixel(color_type):
    switcher = {
        0: 1,
        2: 3,
        3: 1,
        4: 2,
        6: 4,
    }
    return switcher.get(color_type, 'Not found')


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
    def __init__(self, init_data, width, height, color_type):
        self.recon_data = None
        super().__init__(chunk_list=init_data) if isinstance(init_data, list) else super().__init__(chunk_bytes=init_data)
        if isinstance(self.data, list):
            self.length = sum(self.length)
            self.data = b''.join(self.data)
        self.width = width
        self.height = height
        self.color_type = color_type
        self.bytes_per_pixel = byte_per_pixel(color_type)
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
                    raise Exception('Unknown filter type: ' + str(filter_type))
                self.recon_data.append(recon_x & 0xff)  # truncation to byte

    def recon_a(self, r, c, stride):
        return self.recon_data[r * stride + c - self.bytes_per_pixel] if c >= self.bytes_per_pixel else 0

    def recon_b(self, r, c, stride):
        return self.recon_data[(r - 1) * stride + c] if r > 0 else 0

    def recon_c(self, r, c, stride):
        return self.recon_data[(r - 1) * stride + c - self.bytes_per_pixel] if r > 0 and c >= self.bytes_per_pixel else 0

    def display_data(self, title, data=None, bytes_per_pixel=None):
        if data is None:
            data = self.recon_data
        fig, ax = plt.subplots(1, 1)
        if bytes_per_pixel is None:
            bytes_per_pixel = self.bytes_per_pixel
        if bytes_per_pixel == 1:
            ax.imshow(np.array(data).reshape((self.height, self.width)), cmap='gray')
        else:
            ax.imshow(np.array(data).reshape((self.height, self.width, bytes_per_pixel)))
        ax.set_axis_off()
        ax.set_facecolor('whitesmoke')
        fig.patch.set_facecolor('whitesmoke')
        fig.tight_layout()
        fig.canvas.set_window_title(title)
        plt.draw()
        plt.pause(0.001)

    def apply_palette(self, palette):
        new_data = [pixel for pixel_i in self.recon_data for pixel in palette[pixel_i]]
        self.display_data('IDAT + palettes', data=new_data, bytes_per_pixel=3)

    def apply_transparency(self, transparency_data, palette=None):
        if palette is not None:
            transparent_palette = []
            for i in range(len(palette)):
                if i > len(transparency_data) - 1:
                    transparent_palette.append((palette[i][0], palette[i][1], palette[i][2], 255))
                else:
                    transparent_palette.append((palette[i][0], palette[i][1], palette[i][2], transparency_data[i]))
            new_data = [pixel for pixel_i in self.recon_data for pixel in transparent_palette[pixel_i]]
            self.display_data('IDAT + palette + transparency', data=new_data, bytes_per_pixel=4)
        print('palette and transparency applied to IDAT')

    def details(self):
        self.print_basic_info()
        self.display_data('IDAT')
