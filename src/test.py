import struct
import zlib
import matplotlib.pyplot as plt
import numpy as np

# https://pyokagan.name/blog/2019-10-14-png/
# https://www.w3.org/TR/PNG/#5Chunk-layout
file = open('../img-example/basn6a08.png', 'rb')

# PNG Signature - czyli pierwsze 8 bajtów pliku
PngSignature = b'\x89PNG\r\n\x1a\n'
if file.read(len(PngSignature)) != PngSignature:
    raise Exception('Invalid PNG Signature')


# po PNG signature mamy juz tylko chunki do konca pliku maja one nastepujaca strukture:
# 4 bajty - dlugosc chunka(nie moze byc zerem)
# 4 bajty - typ chunka(tutaj idk co do zera)
# dlugosc chunka bajtow - dane chunka, 4 bajty
# CRC(Cyclic Redundancy Code)- suma kontrolna, sprawdza czy dane chunka sa poprawne
# wszystkie chunki sa niezalezne od siebie, wiec mozna je czytac w dowolnej kolejnosci
# chunki mogą sie powtarzac, ale tylko wtedy gdy sa to chunki o roznych typach
# chunki mogą sie nakladac na siebie, ale tylko wtedy gdy sa to chunki o roznych typach
# chunki sa przechowywane w big endian format (najbardziej znaczacy bajt jest pierwszy)
# chunki moga byc dowolnej dlugosci, ale nie moga byc dluzsze niz 2^31 bajtow

def read_chunk(f):
    # Returns (chunk_type, chunk_data)
    chunk_length, chunk_type = struct.unpack('>I4s', f.read(8))
    chunk_data = f.read(chunk_length)
    checksum = zlib.crc32(chunk_data, zlib.crc32(struct.pack('>4s', chunk_type)))
    chunk_crc, = struct.unpack('>I', f.read(4))
    if chunk_crc != checksum:
        raise Exception('chunk checksum failed {} != {}'.format(chunk_crc,
                                                                checksum))
    return chunk_type, chunk_data


# chunk IEND - koniec pliku

chunks = []
while True:
    chunk_type, chunk_data = read_chunk(file)
    chunks.append((chunk_type, chunk_data))
    if chunk_type == b'IEND':
        break

print([chunk_type for chunk_type, chunk_data in chunks])
# daje to nam liste wszystkich chunkow w pliku
# [b'IHDR', b'gAMA', b'IDAT', b'IEND']

# IHDR - naglowek pliku, musi byc pierwszym chunkiem w pliku, zawiera podstawowe informacje o pliku takie jak:
# rozmiar, typ, glebia kolorow, metoda kompresji, metoda filtracji, metoda interlacingu
# gAMA - gamma obrazu, zawiera wartosc gamma obrazu, jesli nie ma tego chunka to zaklada sie ze gamma wynosi 1/2.2
# IDAT - dane obrazu, zawiera skompresowane dane obrazu, moze byc wiele chunkow IDAT, jest on wymagany
# IEND - koniec pliku, musi byc ostatnim chunkiem w pliku, nie zawiera zadnych danych

# PNG dzielimy na 2 typy chunkow:
# critial(krytyczne) - te chunki musza byc w pliku i musza byc w odpowiedniej kolejnosci oraz musza byc przeprocesowane przez odbiorce
# anicillary(pomocnicze) - opcjonalne i odbiorca moze je przetworzyc albo i nie, nie maja one zadnego wplywu na obraz
# generalnie jak cos jest upper casem to jest to critial chunk, a jak lower casem to anicillary chunk
# specyfikacja PNG specyfikuje liste chunkow i jak je interpretowac, jednak to nie jest jakas sztywna lista bo mozemy dodac swoje chunki
# w ten sposob np Adobe dodal swoje chunki do PNG, zeby sie ich nie dalo przegladac przez inne apki

# IHDR - Image Header ma zawsze 13 bajtow i zawiera nastepujace informacje:
# 4 bajty - szerokosc obrazu w pikselach, nie moze byc zerem
# 4 bajty - wysokosc obrazu w pikselach, nie moze byc zerem

# 1 bajt - glebia kolorow, moze byc 1, 2, 4, 8, 16, 24, 32, 48, 64
# PNG Image Type	Color type	Allowed bit depths	Interpretation
# Grayscale	0	1, 2, 4, 8, 16	Each pixel is a grayscale sample.
# Truecolor	2	8, 16	Each pixel is a R,G,B triple.
# Indexed-color	3	1,2,4,8	Each pixel is a palette index; a PLTE chunk shall appear.
# Grayscale with alpha	4	8, 16	Each pixel is a grayscale sample followed by an alpha sample.
# Truecolor with alpha	6	8, 16	Each pixel is a R,G,B triple followed by an alpha sample.


# 1 bajt - typ koloru, moze byc 0 - grayscale, 2 - RGB, 3 - indexed, 4 - grayscale + alpha, 6 - RGB + alpha
# 1 bajt - metoda kompresji
# 1 bajt - metoda filtracji, moze byc 0 - adaptive filtering with five basic filter types, 1 - no filtering
# 1 bajt - metoda przeplotu, moze byc 0 - no interlacing, 1 - Adam7 interlacing

_, IHDR_data = chunks[0]  # IHDR is always first chunk
width, height, bitd, colort, compm, filterm, interlacem = struct.unpack('>IIBBBBB', IHDR_data)

if compm != 0:
    raise Exception('invalid compression method')
if filterm != 0:
    raise Exception('invalid filter method')
if colort != 6:
    raise Exception('we only support truecolor with alpha')
if bitd != 8:
    raise Exception('we only support a bit depth of 8')
if interlacem != 0:
    raise Exception('we only support no interlacing')

print(width, height)

# IDAT chunk

# png sklada sie z scanlines, kazdy scanline sklada sie z RGBA 8 bitowych pikseli
# gdzie kazdy piksel sklada sie z 4 kanalow R, G, B, A, gdzie A to alpha, czyli przezroczystosc
# scanline jest dlugosci width * 4, bo kazdy piksel ma 4 kanaly
# scanline jest dlugosci width * 4 + 1, bo na poczatku jest jeden bajt na filtr

raw_image_data = [
    [255, 0, 0, 255, 0, 0, 255, 255],  # First scanline, zawiera dwa tuple po 4 kanaly
    [0, 255, 0, 255, 255, 255, 255, 255],  # Second scanline, tak samo jak wyzej
]

filtered_image_data = [
    [0, 255, 0, 0, 255, 0, 0, 255, 255],  # First scanline, first item (0) specifies filter type 0
    [0, 0, 255, 0, 255, 255, 255, 255, 255],  # Second scanline, first item (0) specifies filter type 0
]

# Konsolidacja danych IDAT
# dane są przechoiwywane w kawałkach IDAT, rozdzielionych na wiele kawałków, także trzeba wszystkie połączyć


IDAT_data = b''.join(chunk_data for chunk_type, chunk_data in chunks if chunk_type == b'IDAT')
IDAT_data = zlib.decompress(IDAT_data)

print(len(IDAT_data))


# wychodzi nam 4128, bo width = 32, height = 32, bytes per pixel = 4, wiec 32 * 32 * 4 = 4096, a 4096 + 32 = 4128

# Filtrowanie 
# filtrujemy dane, zeby je skompresowac, filtrujemy kazdy scanline osobno

# Type  | Name	    | Filter Function	                                               | Reconstruction Function
# 0	    | None	    | Filt(x) = Orig(x)	                                               | Recon(x) = Filt(x)
# 1	    | Sub	    | Filt(x) = Orig(x) - Orig(a)	                                   | Recon(x) = Filt(x) + Recon(a)
# 2	    |Up	        | Filt(x) = Orig(x) - Orig(b)	                                   | Recon(x) = Filt(x) + Recon(b)
# 3	    |Average	| Filt(x) = Orig(x) - floor((Orig(a) + Orig(b)) / 2)	           | Recon(x) = Filt(x) + floor((Recon(a) + Recon(b)) / 2)
# 4	    |Paeth	    | Filt(x) = Orig(x) - PaethPredictor(Orig(a), Orig(b), Orig(c))    | Recon(x) = Filt(x) + PaethPredictor(Recon(a), Recon(b), Recon(c))
# Gdzie :
# x to aktualny bajt
# a jest bajtem odpowiadającym x w pikselu bezpośrednio przed pikselem zawierającym x (lub 0, jeśli taki piksel jest poza granicami obrazu)
# b jest bajtem odpowiadającym x w poprzednim wierszu obrazu (lub 0, jeśli taki wiersz nie istnieje)
# c jest bajtem odpowiadającym x w poprzednim wierszu i pikselu bezpośrednio przed pikselem zawierającym x (lub 0, jeśli taki wiersz i piksel nie istnieją)

# def PaethPredictor(a, b, c):
#     p = a + b - c
#     pa = abs(p - a)
#     pb = abs(p - b)
#     pc = abs(p - c)
#     if pa <= pb and pa <= pc:
#         Pr = a
#     elif pb <= pc:
#         Pr = b
#     else:
#         Pr = c
#     return Pr


Recon = []
bytesPerPixel = 4
stride = width * bytesPerPixel


def Recon_a(r, c):
    return Recon[r * stride + c - bytesPerPixel] if c >= bytesPerPixel else 0


def Recon_b(r, c):
    return Recon[(r - 1) * stride + c] if r > 0 else 0


def Recon_c(r, c):
    return Recon[(r - 1) * stride + c - bytesPerPixel] if r > 0 and c >= bytesPerPixel else 0


i = 0
for r in range(height):  # for each scanline
    filter_type = IDAT_data[i]  # first byte of scanline is filter type
    i += 1
    for c in range(stride):  # for each byte in scanline
        Filt_x = IDAT_data[i]
        i += 1
        if filter_type == 0:  # None
            Recon_x = Filt_x
        elif filter_type == 1:  # Sub
            Recon_x = Filt_x + Recon_a(r, c)
        elif filter_type == 2:  # Up
            Recon_x = Filt_x + Recon_b(r, c)
        elif filter_type == 3:  # Average
            Recon_x = Filt_x + (Recon_a(r, c) + Recon_b(r, c)) // 2
        elif filter_type == 4:  # Paeth
            Recon_x = Filt_x + PaethPredictor(Recon_a(r, c), Recon_b(r, c), Recon_c(r, c))
        else:
            raise Exception('unknown filter type: ' + str(filter_type))
        Recon.append(Recon_x & 0xff)  # truncation to byte

plt.imshow(np.array(Recon).reshape((height, width, 4)))
plt.show()
