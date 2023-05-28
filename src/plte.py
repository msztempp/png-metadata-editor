from chunk import Chunk
import numpy as np
import matplotlib.pyplot as plt


def init_palette():
    return {
        "Red": {i: 0 for i in range(256)},
        "Green": {i: 0 for i in range(256)},
        "Blue": {i: 0 for i in range(256)}
    }


class PLTE(Chunk):
    def __init__(self, length, data, crc, color_type):
        super().__init__(length, "PLTE", crc)
        self.entries = length // 3
        self.required = color_type == 3
        self.palette = init_palette()
        self.fill_palette(data)

    def fill_palette(self, data):
        for i in range(0, self.length, 3):
            self.palette["Red"][data[i]] += 1
            self.palette["Green"][data[i + 1]] += 1
            self.palette["Blue"][data[i + 2]] += 1

    def print_palette(self):
        print("Palette:")
        for color, values in self.palette.items():
            print(f"   {color}:")
            for key, value in values.items():
                if value == 0:
                    continue
                print(f"         {key}: {value}")

    def plot_palette(self):
        max_y = max(max(color.values()) for color in self.palette.values())
        yticks = np.arange(0, max_y + 1, 1)
        fig, axs = plt.subplots(1, 3)
        plot_colors = ['r', 'g', 'b']
        for i, (color, values) in enumerate(self.palette.items()):
            axs[i].set_yticks(yticks)
            axs[i].set_ylim(0, max_y + 1)
            axs[i].set_xlim(0, 256)
            axs[i].bar(values.keys(), values.values(), width=5, color=plot_colors[i])
            axs[i].grid(axis='y', alpha=0.2)
        plt.show()

    def print_info(self):
        self.basic_info()
