import cv2
import numpy as np
import binascii
import random as rand
from Crypto.Cipher import DES,DES3,AES

# self.height, self.width = self.image.shape[:2]

def des_encrypt(key,iv,plain):
    mydes = DES.new(key,DES.MODE_CBC,iv)
    return mydes.encrypt(plain)

def des_decrypt(key,iv,cipher):
    mydes = DES.new(key,DES.MODE_CBC,iv)
    return mydes.decrypt(cipher)

def get_bits(data):
    """
    Get the bits representation from the data.
    :param data : any string or binary data
    :type data : String
    :return : bits string
    :rtype : String
    """
    return ''.join(format(ord(i),'b').zfill(8) for i in data)

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

def extract(imagearray,seed, bitlength):
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
    char_bits = [bits[i:i+8] for i in xrange(0,bitlength,8)] # convert the bits string to 8 bit binary format
    txt = ''.join(chr(int(x,2)) for x in char_bits) # convert 8 binary to integer then parse to char
    return txt


#embedding

plaindata = ""
key = ""
iv = "\x00\x00\x00\x00\x00\x00\x00\x00"
#secret = des_encrypt(key,iv,plaindata)
#print "Pajang data",len(secret)
#image = cv2.imread('lena.png',cv2.IMREAD_UNCHANGED)
#seed = 24434
#stegimage = embed(image,secret,seed)
#cv2.imwrite('steg.png',stegimage)

#extracting

seed = 24434
image = cv2.imread('steg.png',cv2.IMREAD_UNCHANGED)
bitlength = 16*8 # the embedded string is 15 chars long, 1 char = 8bit
secret = extract(image,seed,bitlength)
plain = des_decrypt(key,iv,secret)
print "The Secret Message is :",plain
