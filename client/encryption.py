from Crypto import Random
from Crypto.Hash import SHA
from Crypto.Cipher import PKCS1_OAEP as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

from Crypto.Cipher import AES
import base64
import os

from termcolor import colored

def decide_filename(username, recipient):
    if username < recipient:
        return 'local_cache/AES_keys/' + username + '_' + recipient + '.key'
    else:
        return 'local_cache/AES_keys/' + recipient + '_' + username + '.key'


def gen_AES_key(username, recipient):
    # the block size for the cipher object; must be 16, 24, or 32 for AES
    BLOCK_SIZE = 32

    # generate a random secret key
    key = os.urandom(BLOCK_SIZE)
    key_path = decide_filename(username, recipient)

    if os.path.isfile(key_path):
        with open(key_path, mode='rb') as f:
            key = f.read()
    else:
        with open(key_path, mode='wb') as f:
            f.write(key)

    return key

def gen_RSA_key(username):

    random_generator = Random.new().read
    rsa = RSA.generate(1024, random_generator)

    private_key = rsa.exportKey()
    with open('local_cache/private_keys/' + username + '_private.pem', 'wb') as f:
        try:
            f.write(private_key)
        except Exception as e:
            raise Error(colored("Key generation failed!", 'red'))

    public_key = rsa.publickey().exportKey()
    return public_key

def encode_AES(AES_key, recipient_public_key):

    rsa_key = RSA.importKey(recipient_public_key)
    cipher = Cipher_pkcs1_v1_5.new(rsa_key)
    encoded_AES = cipher.encrypt(AES_key)
    print("")
    encoded_AES = base64.b64encode(encoded_AES)
    return encoded_AES

def decode_AES(encoded_AES, username):

    with open('local_cache/private_keys/' + username + '_private.pem', 'rb') as f:
        private_key = f.read()
        rsa_key = RSA.importKey(private_key)
        cipher = Cipher_pkcs1_v1_5.new(rsa_key)
        decoded_AES = base64.b64decode(encoded_AES)
        decoded_AES = cipher.decrypt(decoded_AES) 
        return decoded_AES

def query_AES(username, recipient):

    key_path = decide_filename(username, recipient)

    if os.path.isfile(key_path):
        with open(key_path, mode='rb') as f:
            AES_key = f.read()
            return True, AES_key
    else:
        return False, ""

def store_AES_key(AES_key, username, recipient):

    key_path = decide_filename(username, recipient)

    with open(key_path, mode='wb') as f:
        f.write(AES_key)

def AES_encrypt(message, AES_key):
    BLOCK_SIZE = 32
    PADDING = ' '
    pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING
    EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s).encode('utf-8')))
    cipher = AES.new(AES_key, AES.MODE_ECB)
    return EncodeAES(cipher, message)

def AES_decrypt(message, AES_key):
    PADDING = ' '
    DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING.encode('utf-8'))
    cipher = AES.new(AES_key, AES.MODE_ECB)
    decrypted = ""
    for line in message:
        decrypted += DecodeAES(cipher, line).decode('ascii')
    return decrypted