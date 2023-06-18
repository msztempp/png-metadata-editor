from src.chunk import Chunk
from src.clear_terminal import clear_terminal


class SRGB(Chunk):
    RENDERING_INTENT = {
        0: 'Perceptual',  # for images preferring good adaptation to the output device gamut at the expense of colorimetric accuracy, such as photographs.
        1: 'Relative colorimetric',  # or images requiring colour appearance matching (relative to the output device white point), such as logos.
        2: 'Saturation',  # for images preferring preservation of saturation at the expense of hue and lightness, such as charts and graphs.
        3: 'Absolute colorimetric'  # for images requiring preservation of absolute colorimetry, such as previews of images destined for a different output device (proofs).
    }

    def __init__(self, chunk_bytes):
        super().__init__(chunk_bytes)
        self.rendering_intent = None
        self.analyse()

    def analyse(self):
        if self.length != 1:
            raise Exception('sRGB chunk length is invalid')
        data = self.data
        rendering_number = int.from_bytes(data[0:1], byteorder='big')
        self.rendering_intent = SRGB.RENDERING_INTENT.get(rendering_number)

    def details(self):
        clear_terminal()
        self.print_basic_info()
        print('sRGB chunk info:')
        print('Rendering intent: ', self.rendering_intent)
        print()
