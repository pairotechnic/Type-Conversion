import base64

'''
    Convert letters to hex
    Convert hex to bits
    Convert bits to base64
'''

my_text = "Hello World"

my_text = my_text.encode("ascii")

my_text_b64 = base64.b64encode(my_text)

# print(my_text_b64)

# print(base64.b64decode(my_text_b64))

with open("..\image_files\strawberry.png", "rb") as f:
    data = f.read()

transmitted_data = base64.b64encode(data)

print(transmitted_data)

# data = base64.b64decode(transmitted_data)

# with open("..\image_files\copy_of_hello_world.png", "wb") as f:
#     f.write(data)

