#!/usr/bin/env python2.7
import logging
logging.basicConfig(level=logging.INFO)

import argparse
import os
import sys

def get_main_dir():
    return os.path.dirname(sys.argv[0])


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Runs the web for token redeeming')
    parser.add_argument('--basepath', '-b', dest='basepath', help='Sets the basepath for the server', action='store')
    
    args = parser.parse_args()
    

    os.chdir(os.path.join(get_main_dir(), 'web2py'))
    sys.path.append('.')
    sys.path.append('..')
    sys.path.append('gluon')

    import web2py.gluon.widget

    # commandline for web2py to parse
    sys.argv = ['web2py.py', '-a', '12345', '-i', '0.0.0.0', '-p', '8001']
    web2py.gluon.widget.start(cron=True)
