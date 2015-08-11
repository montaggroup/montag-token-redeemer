from collections import namedtuple
import base64
import redeemer.pbkdf2

SDConfig = namedtuple('SDConfig', "salt, usage, iteration_count")


class SecretsDerivator(object):
    def __init__(self, config):
        self.config = config
        if not len(self.config.salt) or int(self.config.iteration_count) <= 0 or not len(self.config.usage):
            raise ValueError("Must supply salt, usage and iteration count!")

    def derive_secret(self, token):
        binary_string = redeemer.pbkdf2.pbkdf2_hmac('sha512', token,
                                                    self.config.salt + self.config.usage, self.config.iteration_count)
        hex_string = base64.b16encode(binary_string)
        return hex_string.lower()

    def derive_secret_base64(self, token):
        binary_string = redeemer.pbkdf2.pbkdf2_hmac('sha512', token,
                                                    self.config.salt + self.config.usage, self.config.iteration_count)
        result = base64.b64encode(binary_string)
        return result.lower()