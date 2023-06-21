import os
from glob import glob

from clear_terminal import clear_terminal
from matplotlib import pyplot as plt
from file_data import File

from src.decrypt_encrypt.decrypt_encrypt_algorithm import DecryptEncryptAlgorithm


class Menu:
    def __init__(self):
        self.DecryptEncryptAlgorithm = None
        self.file_menu = None
        self.file_list = None
        self.pathname = None
        self.original_file = None
        self.choice = None
        self.active_menu = self.menu_main
        self.active_options = self.main_options
        self.data_after_encryption = None
        self.data_after_decryption = None
        self.after_iend_data = None

    def set_file_list(self, dir_path):
        self.file_list = glob(dir_path + '*')

    def start(self):
        plt.ion()
        plt.show()
        self.set_file_list('../img-example/')
        while self.choice != 'q' or self.choice != 'Q':
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
        print(' 5 - encrypt/decrypt file')
        print(' b - go back')
        print(' q - quit')
        print()
        print('Your choice: ', end='')

    @staticmethod
    def encrypt_decrypt_options():
        print('Choose option to perform:')
        print()
        print(' 1 - encrypt ECB - Electronic Codebook Mode')
        print(' 2 - decrypt ECB - Electronic Codebook Mode')
        print(' 3 - encrypt CBC - Cipher Block Chaining Mode')
        print(' 4 - decrypt CBC - Cipher Block Chaining Mode')
        print(' 5 - compare ECB, CBC and imported RSA soultion')
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

        def switch_encrypt_decrypt_menu():
            clear_terminal()
            self.active_menu = self.decrypt_encrypt_menu
            self.active_options = self.encrypt_decrypt_options

        switch = {
            '1': self.original_file.print_chunks,
            '2': switch_chunks_menu,
            '3': self.original_file.print_to_file,
            '4': self.original_file.perform_fft,
            '5': switch_encrypt_decrypt_menu,
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

    def decrypt_encrypt_menu(self):
        def encrypt_common(encrypt_func):
            self.original_file.chunks['IDAT'].display_data('data before encryption')
            self.DecryptEncryptAlgorithm = DecryptEncryptAlgorithm(1024)
            encrypted_data = getattr(self.DecryptEncryptAlgorithm, encrypt_func)(self.original_file.chunks['IDAT'].recon_data)

            new_idat_data = self.DecryptEncryptAlgorithm.separate_after_iend(encrypted_data[0])

            self.original_file.chunks['IDAT'].data = new_idat_data[0]
            self.original_file.chunks['IDAT'].recon_data = new_idat_data[0]

            self.after_iend_data = encrypted_data[1] + new_idat_data[1]
            self.data_after_encryption = new_idat_data[0]
            self.original_file.chunks['IDAT'].display_data('data after encryption with {}'.format(encrypt_func))

        def decrypt_common(decrypt_func):
            self.data_after_decryption = getattr(self.DecryptEncryptAlgorithm, decrypt_func)(self.data_after_encryption, self.after_iend_data)
            self.original_file.chunks['IDAT'].data = self.data_after_decryption
            self.original_file.chunks['IDAT'].recon_data = self.data_after_decryption
            self.original_file.chunks['IDAT'].display_data('data decrypted with {}'.format(decrypt_func))

        def encrypt_ecb():
            encrypt_common('encrypt_ecb')

        def encrypt_cbc():
            encrypt_common('encrypt_cbc')

        def decrypt_ecb():
            decrypt_common('decrypt_ecb')

        def decrypt_cbc():
            decrypt_common('decrypt_cbc')

        def compare():
            self.DecryptEncryptAlgorithm = DecryptEncryptAlgorithm(1024)
            encrypted_data_ebc = self.DecryptEncryptAlgorithm.encrypt_ecb(self.original_file.chunks['IDAT'].recon_data)

            new_idat_data = self.DecryptEncryptAlgorithm.separate_after_iend(encrypted_data_ebc[0])
            ecb_data_to_compare = new_idat_data[0]
            self.original_file.chunks['IDAT'].data = ecb_data_to_compare
            self.original_file.chunks['IDAT'].recon_data = ecb_data_to_compare

            self.original_file.chunks['IDAT'].display_data('data encrypted with {}'.format('ECB'))

            encrypted_data_ebc = self.DecryptEncryptAlgorithm.encrypt_cbc(self.original_file.chunks['IDAT'].recon_data)

            new_idat_data = self.DecryptEncryptAlgorithm.separate_after_iend(encrypted_data_ebc[0])
            cbc_data_to_compare = new_idat_data[0]
            self.original_file.chunks['IDAT'].data = cbc_data_to_compare
            self.original_file.chunks['IDAT'].recon_data = cbc_data_to_compare

            self.original_file.chunks['IDAT'].display_data('data encrypted with {}'.format('CBC'))

            encrypted_data_ebc = self.DecryptEncryptAlgorithm.encrypt_from_rsa_module(self.original_file.chunks['IDAT'].recon_data)

            new_idat_data = self.DecryptEncryptAlgorithm.separate_after_iend(encrypted_data_ebc[0])
            rsa_data_to_compare = new_idat_data[0]
            self.original_file.chunks['IDAT'].data = rsa_data_to_compare
            self.original_file.chunks['IDAT'].recon_data = rsa_data_to_compare

            self.original_file.chunks['IDAT'].display_data('data encrypted with {}'.format('RSA imported module'))

        def go_back():
            clear_terminal()
            self.active_menu = self.menu_file
            self.active_options = Menu.file_options

        switch = {
            '1': encrypt_ecb,
            '2': decrypt_ecb,
            '3': encrypt_cbc,
            '4': decrypt_cbc,
            '5': compare,
            'b': go_back,
            'q': exit,
        }
        choice = input('').lower()
        clear_terminal()
        switch.get(choice, Menu.invalid_option)()
