from chunk_data import File


def main_options():
    print('Main Menu')
    print('1 - Load File')
    print('Q - Quit')


class Menu:
    def __init__(self):
        self.active_options = None
        self.original_file = None

    @staticmethod
    def file_options():
        print('File Menu:')
        print('1 - Print basic info')
        print('2 - Print chunks')
        print('3 - Chunks menu')
        print('B - Back to main menu')
        print('Q - Quit')

    @staticmethod
    def chunks_options():
        print('Chunks Menu')
        print('Enter the number of the chunk to view details')
        print('B - Back to file menu')
        print('Q - Quit')

    @staticmethod
    def invalid_option():
        print('Invalid option!')

    def start(self):
        while True:
            main_options()
            choice = input('Enter your choice: ').lower()

            if choice == '1':
                self.load_file()
                self.file_menu()
            elif choice == 'q':
                break
            else:
                Menu.invalid_option()

    def file_menu(self):
        self.active_options = self.file_options
        while True:
            self.active_options()
            choice = input('Enter your choice: ').lower()

            if choice == '1':
                self.original_file.print_info()
            elif choice == '2':
                self.original_file.print_chunks()
            elif choice == '3':
                self.chunks_menu()
            elif choice == 'b':
                break
            elif choice == 'q':
                exit()
            else:
                Menu.invalid_option()

    def chunks_menu(self):
        self.active_options = self.chunks_options
        while True:
            self.active_options()
            choice = input('Enter your choice: ').lower()

            if choice == 'b':
                break
            elif choice == 'q':
                exit()
            else:
                if choice.isdigit():
                    index = int(choice) - 1
                    if 0 <= index < len(self.original_file.chunks):
                        chunk = list(self.original_file.chunks.values())[index]
                        chunk.show_details()
                    else:
                        self.invalid_option()
                else:
                    self.invalid_option()
        self.active_menu()

    def load_file(self):
        self.original_file = File('../img-example/1.png')

    def active_menu(self):
        pass
