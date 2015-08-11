# -*- coding: utf-8 -*-
#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()
import re
import os
import sys

web2py_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)))
py_dir = web2py_dir
for i in range(0, 4):
    py_dir, _ = os.path.split(py_dir)

if py_dir not in sys.path:
    sys.path.append(py_dir)
print py_dir
print sys.path

from redeemer.tokenwords import tokenconverter
from redeemer.tokenwords import secretsderivator

db = DAL('sqlite://storage.sqlite')

db.define_table('tokens', Field('token_string'),
                Field('redeemed', type='boolean'),
                Field('nickname'),
                Field('pagekey'))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager

auth = None

crud, service, plugins = Crud(db), Service(), PluginManager()

response.breadcrumb_bar = request.function.replace('_', ' ').title()


def is_token_valid(token_string):
    try:
        tokenconverter.get_tokenhex_for_tokenstring(token_string)
    except ValueError:
        pass

    rows = db(db.tokens.token_string == token_string).select()
    return bool(rows)


def is_token_redeemed(token_string):
    if not is_token_valid(token_string):
        raise ValueError("Invalid token")
    row = db(db.tokens.token_string == token_string).select().first()
    return row.redeemed


def redeem_token(token_string, nickname):
    nickname = re.sub("[^A-Za-z0-9_\.;/$%&()\-']", "_", nickname)
    if not is_token_valid(token_string):
        raise ValueError("Invalid token")
    if is_token_redeemed(token_string):
        raise ValueError("Token already redeemed.")

    page_key = generate_page_key(token_string)

    row = db(db.tokens.token_string == token_string).select().first()
    row.update_record(redeemed=True, nickname=nickname, pagekey=page_key)

    return page_key


def generate_page_key(token_string):
    config = secretsderivator.SDConfig('salt', 'page_key', 1000)
    page_key_derivator = secretsderivator.SecretsDerivator(config)

    hex = tokenconverter.get_tokenhex_for_tokenstring(token_string)
    return page_key_derivator.derive_secret(hex)[:32]


def get_all_tokens():
    return db(db.tokens.ALL).select()


def get_entry_by_page_key(page_key):
    return db(db.tokens.token_string == page_key and db.tokens.redeemed).select().first()



def generate_secret(token_hex):
    config = secretsderivator.SDConfig('salt', 'pydb_secret', 1000)
    secret_derivator = secretsderivator.SecretsDerivator(config)

    return secret_derivator.derive_secret_base64(token_hex)[:32]
