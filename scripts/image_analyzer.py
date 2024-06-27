'''
    Purpose : To analyze the structure of any given image file
    Author : Rohit Pai
    Date : 25/6/24
'''

# Standard Library Imports

# Third Party Imports

# Local Application Imports

class ImageAnalyzer:
    '''
        Displays the internal structure of an image (png, tiff, etc)
    '''

    def __init__(self, img_path):

        self.img = img_path

    def show_chunk(self, file):
        '''
            Displays the 4 parts of any given chunk : Size of data, Type, Data, CRC
        '''
        # Show the size of chunk data ( takes up 4 bytes )
        chunk_data_size_in_bytes = file.read(4)
        print(chunk_data_size_in_bytes)

        # Convert size of chunk data from byte string to integer
        chunk_data_size_in_integers = int.from_bytes(chunk_data_size_in_bytes, byteorder='big')
        print(chunk_data_size_in_integers)

        # Show the chunk type ( eg : IHDR, PLTE, IDAT, IEND ) (takes up 4 bytes)
        chunk_type = file.read(4)
        print(chunk_type)

        # Show the chunk data ( takes up as many bytes as specified in chunk data size)
        chunk_data = file.read(chunk_data_size_in_integers)
        print(chunk_data)

        # Show the CRC ( takes up 4 bytes )
        chunk_crc = file.read(4)
        print(chunk_crc)

        return chunk_type

    def analyze_image(self):
        '''
            We open the PNG file as binary, traverse through and display all of its chunks
        '''

        with open(self.img, 'rb') as file :
        
            # Show PNG signature ( Read first 8 bytes )
            signature = file.read(8)
            assert signature == b'\x89PNG\r\n\x1a\n', "Not a valid PNG file"
            print(signature)

            chunk_type = None
            while chunk_type != b'IEND': 
                chunk_type = self.show_chunk(file)

        print("---------------------------------------------------------------------------------")


def main():
    '''
        This is the code we want executed when we run this file directly
    '''

    png_path = "..\image_files\white_img.png"
    ia = ImageAnalyzer(png_path)
    ia.analyze_image()

if __name__ == "__main__":
    '''
        If we directly run this file, then this code is executed
    '''
    main()