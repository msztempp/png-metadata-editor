from chunk import Chunk
import numpy as np
import matplotlib.pyplot as plt


def init_palette():
    return {
        'Red': np.zeros(256, dtype=np.int32),
        'Green': np.zeros(256, dtype=np.int32),
        'Blue': np.zeros(256, dtype=np.int32)
    }


def translate(value, from_min, from_max, to_min, to_max):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min


def translate_RGB(rgb_tuple):
    return (
        translate(rgb_tuple[0], 0, 255, 0, 1),
        translate(rgb_tuple[1], 0, 255, 0, 1),
        translate(rgb_tuple[2], 0, 255, 0, 1)
    )


class PLTE(Chunk):
    def __init__(self, raw_bytes, color_type=3):
        super().__init__(raw_bytes)
        self.entries = self.length // 3
        self.required = True if color_type == 3 else False
        self.palettes = [(self.data[i], self.data[i + 1], self.data[i + 2]) for i in range(0, self.length, 3)]


    def fill_palette(self, data):
        for i in range(0, self.length, 3):
            self.palette['Red'][data[i]] += 1
            self.palette['Green'][data[i + 1]] += 1
            self.palette['Blue'][data[i + 2]] += 1

    def print_palette(self):
        print('Palette:')
        for color, values in self.palette.items():
            print(f'   {color}:')
            for key, value in enumerate(values):
                if value == 0:
                    continue
                print(f'{key}: {value}')

    def plot_palettes(self):
        fig, ax = plt.subplots(1, 1)
        ax.set_xlim(0, self.entries)
        ax.set_ylim(0, 1)
        for i in range(self.entries):
            ax.bar(i, 1, width=1, color=translate_RGB(self.palettes[i]))
        ax.set_axis_off()
        fig.tight_layout()
        fig.canvas.set_window_title('Palettes')
        plt.show()

    def print_info(self):
        self.print_basic_info()


