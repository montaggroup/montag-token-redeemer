import unittest

from redeemer.tokenwords.secretsderivator import SecretsDerivator
from redeemer.tokenwords.secretsderivator import SDConfig

"""
The tests are based on http://stackoverflow.com/questions/15593184/pbkdf2-hmac-sha-512-test-vectors
"""


class test_secretsderivator(unittest.TestCase):
    def setUp(self):
        self.token = 'password'
        self.config = SDConfig(salt='sa', usage='lt', iteration_count=1)
        self.known_answer = '867f70cf1ade02cff3752599a3a53dc4af34c7a669815ae5d513554e1c8cf252' \
                            'c02d470a285a0501bad999bfe943c08f050235d7d68b1da55e63f73b60a57fce'

    def test_initialization_works_with_valid_config(self):
        sd = SecretsDerivator(self.config)
        self.assertEquals(self.config.salt, sd.config.salt)
        self.assertEquals(self.config.usage, sd.config.usage)
        self.assertEquals(self.config.iteration_count, sd.config.iteration_count)

    def test_invalid_config_raises_error(self):
        invalidconfig = SDConfig('', 'usage', 1)
        with self.assertRaises(ValueError):
            sd = SecretsDerivator(invalidconfig)

        invalidconfig = SDConfig('salt', '', 1)
        with self.assertRaises(ValueError):
            sd = SecretsDerivator(invalidconfig)

        invalidconfig = SDConfig('salt', 'usage', 0)
        with self.assertRaises(ValueError):
            sd = SecretsDerivator(invalidconfig)

    def test_derivation_works_with_valid_config(self):
        sd = SecretsDerivator(self.config)
        self.assertEquals(self.known_answer, sd.derive_secrect(self.token))

    def test_derivation_works_with_a_second_known_input_set(self):
        config = SDConfig(salt='saltSALTsa', usage='ltSALTsaltSALTsaltSALTsalt', iteration_count=4096)
        sd = SecretsDerivator(config)
        self.assertEquals('8c0511f4c6e597c6ac6315d8f0362e225f3c501495ba23b868c005174dc4ee71'
                          '115b59f9e60cd9532fa33e0f75aefe30225c583a186cd82bd4daea9724a3d3b8',
                          sd.derive_secrect('passwordPASSWORDpassword'))

    def test_parameter_usage_correctly_separates_domains(self):
        sd = SecretsDerivator(self.config)
        config2 = SDConfig(salt='sa', usage='lz', iteration_count=1)
        sd2 = SecretsDerivator(config2)
        self.assertNotEqual(sd.derive_secrect(self.token), sd2.derive_secrect(self.token))

    def test_derivation_is_deterministic_over_time(self):
        sd = SecretsDerivator(self.config)
        for x in xrange(20):
            self.assertEquals(self.known_answer, sd.derive_secrect(self.token))

