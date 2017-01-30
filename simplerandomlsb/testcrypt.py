from Crypto.Cipher import DES, DES3
from Crypto import Random
import binascii
key = b'Ellawara'
iv = '\x00\x00\x00\x00\x00\x00\x00\x00'
cipher = DES.new(key,DES.MODE_CBC,iv)
plaintext = b'Mukhlas Rosyadi\x00'
c = cipher.encrypt(plaintext)
cipher2 = DES.new(key,DES.MODE_CBC,iv)
p = cipher2.decrypt(c)
print c
print p
