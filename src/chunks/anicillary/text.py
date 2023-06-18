from src.chunk import Chunk


class TEXT(Chunk):
    def __init__(self, init_data):
        if type(init_data) == list:
            super().__init__(is_chunk_list=init_data)
            self.keyword = []
            self.text = []
        else:
            super().__init__(chunk_bytes=init_data)
            self.keyword=None
            self.text=None
        self.analyse()

    def analyse(self):
        if type(self.data)==list:
            for data in self.data:
                data = data.split(b'\x00')
                self.keyword.append(data[0].decode('latin1'))
                self.text.append(data[1].decode('latin1'))
        else:
            data=self.data
            data = data.split(b'\x00')
            self.keyword=data[0].decode('latin1')
            self.text=data[1].decode('latin1')

    def details(self):
        self.print_basic_info()
        if type(self.data)==list:
            for i in range(0,len(self.data)):
                print('Keyword: ', self.keyword[i])
                print('Text string: ', self.text[i])
        else:
            print('Keyword: ',self.keyword)
            print('Text string: ',self.text)