import chunk
import signature
import chunk_decoder


def menu():
    file_input = False
    while not file_input:
        file = input("Input a name of the PNG image or type quit:\n")
        if file == "quit":
            print("Naura.")
            return 0
        file_path = "../img-example/" + file
        chunks_from_file = []
        try:
            with open(file_path, 'rb') as f:
                byte_data = f.read()

                if not signature.check_signature(byte_data):
                    print("Invalid signature, it is not a PNG file. Try again!\n")
                else:
                    print("File read successfully.")

                    file_input = True
                    chunk_index = 8
                    while chunk_index != (-1):
                        chunks_from_file.append(chunk.read_chunk(byte_data, chunk_index))
                        chunk_index = chunks_from_file[-1].next_index

        except OSError as e:
            print("Error: Unable to locate the file '" + file_path + "'. Please check the file path and try again.")
            print("Detailed error message: " + str(e) + "\n")
    option = False

    while not option:
        print("\n Menu:")
        print("1. View image data.")
        menu_choice = int(input("Choose option: "))
        if menu_choice == 1:
            print("Image data:")
        else:
            print("Wrong option, try again.")


def main():
    menu()


if __name__ == "__main__":
    main()
