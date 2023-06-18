from src.chunk import Chunk


class TIME(Chunk):
    def __init__(self, raw_bytes):
        super().__init__(raw_bytes)
        self.year = None  # 2 bytes (e.g., 1995 not 95)
        self.month = None  # 1 byte (1-12)
        self.day = None  # 1 byte (1-31)
        self.hour = None  # 1 byte (0-23)
        self.minute = None  # 1 byte (0-59)
        self.second = None  # 1 byte (0-60) (to allow leap second)
        self.check_time()

    def check_time(self):
        if self.length != 7:
            raise Exception('Invalid tIME chunk length')
        self.year = int.from_bytes(self.data[:2], 'big')
        self.month = int.from_bytes(self.data[2:3], 'big')
        self.day = int.from_bytes(self.data[3:4], 'big')
        self.hour = int.from_bytes(self.data[4:5], 'big')
        self.minute = int.from_bytes(self.data[5:6], 'big')
        self.second = int.from_bytes(self.data[6:7], 'big')

    def details(self):
        self.print_basic_info()
        print('chunk tIME info:')
        print(' year:', self.year)
        print(' month:', self.month)
        print(' day:', self.day)
        print(' hour:', self.hour)
        print(' minute:', self.minute)
        print(' second:', self.second)
        print()
