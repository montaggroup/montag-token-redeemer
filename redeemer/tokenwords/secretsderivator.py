from collections import namedtuple
import base64
import redeemer.pbkdf2

SDConfig = namedtuple('SDConfig','salt, usage, iteration_count')

class SecretsDerivator(object):
    def __init__(self, config):
        self.config = config
        if not len(self.config.salt) or not int(self.config.iteration_count) or not len(self.config.usage):
            raise ValueError("Must supply salt, usage and iteration count!")

    def derive_secrect(self, token):
        binarystring = redeemer.pbkdf2.pbkdf2_hmac('sha512', token,
                                                   self.config.salt+self.config.usage, self.config.iteration_count)
        hexstring = base64.b16encode(binarystring)
        return hexstring.lower()

