import cv2
import numpy as np
import binascii
import random as rand

# self.height, self.width = self.image.shape[:2]


def num2bit(x):
    """
    Convert from 8bit to 5bit
    """
    return format(x, 'b').zfill(5)


def convert2txt(bits):
    flagAndMask = {0x1b:0x60, 0x1c:0x40,0x1d:0x20,0x1e:0x30}
    mask = 0
    flag = 0
    txt = ''
    for i in bits:
        i = int(i,16)
        if i in flagAndMask:
            flag = i
            mask = flagAndMask[i]
            continue
        """
        if flag == 0x1b or flag == 0x1c:
            txt+=chr(i^mask)
        if flag == 0x1d:
            txt+=chr(i^mask)
        if flag == 0x1e:
        """
        txt+=chr(i|mask)
    return txt

def get_bits(data):
    """
    Get the bits representation from the data.
    :param data : any string or binary data
    :type data : String
    :return : bits string
    :rtype : String
    """
    txt = ''
    cur_flag = 0
    for i in data:
        if ord(i) in range(0x61, 0x7b):
            flag = 0x1b
            if flag != cur_flag:
                cur_flag = 0x1b
                txt += num2bit(flag)
        if ord(i) in range(0x41, 0x5b):
            flag = 0x1c
            if flag != cur_flag:
                cur_flag = 0x1c
                txt += num2bit(flag)
        if ord(i) in range(0x20, 0x30):
            flag = 0x1d
            if flag != cur_flag:
                cur_flag = 0x1d
                txt += num2bit(flag)

        if ord(i) in range(0x30, 0x40):
            flag = 0x1e
            if flag != cur_flag:
                cur_flag = 0x1e
                txt += num2bit(flag)
        # convert ke 5-bit terus tambahkan ke txt
        print i
        txt += num2bit(ord(i) & 0x1f)
    txt += num2bit(0x1f)
    return txt


def embed(imagearray, data):
    """
    Random LSB embedding using PRNG
    :param data : data to be embedded
    :param imagearray: cv2 image array
    :param seed : seed for the random generator
    :return : imagearray contains embedded data
    """
    height, width = imagearray.shape[:2]  # get the size of the image
    layer = 1  # greyscale=1, rgb=3, rgba=4
    arr = np.resize(imagearray, (width*height*layer))  # make the array flat
    bits = get_bits(data)  # get the bits string
    i = 0
    for bit in bits:
        if bit == '0':
            arr[i] &= 0b11111110  # embed bit to the lsb
        elif bit == '1':
            arr[i] |= 0b00000001  # embed bit to the lsb
        i += 1
    # resize to the original image size
    arr = np.resize(arr, (height, width, layer))
    return arr


def extract(imagearray):
    height, width = imagearray.shape[:2]
    layer = 1  # greyscale=1, rgb=3, rgba=4
    arr = np.resize(imagearray, (width*height*layer))
    bits = ''
    flag = ''
    i = 0
    while True:
        if (i+1) % 5 == 0:  # periksa 5-bit terkakhir yang dibaca
            if hex(int(flag, 2)) == 0x1F:  # jika flag = 0x1F keluar dari looping
                break
        bits += bin(arr[i])[-1:]  # get the LSB bit and insert into the string
        flag += bin(arr[i])[-1:]  # untuk pemeriksaan flag
        i += 1
    # convert the bits string to 8 bit binary format
    char_bits = [bits[i:i+5] for i in xrange(0, i, 5)]
    txt = convert2txt(char_bits)
    return txt


# embedding

#secret = ""
#image = cv2.imread('lena.png',cv2.IMREAD_UNCHANGED)
#seed = 24434
#stegimage = embed(image,secret,seed)
# cv2.imwrite('steg.png',stegimage)

# extracting
"""
seed = 24434
image = cv2.imread('steg.png',cv2.IMREAD_UNCHANGED)
bitlength = 15*8 # the embedded string is 15 chars long, 1 char = 8bit
secret = extract(image,seed,bitlength)
print "The Secret Message is :",secret
"""
bits = get_bits("mantapmantapbang123123!@#&APASIH")
# convert the bits string to 8 bit binary format
char_bits = [hex(int(bits[i:i+5], 2)) for i in xrange(0, len(bits), 5)]
print char_bits 
print convert2txt(char_bits)
