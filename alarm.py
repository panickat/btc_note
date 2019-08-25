from os import system
import requests
import json

rq = requests.get('https://api.coindesk.com/v1/bpi/currentprice/mxn.json').json()

def speech():
    usd=str(int(rq["bpi"]["USD"]["rate_float"]))[0:3]+"00"
    mxn=str(int(rq["bpi"]["MXN"]["rate_float"]))[0:3]+"000"

    txt="bitcoin en %s dolares y %s pesos" %(usd,mxn)
    print(txt)
    system("say -r 205 "+txt)

speech()
