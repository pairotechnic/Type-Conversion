'''
    Purpose : To analyze the structure of any given image file
    Author : Rohit Pai
    Date : 25/6/24
'''

# Standard Library Imports
import struct
import zlib
import datetime

# Third Party Imports
import pytz

# Local Application Imports

class ImageAnalyzer:
    '''
        Displays the internal structure of an image (png, tiff, etc)
    '''

    def __init__(self):

        self.png = "..\image_files\hello_world.png"
        self.tiff = "..\image_files\sample_image.tiff"

        self.img = "..\image_files\white_img.png"
        self.filetype = None

    def identify_image_format(self):
        '''
            Analyze the starting characters of the imae file to identify the type of the file
            Eg : 
                PNG starts with 89 50 4E 47 0D 0A 1A 0A

        '''

        with open(self.img, 'rb') as file :
            content = file.read()

        if content[:8] == b'\x89PNG\r\n\x1a\n' :
            self.filetype = "PNG"
        
        if self.filetype is not None : 
            print(f"The format of your image is : {self.filetype}")

    def analyze_png_image(self):

        with open(self.png, 'rb') as file :
            content = file.read()
        
        # Check if the file starts with the correct PNG signature
        print("\nA PNG file should start with : ")
        print(b'\x89PNG\r\n\x1a\n')

        first_8_characters = content[:8]

        print("\nFirst 8 characters of your image : ")
        print(first_8_characters)

        if first_8_characters == b'\x89PNG\r\n\x1a\n':
            print("\nThis is a PNG file.")
        else :
            print("\nThis is not a PNG file")

        # Print the first few bytes to see the IHDR chunk
        # print("These are the bytes of your image: ")
        # print(content[:1000])
        print(content)
        # print(content.find(b'IHDR'))

        # for x in content[:20] :
        #     print(x)

        # for part in content :
        #     print(part, end="")

        print("---------------------------------------------------------------------------------")

    def parse_png(self, file_path):
        with open(file_path, 'rb') as f:
            # Read the PNG signature
            signature = f.read(8)
            assert signature == b'\x89PNG\r\n\x1a\n', "Not a valid PNG file"
            
            # Read the IHDR chunk
            ihdr_length = int.from_bytes(f.read(4), byteorder='big')
            ihdr_data = f.read(ihdr_length)
            ihdr_data = ihdr_data.decode('utf-8').split('\n')
            width, height = map(int, ihdr_data[1].split(': ')[1].split(' '))
            color_type = int(ihdr_data[3].split(': ')[1])
            
            # Read the PLTE chunk for indexed color
            if color_type == 0:
                plte_length = int.from_bytes(f.read(4), byteorder='big')
                plte_data = f.read(plte_length)
                # Extract palette colors here
            
            # Skip to the IDAT chunk
            idat_length = int.from_bytes(f.read(4), byteorder='big')
            idat_data = f.read(idat_length)
            
            return width, height, color_type, idat_data
        
    # def create_tiff(width, height, color_type, idat_data, output_file_path):
    #     with open(output_file_path, 'wb') as tiff_file:
    #         # Write TIFF header
    #         tiff_file.write(b'II*\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0```

    

    def read_png(self, filename):
        with open(filename, 'rb') as f:
            # Check PNG signature
            signature = f.read(8)
            assert signature == b'\x89PNG\r\n\x1a\n', "Not a valid PNG file"

            chunks = []
            while True:
                chunk_header = f.read(8)
                if len(chunk_header) < 8:
                    break
                length, chunk_type = struct.unpack('>I4s', chunk_header)
                chunk_data = f.read(length)
                crc = f.read(4)
                chunks.append((chunk_type, chunk_data))

                if chunk_type == b'IEND':
                    break

        return chunks

    def write_tiff(self, image_data, width, height, bpp, filename):
        with open(filename, 'wb') as f:
            # TIFF header
            f.write(b'II')  # Little-endian
            f.write(struct.pack('<H', 42))  # Magic number
            f.write(struct.pack('<I', 8))  # Offset to first IFD

            # Image File Directory (IFD)
            ifd_entries = [
                (256, 4, 1, width),  # ImageWidth
                (257, 4, 1, height),  # ImageLength
                (258, 3, 1, bpp),  # BitsPerSample
                (259, 3, 1, 1),  # Compression (none)
                (262, 3, 1, 2),  # PhotometricInterpretation (RGB)
                (273, 4, 1, 8 + 2 + 12 * 6),  # StripOffsets
                (277, 3, 1, 3),  # SamplesPerPixel
                (278, 4, 1, height),  # RowsPerStrip
                (279, 4, 1, len(image_data)),  # StripByteCounts
            ]

            f.write(struct.pack('<H', len(ifd_entries)))  # Number of IFD entries
            for tag, type, count, value in ifd_entries:
                f.write(struct.pack('<HHII', tag, type, count, value))

            # Offset to next IFD (none)
            f.write(struct.pack('<I', 0))

            # Image data
            f.write(image_data)

    def png_to_tiff(self, png_filename, tiff_filename):
        chunks = self.read_png(png_filename)

        ihdr = None
        idat = b''

        for chunk_type, chunk_data in chunks:
            if chunk_type == b'IHDR':
                ihdr = chunk_data
            elif chunk_type == b'IDAT':
                idat += chunk_data

        if ihdr is None:
            raise ValueError("Missing IHDR chunk")

        width, height, bit_depth, color_type, compression, filter, interlace = struct.unpack('>IIBBBBB', ihdr)

        if bit_depth != 8:
            raise ValueError("Only 8-bit images are supported")

        if color_type not in (2, 0):
            raise ValueError("Only grayscale or RGB images are supported")

        # Decompress IDAT chunk
        image_data = zlib.decompress(idat)

        # Remove filter bytes (one per scanline)
        if color_type == 2:  # RGB
            bpp = 24
            stride = width * 3
        elif color_type == 0:  # Grayscale
            bpp = 8
            stride = width

        raw_image_data = bytearray()
        for y in range(height):
            raw_image_data.extend(image_data[y * (stride + 1) + 1:y * (stride + 1) + 1 + stride])

        self.write_tiff(raw_image_data, width, height, bpp, tiff_filename)


def main():
    png_path = "..\image_files\hello_world.png"
    ia = ImageAnalyzer()
    # ia.identify_image_format()

    ia.analyze_png_image()
    # ia.parse_png(png_path)

if __name__ == "__main__":
    main()