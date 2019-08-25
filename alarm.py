import subprocess
import requests
import json

def req_bitcoin():
    rq = requests.get(
        'https://api.coindesk.com/v1/bpi/currentprice/mxn.json').json()
    
    global usd,mxn,usd_move
    usd = int(rq["bpi"]["USD"]["rate_float"])
    mxn = int(rq["bpi"]["MXN"]["rate_float"])
    usd_move = 1
    print("request: "+str(usd))

def get_env_usd():
    completed = subprocess.run(
        ["launchctl", "getenv", "usd"], stdout=subprocess.PIPE)
    return int(completed.stdout.decode('utf-8'))

def price_move():
    req_bitcoin()
    last_usd = get_env_usd()
    print("price_move: "+ str(last_usd))
    
    if (last_usd == 0) or (usd > last_usd + usd_move) or (usd < last_usd - usd_move):
        subprocess.run(["launchctl","setenv","usd",str(usd)])
        return True
    else:
        return False

def speech():
    _usd = str(usd)[0:3]+"00"
    _mxn = str(mxn)[0:3]+"000"

    txt = "'bitcoin en %s dolares, en %s pesos, con variación de: '" % (
        _usd, _mxn)
    subprocess.run(["say","-r 190",txt])
    
speech() if price_move() else print("no cambio esta en: $" + str(usd))
