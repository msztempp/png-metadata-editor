from src.chunk import Chunk


class TEXT(Chunk):
    def __init__(self, init_data):
        super().__init__(chunk_list=init_data) if type(init_data) == list else super().__init__(chunk_bytes=init_data)
        self.data_to_str()

    def data_to_str(self):
        self.data = [[x.decode("utf-8").upper() for x in instance.split(b"\x00")] for instance in self.data]

    def details(self):
        self.print_basic_info()
        print(" tEXt DATA ")
        for keyword, content in self.data:
            print(f"> {keyword}: {content}")
        print()
