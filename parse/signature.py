def check_signature():
    sygnature = [137, 80, 78, 71, 13, 10, 26, 10]  # PNG sygnature
    sygnature_byte = 0

    while sygnature_byte < 8:
        if sygnature[sygnature_byte] != sygnature[sygnature_byte]:
            return False
        sygnature_byte += 1
    print("PNG file detected.")
    return True

