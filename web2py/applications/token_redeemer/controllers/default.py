# -*- coding: utf-8 -*-
from redeemer import pydb

def index():
    return _token_input()


def show_setup_instructions():

    page_key = request.args[0]
    entry = get_entry_by_page_key(page_key)
    if not entry:
        response.flash = "Sorry, this page does not exist."
        return dict(secret=None)

    nick = entry.nickname
    token_string = entry.token_string
    token_hex = tokenconverter.get_tokenhex_for_tokenstring(token_string)

    secret = generate_secret(token_hex)

    return dict(nick=nick, secret=secret)



def _token_input():
    form=FORM('Token code:',
              INPUT(_name='token', requires=IS_NOT_EMPTY()),BR(),
              'Nick (Optional): ',
              INPUT(_name='nick'),BR(),
              INPUT(_type='submit'))
    if form.accepts(request,session):
        nick = form.vars.nick or "- Empty - "
        token_string = form.vars.token

        print "Nick {} has entered token {}".format(nick, token_string)

        if not is_token_valid(token_string):
            response.flash = "Sorry, the the token is not valid."
            return dict(form=form)

        if is_token_redeemed(token_string):
            response.flash = "Sorry, this token has already been redeemed."
            return dict(form=form)

        token_hex = tokenconverter.get_tokenhex_for_tokenstring(token_string)

        secret = generate_secret(token_hex)
        print token_hex, secret
        pydb.add_friend_to_pydb(token_hex, secret)
        page_key = redeem_token(token_string, nick)

        redirect(URL('default', 'show_setup_instructions', args=page_key))

        response.flash = form.vars.nick
    elif form.errors:
        response.flash = 'Form has errors.'
    else:
        response.flash = 'Please fill out the token field.'
    return dict(form=form)