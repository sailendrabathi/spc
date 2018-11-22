#!/usr/bin/python
#!/usr/bin/python3


import os
import struct
import hashlib
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto import Random
from Crypto.Cipher import PKCS1_OAEP
import zlib
import base64

def encrypt_file_aes(key, in_filename, out_filename=None, chunksize=64*1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    # iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file_aes(key, in_filename, out_filename=None, chunksize=24*1024):
    """ Decrypts a file using AES (CBC mode) with the
        given key. Parameters are similar to encrypt_file,
        with one difference: out_filename, if not supplied
        will be in_filename without its last extension
        (i.e. if in_filename is 'aaa.zip.enc' then
        out_filename will be 'aaa.zip')
    """
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_CBC, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def encrypt_file_rsa(public_key, in_filename, out_filename=None, chunksize=470):
    to_join = []
    rsa_key = RSA.importKey(public_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    if not out_filename:
        out_filename = in_filename + '.enc'

    filesize = os.path.getsize(in_filename)

    offset = 0
    end_loop = False
    encrypted = b''

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            blob = infile.read()
            blob = zlib.compress(blob)
            while not end_loop:
                chunk = blob[offset:offset+chunksize]
                if len(chunk) % chunksize != 0:
                    end_loop = True
                    chunk += b' ' * (chunksize - len(chunk))
                encrypted += rsa_key.encrypt(chunk)
                offset += chunksize

            outfile.write(base64.b64encode(encrypted))


def decrypt_file_rsa(private_key, in_filename, out_filename=None, chunksize=512):
    rsa_key = RSA.importKey(private_key)
    rsa_key = PKCS1_OAEP.new(rsa_key)

    offset = 0;
    decrypted = b''

    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        blob = infile.read()
        blob = base64.b64decode(blob)
        with open(out_filename, 'wb') as outfile:
            while offset < len(blob):
                chunk = blob[offset:offset + chunksize]
                decrypted += rsa_key.decrypt(chunk)
                offset += chunksize

            outfile.write(zlib.decompress(decrypted))

            outfile.truncate(origsize)

def encrypt_file_aes1(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    # iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_ECB, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file_aes1(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_ECB, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)


def encrypt_file_aes2(key, in_filename, out_filename=None, chunksize=64*1024):
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = os.urandom(16)
    # iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_OFB, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += b' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


def decrypt_file_aes2(key, in_filename, out_filename=None, chunksize=24*1024):
    if not out_filename:
        out_filename = os.path.splitext(in_filename)[0]

    with open(in_filename, 'rb') as infile:
        origsize = struct.unpack('<Q', infile.read(struct.calcsize('Q')))[0]
        iv = infile.read(16)
        decryptor = AES.new(key, AES.MODE_OFB, iv)

        with open(out_filename, 'wb') as outfile:
            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                outfile.write(decryptor.decrypt(chunk))

            outfile.truncate(origsize)




# password = "kitty"
#
# key = hashlib.sha256(password.encode('utf-8')).digest()
#
# encrypt_file_aes2(key, "fernando.jpg", "p1.txt.enc")
#
# decrypt_file_aes2(key, "p1.txt.enc", "fernando2.jpg")

# ran_gen = Random.new().read
# rsa_key = RSA.generate(4096, e=65537)
# private_key = rsa_key.exportKey("PEM")
# public_key = rsa_key.publickey().exportKey("PEM")
#
# fd = open("private_key.pem", "wb")
# fd.write(private_key)
# fd.close()
#
# fd = open("public_key.pem", "wb")
# fd.write(public_key)
# fd.close()
# encrypt_file_rsa(public_key, "fernando.jpg", "rsa.enc")
# print("------------")
# decrypt_file_rsa(private_key, "rsa.enc", "fernando3.jpg")
