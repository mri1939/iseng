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
    flagAndMask = {0x1b:0x60, 0x1c:0x40,0x1d:0x20,0x1e:0x30, 0x1f:0x00}
    mask = 0
    flag = 0
    txt = ''
    for i in bits:
        i = int(i,16)
        if i in flagAndMask:
            flag = i
            mask = flagAndMask[i]
            continue
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
        if ord(i) == 0x20:
            flag = 0x1d
            if flag != cur_flag:
                cur_flag = 0x1d
                txt += num2bit(flag)

        if ord(i) in range(0x30, 0x3a):
            flag = 0x1e
            if flag != cur_flag:
                cur_flag = 0x1e
                txt += num2bit(flag)
        # convert ke 5-bit terus tambahkan ke txt
        txt += num2bit(ord(i) & 0x1f)
    txt += num2bit(0x1f)
    return txt

def get_hex_bits(bits):
    return [hex(int(bits[i:i+5], 2)) for i in range(0, len(bits), 5)]

def embed(imagearray, data, seed):
    """
    Random LSB embedding using PRNG
    :param data : data to be embedded
    :param imagearray: cv2 image array
    :param seed : seed for the random generator
    :return : imagearray contains embedded data
    """
    rand.seed(seed) #random seed initialization
    height, width = imagearray.shape[:2] # get the size of the image
    layer = 1 #greyscale=1, rgb=3, rgba=4
    arr = np.resize(imagearray,(width*height*layer)) # make the array flat
    bits = get_bits(data); # get the bits string
    used = [] # list contains pixels that will have been used
    for bit in bits: #embed all the bits in to image
        while True: #find unused pixel
            r = rand.randint(0, len(arr))
            if r not in used:
                used.append(r)
                break
        if bit == '0': 
            arr[r] &= 0b11111110 # embed bit to the lsb
        elif bit == '1':
            arr[r] |= 0b00000001 # embed bit to the lsb
    arr = np.resize(arr,(height,width,layer)) #resize to the original image size
    return arr

def extract(imagearray, seed, bitlength):
    rand.seed(seed)
    height, width = imagearray.shape[:2]
    layer = 1 #greyscale=1, rgb=3, rgba=4
    arr = np.resize(imagearray,(width*height*layer))
    bits = ''
    used = []
    for count in xrange(bitlength):
        while True:
            r = rand.randint(0,len(arr))
            if r not in used:
                used.append(r)
                break
        bits += bin(arr[r])[-1:] # get the LSB bit and insert into the string
    hex_bits = get_hex_bits(bits) 
    txt = convert2txt(hex_bits) 
    return txt
              
text = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ 1234567890"
password = "24434"

image = cv2.imread('steg.png',cv2.IMREAD_UNCHANGED)
