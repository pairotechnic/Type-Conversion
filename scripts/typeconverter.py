'''
    Purpose : To convert a file from base 64 png to base 64 tiff image format
    Author : Rohit Pai
    Date : 16/06/24
'''

# Standard Library Imports
import base64

# Third Party Imports
from PIL import Image

# Local Application Imports

class TypeConverter:
    '''
        1. Decode base64_png into png
        2. Convert png to tiff
        3. Encode tiff into base64_tiff
    '''

    def __init__(self, base64_png):
        
        self.base64_png = base64_png
        self.binary_png = None
        self.png = "..\image_files\sample_image.png"
        self.tiff = "..\image_files\sample_image.tiff"
        self.binary_tiff = None
        self.base64_tiff = None

    def decode_base64_png_to_png(self):
        '''
            The base 64 encoded string is decoded back to png imgage
            Each character in the byte string (A-Z, a-z, 0-9, +, /) is converted to 6 bits (0s and 1s)
        '''

        # Decode the Base64 PNG to binary data
        self.binary_png = base64.b64decode(self.base64_png)

        # Write the binary data to a PNG file
        with open(self.png, "wb") as file:
            file.write(self.binary_png)

    def convert_png_to_tiff(self):
        '''
            The pillow library allows us to convert PNG to TIFF
        '''

        # Open the PNG file
        png_image = Image.open(self.png)

        # Save as TIFF file
        png_image.save(self.tiff)

    def encode_tiff_to_base64_tiff(self):
        '''
            The tiff image is encoded to base64 tiff string
            6 bits at a time are converted to base64 characters
        '''

        # Open TIFF file in binary and get the binary data
        with open(self.tiff, "rb") as file:
            self.binary_tiff = file.read()

        # Encode the binary tiff data in base64, to make it compatible with protocols like mailing
        self.base64_tiff = base64.b64encode(self.binary_tiff)

        print("Base 64 tiff : \n")
        print(self.base64_tiff)

    def convert_base64_png_to_base64_tiff(self):
        '''
            To convert base64 png to base64 tiff, we first decode the png, change format to tiff, then encode to base64
        '''

        self.decode_base64_png_to_png()
        self.convert_png_to_tiff()
        self.encode_tiff_to_base64_tiff()

        return self.base64_tiff
    
    


def main():
    base64_png = input("Enter your base64 png byte string : ")
    type_converter = TypeConverter(base64_png)
    base64_tiff = type_converter.convert_base64_png_to_base64_tiff()
    print(base64_tiff)

if __name__ == "__main__":
    main()