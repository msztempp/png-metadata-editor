from src.chunk import Chunk


class CHRM(Chunk):
    def __init__(self, chunk_bytes):
        super().__init__(chunk_bytes)
        self.whitePointX=None
        self.whitePointY = None
        self.redX = None
        self.redY = None
        self.greenX = None
        self.greenY = None
        self.blueX = None
        self.blueY = None
        self.analyse()

    def analyse(self):
        if self.length!=32:
            raise Exception('CHRM chunk length is invalid')

        data=self.data
        self.whitePointX=int.from_bytes(data[0:4], byteorder='big')/100000
        self.whitePointY = int.from_bytes(data[4:8], byteorder='big')/100000
        self.redX = int.from_bytes(data[8:12], byteorder='big')/100000
        self.redY = int.from_bytes(data[12:16], byteorder='big')/100000
        self.greenX = int.from_bytes(data[16:20], byteorder='big')/100000
        self.greenY = int.from_bytes(data[20:24], byteorder='big')/100000
        self.blueX = int.from_bytes(data[24:28], byteorder='big')/100000
        self.blueY = int.from_bytes(data[28:32], byteorder='big')/100000

    def details(self):
        self.print_basic_info()
        print(f'White point x: {self.whitePointX}')
        print(f'White point y: {self.whitePointY}')
        print(f'Red x: {self.redX}')
        print(f'Red y: {self.redY}')
        print(f'Green x: {self.greenX}')
        print(f'Green y: {self.greenY}')
        print(f'Blue x: {self.blueX}')
        print(f'Blue y: {self.blueY}')
