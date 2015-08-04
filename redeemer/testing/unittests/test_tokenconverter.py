import unittest

import redeemer.tokenwords.tokenconverter as tk


class test_skey_dictionary(unittest.TestCase):
    def setUp(self):
        pass

    def test_first_word_in_dictionary(self):
        result = tk._get_word_for_number(0)
        self.assertEquals(result,'A')

    def test_last_word_in_dictionary(self):
        result = tk._get_word_for_number(2047)
        self.assertEquals(result,'YOKE')

    def test_no_word_for_2048(self):
        with self.assertRaises(ValueError):
            word = tk._get_word_for_number(2048)

    def test_first_number_in_dictionary(self):
        result = tk._get_number_for_word('A')
        self.assertEquals(result,0)

    def test_last_number_in_dictionary(self):
        result = tk._get_number_for_word('YOKE')
        self.assertEquals(result,2047)

    def test_no_number_for_foo(self):
        with self.assertRaises(ValueError):
            word = tk._get_number_for_word('FOO')

    def test_case_is_ignored(self):
        result = tk._get_number_for_word('yokE')
        self.assertEquals(2047, result)

    def test_five_numbers_to_skeystring(self):
        result = tk._get_wordstring_for_numbers([0,1,2,3,2047])
        self.assertEquals('A ABE ACE ACT YOKE', result)

    def test_skeystring_to_five_numbers(self):
        result = tk._get_numbers_for_wordstring('YEAH YEAR YELL YOGA AGO')
        self.assertEquals([2043,2044,2045,2046,7], result)

    def test_correct_hexstring_to_skeystring(self):
        result = tk.get_skeystring_for_hexstring('D1854218EBBB0B51')
        self.assertTrue(result.startswith('ROME MUG FRED SCAN LIVE LACE'))

    def test_hexstring_with_wrong_lenght_to_skeystring_throws_exception(self):
        with self.assertRaises(ValueError):
            result = tk.get_skeystring_for_hexstring('1234ABCD')

    def test_correct_skeystring_to_hexstring(self):
        result = tk.get_hexstring_for_skeystring('CHEW GRIM WU HANG BUCK SAID')
        self.assertEquals('65d20d1949b5f7ab', result)

    def test_skeystring_with_wrong_lenght_to_hexstring_throws_exception(self):
        with self.assertRaises(ValueError):
            result = tk.get_skeystring_for_hexstring('CHEW GRIM WU HANG BUCK')

    def test_skeystring_to_hexstring_parity_detection(self):
        result = tk.get_hexstring_for_skeystring('FOWL KID MASH DEAD DUAL OAF')
        self.assertEquals('85c43ee03857765b', result)
        with self.assertRaises(ValueError):
            result = tk.get_skeystring_for_hexstring('FOWL KID MASH DEAD DUAL NUT')
        with self.assertRaises(ValueError):
            result = tk.get_skeystring_for_hexstring('FOWL KID MASH DEAD DUAL O')
        with self.assertRaises(ValueError):
            result = tk.get_skeystring_for_hexstring('FOWL KID MASH DEAD DUAL OAK')

    def test_correct_tokenhex_to_tokenstring(self):
        result = tk.get_tokenstring_for_tokenhex('0060080080')  # 3 2 1 0 in 11bit chunks
        self.assertEquals('ACT ACE ABE A', result)

    def test_tokenhex_with_wrong_lenght_to_tokenstring_throws_exception(self):
        with self.assertRaises(ValueError):
            result = tk.get_tokenstring_for_tokenhex('1234567890A')
        with self.assertRaises(ValueError):
            result = tk.get_tokenstring_for_tokenhex('123456789')

    def test_correct_tokenstring_to_tokenhex(self):
        result = tk.get_tokenhex_for_tokenstring('YOKE ACE ABE A')  # 2047 2 1 0 in 11bit chunks
        self.assertEquals('ffe0080080', result)

    def test_nonzero_last_nibble_tokenstring_to_tokenhex_causes_exception(self):
        with self.assertRaises(ValueError):
            result = tk.get_tokenhex_for_tokenstring('YOKE ACE ABE ABE')  # 2047 2 1 1 in 11bit chunks

    def test_wrong_length_tokenstring_to_tokenhex_causes_exception(self):
        with self.assertRaises(ValueError):
            result = tk.get_tokenhex_for_tokenstring('YOKE')

if __name__ == '__main__':
    unittest.main()
