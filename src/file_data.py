import os
from chunk import Chunk
from src.chunks.anicillary.chrm import CHRM
from src.chunks.anicillary.itxt import ITXT
from src.chunks.anicillary.srgb import SRGB
from src.chunks.anicillary.text import TEXT
from src.chunks.anicillary.trns import TRNS
from src.chunks.anicillary.time import TIME
from src.chunks.critical.ihdr import IHDR
from src.chunks.critical.plte import PLTE
from src.chunks.critical.idat import IDAT
from src.chunks.critical.iend import IEND
from src.chunks.anicillary.gama import GAMMA
import cv2
import numpy as np
from matplotlib import pyplot as plt
from check_signature import check_signature


class File:
    def __init__(self, pathname):
        self.file_name = None
        self.chunks_indices = None
        self.byte_data = None
        self.name_without_extension = None
        self.pathname = pathname
        self.chunks = {}
        self.load_and_get_name(pathname)
        self.find_chunks()
        self.init_chunks()

    def load_and_get_name(self, pathname):
        try:
            #pathname = pathname.lower()
            self.file_name = os.path.basename(pathname)
            self.name_without_extension = os.path.splitext(self.file_name)[0]

            png_file = open(pathname, 'rb')
            self.byte_data = png_file.read()
            if not check_signature(self.byte_data):
                raise Exception('Incorrect file format'
                                '\nThis program is strictly for analyzing PNG files.')
            png_file.close()
        except Exception as e:
            print(str(e))
            choice = input("Would you like to try again? ('yes' to try again): ")
            if choice.lower() == "yes":
                from menu import Menu
                menu = Menu()
                menu.start()
            else:
                print("Exiting program...")
                exit()

    def find_chunks(self):
        found_chunks = {'critical': {}, 'ancillary': {}}
        i = 0
        while self.byte_data[i:i + 1]:
            chunk_type_bytes = self.byte_data[i:i + 4]
            if chunk_type_bytes in chunks_types:
                chunk_type_str = chunk_type_bytes.decode('utf-8')
                if chunk_type_str in found_chunks['critical'].keys():
                    found_chunks['critical'][chunk_type_str].append(i - 4)
                else:
                    found_chunks['critical'][chunk_type_str] = [i - 4]
                i += 4
            else:
                i += 1
        self.chunks_indices = found_chunks

    def get_chunk_data(self, index):
        start = index
        length = int.from_bytes(self.byte_data[start:start + 4], 'big')
        end = start + length + 12
        return self.byte_data[start:end]

    def get_chunks(self):
        for chunks_dict in self.chunks_indices.values():
            for chunk_type in chunks_dict.keys():
                for instance_index in chunks_dict[chunk_type]:
                    if chunk_type in self.chunks.keys():
                        if type(self.chunks[chunk_type]) != list:
                            self.chunks[chunk_type] = [self.chunks[chunk_type]]
                        self.chunks[chunk_type].append(self.get_chunk_data(instance_index))
                    else:
                        self.chunks[chunk_type] = self.get_chunk_data(instance_index)

    def init_chunks(self):
        self.get_chunks()  # Initialize self.chunks with raw_bytes
        is_plte = False
        for chunk_type, chunk_value in self.chunks.items():
            if chunk_type == 'IHDR':
                self.chunks[chunk_type] = IHDR(chunk_value)
            elif chunk_type == 'PLTE':
                self.chunks[chunk_type] = PLTE(chunk_value, self.chunks['IHDR'].color_type)
                is_plte=True
            elif chunk_type == 'IEND':
                self.chunks[chunk_type] = IEND(chunk_value)
            elif chunk_type == 'gAMA':
                self.chunks[chunk_type] = GAMMA(chunk_value)
            elif chunk_type == 'tEXt':
                if isinstance(chunk_value, list):
                    chunk_list = [Chunk(chunk) for chunk in chunk_value]
                    self.chunks[chunk_type] = TEXT(chunk_list)
                else:
                    self.chunks[chunk_type] = TEXT(chunk_value)
            elif chunk_type == 'cHRM':
                self.chunks[chunk_type] = CHRM(chunk_value)
            elif chunk_type == 'iTXt':
                self.chunks[chunk_type] = ITXT(chunk_value)
            elif chunk_type == 'sRGB':
                self.chunks[chunk_type] = SRGB(chunk_value)
            elif chunk_type == 'tRNS':
                if is_plte:
                    self.chunks[chunk_type] = TRNS(chunk_value, self.chunks['IHDR'].color_type,self.chunks['PLTE'].entries)
                else:
                    self.chunks[chunk_type] = TRNS(chunk_value, self.chunks['IHDR'].color_type, None)
            elif chunk_type == 'tIME':
                self.chunks[chunk_type] = TIME(chunk_value)
            elif chunk_type == 'IDAT':
                if isinstance(chunk_value, list):
                    chunk_list = [Chunk(chunk) for chunk in chunk_value]
                    self.chunks[chunk_type] = IDAT(chunk_list, self.chunks['IHDR'].width,
                                                   self.chunks['IHDR'].height, self.chunks['IHDR'].color_type)
                else:
                    self.chunks[chunk_type] = IDAT(chunk_value, self.chunks['IHDR'].width,
                                                   self.chunks['IHDR'].height, self.chunks['IHDR'].color_type)
            else:
                if isinstance(chunk_value, list):
                    chunk_list = [Chunk(chunk) for chunk in chunk_value]
                    self.chunks[chunk_type] = Chunk(is_chunk_list=chunk_list)
                else:
                    self.chunks[chunk_type] = Chunk(chunk_value)

    def print_chunks(self):
        for chunk in self.chunks.values():
            chunk.print_basic_info()

    def print_to_file(self):
        folder_path = '../img-anonymized'
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        new_name = os.path.join(folder_path, '{}_anonymized.png'.format(self.name_without_extension))
        tmp_png = open(new_name, 'wb')
        tmp_png.write(self.byte_data[:8])
        for chunk_type in self.chunks_indices['critical'].values():
            for instance_index in chunk_type:
                chunk_data = self.get_chunk_data(instance_index)
                tmp_png.write(chunk_data)
        print('Saved only with critical chunks to:\n', new_name)
        print()
        tmp_png.close()

    def perform_fft(self):
        img = cv2.imread(self.pathname)

        # Split channels
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blue_channel, green_channel, red_channel = cv2.split(img)

        # Compute and display DFT magnitude and phase for each channel
        channels = [(gray, 'Gray'), (red_channel, 'Red'), (green_channel, 'Green'), (blue_channel, 'Blue')]
        for channel, channel_name in channels:
            # Compute DFT
            img_float32 = np.float32(channel)
            dft = cv2.dft(img_float32, flags=cv2.DFT_COMPLEX_OUTPUT)
            dft_shift = np.fft.fftshift(dft)

            # Compute magnitude and phase
            magnitude_spectrum, phase_spectrum = cv2.cartToPolar(dft_shift[:, :, 0], dft_shift[:, :, 1])
            magnitude_spectrum += np.finfo(float).eps
            magnitude_spectrum = 20 * np.log(magnitude_spectrum)

            # Display magnitude and phase
            plt.figure(channel_name + " channel")
            plt.subplot(121), plt.imshow(magnitude_spectrum, cmap='gray')
            plt.title('Magnitude Spectrum'), plt.xticks([]), plt.yticks([])
            plt.subplot(122), plt.imshow(phase_spectrum, cmap='gray')
            plt.title('Phase Spectrum'), plt.xticks([]), plt.yticks([])
            plt.suptitle(channel_name + ' channel')
            plt.show()

        cv2.waitKey(0)
        print('Performed FFT on image:', self.file_name + ' on 4 channels(RGB) and gray')
        print()


chunks_types = [b'IHDR', b'PLTE', b'IDAT', b'IEND', b'gAMA',b'cHRM',b'sRGB',b'tRNS', b'tIME',b'tEXt',b'iTXt']
