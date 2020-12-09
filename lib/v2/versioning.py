import hashlib

class Versioning(object):
    def __init__(self):
        self.h = hashlib.blake2b(digest_size=4)

    def digest_file(self, content):
        self.h.update(content.encode('utf-8'))

    def generate(self):
        digest = bytearray(self.h.digest())
        digest = bytearray.hex(digest)
        return digest
