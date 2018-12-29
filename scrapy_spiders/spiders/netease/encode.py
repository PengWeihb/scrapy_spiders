# 先导入所需要的包
# pip3 install Crypto
# 再安装pycrypto
# pip3 install pycrypto
import base64
import binascii
import math
from random import random
# from Crypto.Cipher import AES, PK
from Crypto.Cipher import AES, PKCS1_OAEP

# from cryptography.hazmat.primitives.ciphers.algorithms import AES
# from Crypto.Cipher import AES
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

rsa_key1 = "010001"
rsa_key2 = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
secret_key = '0CoJUm6Qyw8W8jud'

IV = '0102030405060708'


def aes_enc(data, key):
    data_len = len(data)
    pad_len = 16-data_len % 16
    data += (chr(pad_len) * pad_len).encode()

    encoder = AES.new(key.encode(), AES.MODE_CBC, IV.encode())
    test = encoder.encrypt(data)
    print(test, type(test))
    test = base64.b64encode(test)
    return test


def my_random(a):
    b = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    c = ""
    for i in range(a):
        e = random() * len(b)
        e = math.floor(e)
        c += b[e]
    return c


def quick_pow_mod(a, b, c):
    a = a % c
    ans = 1
    while b != 0:
        if b & 1:
            ans = (ans * a) % c
        b >>= 1
        a = (a % c) * (a % c)
    return ans


def rsa_enc(message):
    text = message[::-1]
    print(text)
    rsa = quick_pow_mod(int(binascii.hexlify(text), 16), int(rsa_key1, 16),
                        int(rsa_key2, 16))
    return format(rsa, 'x')


def netease_enc(message):
    i = my_random(16)
    aes_text = aes_enc(message.encode(), secret_key)
    aes_text = aes_enc(aes_text, i)
    rsa_text = rsa_enc(i.encode())

    return {'params': aes_text.decode(), 'encSecKey': rsa_text}


if __name__ == '__main__':
    # print(aes_encrypt('sadfasdf', secret_key))
    # ret = aes_enc('{"s":"ace","limit":"8","csrf_token":""}', secret_key)
    # print(ret, type(ret))
    # ret = rsa_enc(b'zYN5AcOxckqebKXt')
    # print(ret, len(ret))
    # print(rsa.newkeys(3000))

    # ret = encryption(b'zYN5AcOxckqebKXt')
    # print(ret)

    print(netease_enc('{"s":"ace","limit":"8","csrf_token":""}'))

