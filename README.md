# PNG Metadata and Encryption Tool

## Overview
This tool provides a command-line interface for handling PNG files, focusing on reading, editing metadata, and performing encryption and decryption operations. It is designed to assist users in managing the data embedded in PNG files, particularly useful for developers, data analysts, and security experts who need to manipulate image data securely.

## Features

### Read and Edit PNG Chunks
- **Access and Modify Specific Parts**: Manage both critical and ancillary chunks within the PNG file structure.
- **Supported Critical Chunks**: `IHDR`, `PLTE`, `IDAT`, `IEND`
- **Supported Ancillary Chunks**: `gAMA`, `cHRM`, `sRGB`, `tRNS`, `tIME`, `tEXt`, `iTXt`, `sBIT`, `pHYs`

### Encryption and Decryption
- **Encryption Modes**: Support for ECB (Electronic Codebook) and CBC (Cipher Block Chaining) encryption methods to ensure secure data handling.
- **ECB (Electronic Codebook Mode)**: Encrypts each block of data independently, which can be advantageous for parallel processing but may be vulnerable to certain types of analysis if patterns are present in the data.
- **CBC (Cipher Block Chaining Mode)**: Each block of plaintext is XORed with the previous ciphertext block before being encrypted. This method uses an initialization vector to add randomness to the encryption process, enhancing security against patterns in the plaintext.

### Critical Chunks Details
- **IHDR (Image Header)**: Contains key image information like width, height, bit depth, and color type.
- **PLTE (Palette)**: Contains the palette table if the image is indexed.
- **IDAT (Image Data)**: Contains the actual image data which is compressed.
- **IEND (Image End)**: Marks the end of the PNG datastream.

### Ancillary Chunks Details
- **gAMA, cHRM, sRGB**: Related to color management.
- **tRNS**: Contains transparency information.
- **tIME**: Stores the last modification time.
- **tEXt, iTXt**: Used for storing text data.
- **sBIT**: Specifies the significant bits.
- **pHYs**: Holds physical pixel dimensions.

## Using the Tool
To utilize this tool, users need to run the program from the command line, follow the interactive prompts to select PNG files, and perform desired operations like viewing chunk details or applying encryption and decryption.
