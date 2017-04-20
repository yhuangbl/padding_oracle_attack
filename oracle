#!/usr/bin/env python
from Crypto.Cipher import AES
import sys

def b_to_num(message):
    #converts bytes to nums
    num = []
    for i in range(0, len(message)):
        num.append(int(message[i].encode('hex'), 16))
    return num

def num_to_b(num):
    b = []
    for i in range(0, len(num)):
        b.append(chr(num[i]))
    return b
    

def pad(message):
    #pads a message BEFORE encryption
    topad = 16 - len(message) % 16
    for i in range(0, topad):
        message += chr(topad)
    return message

def check_pad(message):
    #checks the padding of a message AFTER decryption
    mnum = b_to_num(message)
    wantpad = mnum[-1]
    if wantpad == 0:
        return 0
    for i in range(0, wantpad):
        if (mnum[-1-i] != wantpad):
            return 0
    return 1

try:
    fname = sys.argv[1]
    f = open(fname, "r")
except:
    print "./poracle <filename>"
    sys.exit(1)

line = f.read()
if len(line) % 16 != 0 or len(line) < 32:
    print "Input file must contain at least 32 characters, and it must be a multiple of 16."
    sys.exit(1)

iv = line[0:16]
ciphertext = line[16:]

key = 'COMP3632 testkey'
obj = AES.new(key, AES.MODE_CBC, iv)
plaintext = obj.decrypt(ciphertext)
sys.stdout.write(str(check_pad(plaintext)))
