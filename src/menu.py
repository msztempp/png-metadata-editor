import os
from glob import glob
from clear_terminal import clear_terminal
from matplotlib import pyplot as plt
from file_data import File


class Menu:
    def __init__(self):
        self.file_menu = None
        self.file_list = None
        self.pathname = None
        self.original_file = None
        self.choice = None
        self.active_menu = self.menu_main
        self.active_options = self.main_options

    def set_file_list(self, dir_path):
        self.file_list = glob(dir_path + '*')

    def start(self):
        plt.ion()
        plt.show()
        self.set_file_list('../img-example/')
        while self.choice is not 'q' or self.choice is not 'Q':
            self.active_options()
            self.active_menu()

    def main_options(self):
        print('Choose a file to work with:')
        print()
        for i, file in enumerate(self.file_list, 1):
            base_name = os.path.basename(file)
            extension = os.path.splitext(base_name)[1]
            file_name = os.path.splitext(base_name)[0]
            print(' {} - {}{}'.format(i, file_name, extension))
        print()
        print('q - quit\n')
        print('Your choice: ', end='')

    @staticmethod
    def file_options():
        print('Choose option to perform:')
        print()
        print(' 1 - print chunks list')
        print(' 2 - go to chunk details')
        print(' 3 - save a new file with only critical chunks')
        print(' 4 - perform fft')
        print(' b - go back')
        print(' q - quit')
        print()
        print('Your choice: ', end='')

    def chunks_options(self):
        print('Choose chunk to show details')
        print()
        print('Available chunks:')
        print()
        for i, chunk in enumerate(self.original_file.chunks.keys(), 1):
            print(' {} - {} details.'.format(i, chunk))
        print()
        print('b - go back')
        print('q - quit')
        print()
        print('Your choice: ', end='')

    @staticmethod
    def invalid_option(*args):
        print('Invalid option! Try again.')

    def load_file(self, pathname):
        self.pathname = pathname
        self.original_file = File(self.pathname)
        clear_terminal()
        print('Successfully loaded: {}'.format(self.original_file.file_name))
        print()

    def menu_main(self):
        def load_file(choice):
            self.load_file(self.file_list[int(choice) - 1])
            self.active_menu = self.menu_file
            self.active_options = Menu.file_options

        switch = {
            'f': load_file,
            'q': exit,
        }
        for i, file in enumerate(self.file_list, 1):
            switch[str(i)] = load_file
        choice = input('').lower()
        clear_terminal()
        switch.get(choice, Menu.invalid_option)(choice)

    def menu_file(self):
        def go_back():
            self.original_file = None
            self.active_menu = self.menu_main
            self.active_options = self.main_options

        def switch_chunks_menu():
            clear_terminal()
            self.active_menu = self.menu_chunk
            self.active_options = self.chunks_options

        switch = {
            '1': self.original_file.print_chunks,
            '2': switch_chunks_menu,
            '3': self.original_file.print_to_file,
            '4': self.original_file.perform_fft,
            'b': go_back,
            'q': exit,
        }
        choice = input('').lower()
        clear_terminal()
        switch.get(choice, Menu.invalid_option)()

    def menu_chunk(self):
        def go_back():
            clear_terminal()
            self.active_menu = self.menu_file
            self.active_options = Menu.file_options

        switch = {
            'b': go_back,
            'q': exit,
        }
        for i, chunk in enumerate(self.original_file.chunks.values(), 1):
            switch[str(i)] = chunk.details
        choice = input('').lower()
        switch.get(choice, Menu.invalid_option)()
