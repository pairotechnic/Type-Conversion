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
        self.endianness = None

    def show_png_chunk(self, file):
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

    def analyze_png_image(self):
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
                chunk_type = self.show_png_chunk(file)

        print("---------------------------------------------------------------------------------")

    def traverse_ifd_entries(self, file, ifd_entries_count_in_integers):
        for i in range(ifd_entries_count_in_integers) :

            tag = file.read(2)

            field_type_in_bytes = file.read(2)
            field_type_in_integers = int.from_bytes(field_type_in_bytes, byteorder = self.endianness)

            match field_type_in_integers : 
                case 1 :
                    field_type_in_string = "BYTE"
                    field_type_size_number_of_bytes = 1
                case 2 :
                    field_type_in_string = "ASCII"
                    field_type_size_number_of_bytes = 1
                case 3 :
                    field_type_in_string = "SHORT"
                    field_type_size_number_of_bytes = 2
                case 4 :
                    field_type_in_string = "LONG"
                    field_type_size_number_of_bytes = 4
                case 5 :
                    field_type_in_string = "RATIONAL"
                    field_type_size_number_of_bytes = 8

            print()

            number_of_values_in_bytes = file.read(4)
            number_of_values_in_integers = int.from_bytes(number_of_values_in_bytes, byteorder = self.endianness)

            size_of_all_values = field_type_size_number_of_bytes * number_of_values_in_integers
            value_or_offset_to_value_in_bytes = file.read(4)
            value_or_offset_to_value_in_integers = int.from_bytes(value_or_offset_to_value_in_bytes, byteorder = self.endianness)

            if size_of_all_values > 4 : 
                position_before_reading_values = file.tell()
                file.seek(value_or_offset_to_value_in_integers)
                values = file.read(size_of_all_values)
                print(values)

                # Here we need to do something with the values. 
                # Separate each value based on size of

                file.seek(position_before_reading_values)
            else : 
                values = value_or_offset_to_value_in_bytes

            print(tag, field_type_in_bytes, number_of_values_in_bytes, value_or_offset_to_value_in_bytes)

            print(f"Size of {field_type_in_string} : {field_type_size_number_of_bytes}")
            print(f"Number of values : {number_of_values_in_integers}")
            print(f"Total size of values : {size_of_all_values}")
    
    def traverse_ifds(self, file, offset_to_the_first_ifd_in_integers):

        offset_to_the_next_ifd_in_integers = offset_to_the_first_ifd_in_integers

        while offset_to_the_next_ifd_in_integers != 0 : 

            # Reset the cursor to offset to the first IFD
            file.seek(offset_to_the_next_ifd_in_integers)

            # Get the count of entries in the first IFD
            ifd_entries_count_in_binary = file.read(2)
            print("Number of entries in the first IFD : ")
            print(ifd_entries_count_in_binary)

            ifd_entries_count_in_integers = int.from_bytes(ifd_entries_count_in_binary, byteorder=self.endianness)
            print(f"{ifd_entries_count_in_integers}\n")

            self.traverse_ifd_entries(file, ifd_entries_count_in_integers)

            offset_to_the_next_ifd_in_bytes = file.read(4)
            print("\nOffset to the next IFD : ")
            print(f"{offset_to_the_next_ifd_in_bytes}")

            offset_to_the_next_ifd_in_integers = int.from_bytes(offset_to_the_next_ifd_in_bytes, byteorder = self.endianness)
            print(f"{offset_to_the_next_ifd_in_integers}")

    def analyze_tiff_image(self):
        '''
            We open the TIFF file as binary, and display its contents
        '''

        with open(self.img, 'rb') as file : 
            
            # Identify byte order (endianness) as Little Endian (II) or Big Endian (MM)
            endianness_code = file.read(2)
            print("\n")
            print("The type of endianness : ")
            print(endianness_code)

            if endianness_code == b'II':
                self.endianness = "little"
            elif endianness_code == b'MM':
                self.endianness = "big"
            print(f"{self.endianness}\n")
            
            # Verify the Magic Number for TIF ( 42 in decimal )
            magic_number_in_bytes = file.read(2)
            print("Magic Number : ")
            print(magic_number_in_bytes)

            magic_number_in_integers = int.from_bytes(magic_number_in_bytes, byteorder=self.endianness)
            print(f"{magic_number_in_integers}\n")

            assert magic_number_in_bytes == b'*\x00', 'Not a valid TIF file'

            # Get the bytes offset to the first IFD from the beginning of the file
            offset_to_the_first_ifd_in_bytes = file.read(4)
            print("Offset to the first IFD : ")
            print(offset_to_the_first_ifd_in_bytes)

            offset_to_the_first_ifd_in_integers = int.from_bytes(offset_to_the_first_ifd_in_bytes, byteorder=self.endianness)
            print(f"{offset_to_the_first_ifd_in_integers}\n")

            self.traverse_ifds(file, offset_to_the_first_ifd_in_integers)

            # Reset the cursor to offset to the beginning of the file
            file.seek(0)

            print(f"\nThe entire byte string of the tif : \n")
            print(file.read())

            '''
                TODO : 
                Figure out what the rest of the characters are in the bytestring other than the signature and IFDs
            '''

            

        print("---------------------------------------------------------------------------------")

def rough():
    '''
        This is a function where i can test out snippets before using it in my main code
    '''
    # byte_string = b'p\x03\x00\x00'
    # byte_string_in_integer = int.from_bytes(byte_string, byteorder='little')
    # print(byte_string_in_integer)

    from tifffile import TiffImage

    # Replace "your_byte_string" with the actual bytestring
    image = TiffImage(b'II*\x00<\x00\x00\x00\x80?\xe0O\xf0\x04\x16\r\x07\x84BaP\xb8\x1c\x12\x17\x0f\x88C q\x18\xa4V\x1b\x15\x8cC\xe2\xf1\x98\xe4\x1e7\x1d\x8e\xc7\xe4\x11\x99\x14\x8e-\x13\x93I%\x12\x98\xac\x04\x15\x00\xfe\x00\x04\x00\x01\x00\x00\x00\x00\x00\x00\x00\x00\x01\x04\x00\x01\x00\x00\x00\n\x00\x00\x00\x01\x01\x04\x00\x01\x00\x00\x00\n\x00\x00\x00\x02\x01\x03\x00\x04\x00\x00\x00>\x01\x00\x00\x03\x01\x03\x00\x01\x00\x00\x00\x05\x00\x00\x00\x06\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x11\x01\x04\x00\x01\x00\x00\x00\x08\x00\x00\x00\x15\x01\x03\x00\x01\x00\x00\x00\x04\x00\x00\x00\x16\x01\x04\x00\x01\x00\x00\x00\n\x00\x00\x00\x17\x01\x04\x00\x01\x00\x00\x004\x00\x00\x00\x1a\x01\x05\x00\x01\x00\x00\x00F\x01\x00\x00\x1b\x01\x05\x00\x01\x00\x00\x00N\x01\x00\x00\x1c\x01\x03\x00\x01\x00\x00\x00\x01\x00\x00\x00(\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00=\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00R\x01\x03\x00\x01\x00\x00\x00\x02\x00\x00\x00\x01\x03\x05\x00\x01\x00\x00\x00V\x01\x00\x00\x03\x03\x01\x00\x01\x00\x00\x00\x00\x00\x00\x00\x10Q\x01\x00\x01\x00\x00\x00\x01\x00\x00\x00\x11Q\x04\x00\x01\x00\x00\x00t\x12\x00\x00\x12Q\x04\x00\x01\x00\x00\x00t\x12\x00\x00\x00\x00\x00\x00\x08\x00\x08\x00\x08\x00\x08\x00\xc0\xd4\x01\x00\xe8\x03\x00\x00\xc0\xd4\x01\x00\xe8\x03\x00\x00\xa0\x86\x01\x00\x8f\xb1\x00\x00')

    # Access the first IFD
    first_ifd = image.asarray()[0]

    # Print the first IFD dictionary
    print(first_ifd)

def main():
    '''
        This is the code we want executed when we run this file directly
    '''

    png_path = "..\image_files\white_img_10_10.tif"
    ia = ImageAnalyzer(png_path)
    # ia.analyze_png_image()
    ia.analyze_tiff_image()

if __name__ == "__main__":
    '''
        If we directly run this file, then this code is executed
    '''
    main()
    # rough()