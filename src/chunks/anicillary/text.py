from src.chunk import Chunk


class TEXT(Chunk):
    def __init__(self, init_data):
        if type(init_data) == list:
            super().__init__(chunk_list=init_data)
        else:
            super().__init__(chunk_bytes=init_data)
        self.data_to_str()

    def data_to_str(self):
        def decode_f(x):
            return x.decode("utf-8")

        self.data = [instance.split(b"\x00") for instance in self.data]
        self.data = [list(map(decode_f, instance_split)) for instance_split in self.data]
        for instance in self.data:
            instance[0] = instance[0].upper()

    def details(self):
        self.print_basic_info()
        print(" ", end="")
        print(" tEXt DATA ")
        for instance in self.data:
            print("> {keyword}: {content}".format(keyword=instance[0], content=instance[1]))
        print()
