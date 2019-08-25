from os import system
import os
import requests
import json

def req_bitcoin():
    rq = requests.get(
        'https://api.coindesk.com/v1/bpi/currentprice/mxn.json').json()
    
    global usd,mxn,usd_move
    usd = int(rq["bpi"]["USD"]["rate_float"])
    mxn = int(rq["bpi"]["MXN"]["rate_float"])
    usd_move = 350

def price_move():
    req_bitcoin()
    last_usd = system("launchctl getenv usd") # error devuelve siempre 0
    
    if (last_usd == 0) or (usd > last_usd + usd_move) or (usd < last_usd - usd_move):
        set_env_usd = "launchctl setenv usd '%s'" % (usd)
        system(set_env_usd)
        return True
    else:
        return False


def speech():
    _usd = str(usd)[0:3]+"00"
    _mxn = str(mxn)[0:3]+"000"

    txt = "bitcoin en %s dolares y %s pesos" % (_usd, _mxn)
    system("say -r 190 "+txt)

if price_move(): speech()