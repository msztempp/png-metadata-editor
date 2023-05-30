from menu import Menu

# https://www.w3.org/TR/2003/REC-PNG-20031110/#5Chunk-layout


# TODO:
# Critical:
# IHDR PLTE IDAT IEND
# Anicillary:
# tEXT
# zamiast tEXT mozna iTXT, serializowany xmp
# sprawdzenie czy jest, jesli nie ( klucz, wartosc )
# jeesli jest xmp, pobieral xml -> formatuje i wpisuje na konsole
# PLTE czy jest roznie przetrwarzana, zaleznie od pliku bit_deph and color type
# GAMA
# tIME
# sRGB
# tRNS


if __name__ == "__main__":
    test = Menu()
    test.start()

