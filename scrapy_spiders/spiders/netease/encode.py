import math
from random import random


def aa(a):
    d = None
    e = None
    b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    c = ""

    for i in range(a):
        e = random() * len(b)
        e = math.floor(e)
        c += b[e]

    return c


def bb(a, b):
    c = CryptoJS.enc.Utf8.parse(b)
    d = CryptoJS.enc.Utf8.parse("0102030405060708")
    e = CryptoJS.enc.Utf8.parse(a)
    f = CryptoJS.AES.encrypt(e, c, {iv: d,mode: CryptoJS.mode.CBC});
    return f.toString()

if __name__ == '__main__':
    print(aa(16))
