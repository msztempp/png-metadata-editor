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
    return tuple(translate(value, 0, 255, 0, 1) for value in rgb_tuple)


class PLTE(Chunk):
    def __init__(self, raw_bytes, color_type=3):
        super().__init__(raw_bytes)
        self.entries = self.length // 3
        self.required = color_type == 3
        self.palettes = [tuple(self.data[i:i+3]) for i in range(0, self.length, 3)]

    def plot_palettes(self):
        width = 1
        fig, ax = plt.subplots(1, 1)
        ax.bar(range(self.entries), [1]*self.entries, width=width, color=[translate_RGB(rgb) for rgb in self.palettes])
        ax.set_xlim(0, self.entries)
        ax.set_ylim(0, 1)
        ax.set_xticks(range(self.entries))
        ax.set_yticks([])
        fig.tight_layout()
        fig.canvas.set_window_title('Palettes')
        plt.draw()
        plt.pause(0.001)

    def details(self):
        self.print_basic_info()
        print('entries:', self.entries)
        print('required:', self.required)
        self.plot_palettes()
