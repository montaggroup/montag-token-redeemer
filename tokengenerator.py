import sys
import os
import base64
import json

import redeemer.pbkdf2
import redeemer.tokenwords.tokenconverter as tk

if __name__ == "__main__":
    numtokens = int(sys.argv[1])
    entrop = os.urandom(64)
    tokens = []
    for x in xrange(numtokens):
        tok = redeemer.pbkdf2.pbkdf2_hmac('sha512', 'hurtz{}'.format(x), entrop, x + 10000, dklen=5)
        tokhex = base64.b16encode(tok)
        tokens.append(tokhex)

    print 'Tokens:\n'
    for tokhex in tokens:
        print "{}\t{}".format(tokhex, tk.get_tokenstring_for_tokenhex(tokhex))
    print '\nJSON:\n'
    print json.dumps(tokens, ensure_ascii=True, indent=2)

