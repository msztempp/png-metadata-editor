from chunk import Chunk


class IHDR(Chunk):
    FILTER_METHODS = {
        0: "None",
        1: "Sub",
        2: "Up",
        3: "Average",
        4: "Paeth"
    }

    def __init__(self, length, data, crc):
        super().__init__(length, "IHDR", crc)
        self.width = None
        self.height = None
        self.bit_depth = None
        self.color_type = None
        self.filter_method = None
        self.interlace_method = None
        self.analyse(data)

    def print_info(self):
        self.basic_info()
        print(f"Width: {self.width}\nHeight: {self.height}")
        print(f"Bit depth: {self.bit_depth}\nColor type: {self.color_type}")
        print(f"Filter method: {self.filter_method}")
        print(f"Interlace method: {self.interlace_method}")

    def analyse(self, data):
        if self.length != 13:
            raise ValueError("IHDR chunk's length is invalid")
        self.width = int.from_bytes(data[:4], byteorder='big')
        self.height = int.from_bytes(data[4:8], byteorder='big')
        self.bit_depth = int.from_bytes(data[8:9], byteorder='big')
        self.color_type = int.from_bytes(data[9:10], byteorder='big')
        self.filter_method = self.get_filter_method(int.from_bytes(data[10:11], byteorder='big'))
        self.interlace_method = "No interlace" if int.from_bytes(data[11:12], byteorder='big') == 0 else "Adam7 interlace"

    @staticmethod
    def get_filter_method(argument):
        return IHDR.FILTER_METHODS.get(argument, "Not found")
