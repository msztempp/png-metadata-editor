import matplotlib.pyplot as plt
from src.chunk import Chunk
from src.clear_terminal import clear_terminal


def translate_plte(value, from_min, from_max, to_min, to_max):
    return (value - from_min) * (to_max - to_min) / (from_max - from_min) + to_min


def translate_RGB(rgb_tuple):
    return tuple(translate_plte(value, 0, 255, 0, 1) for value in rgb_tuple)


class PLTE(Chunk):
    def __init__(self, raw_chunk_bytes, color_type):
        super().__init__(raw_chunk_bytes)
        self.entries = self.length // 3
        self.required = True if color_type == 3 else False
        self.palettes = [(self.data[i], self.data[i + 1], self.data[i + 2]) for i in range(0, self.length, 3)]

    def plot_plte(self):
        width = 1
        fig, ax = plt.subplots(1, 1)
        ax.set_xlim(0 + width / 2, self.entries + width / 2)
        ax.set_ylim(0, 1)
        for i in range(self.entries):
            ax.bar(i + 1, 1, width=width, color=translate_RGB(self.palettes[i]))
        ax.set_xticks([i + 1 for i in range(self.entries)])
        plt.show()

    def details(self):
        clear_terminal()
        self.print_basic_info()
        print('PLTE chunk info:')
        print(' entries:', self.entries)
        print(' required:', self.required)
        self.plot_plte()
