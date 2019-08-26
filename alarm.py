import subprocess
import requests
import json

def req_bitcoin_val():
    rq = requests.get(
        'https://api.coindesk.com/v1/bpi/currentprice/mxn.json').json()
    
    global live_usd,live_mxn,usd_move
    live_usd = int(rq["bpi"]["USD"]["rate_float"])
    live_mxn = int(rq["bpi"]["MXN"]["rate_float"])
    usd_move = 300
    print("req_bitcoin_val(): live_usd $"+str(live_usd))

def get_usd_env():
    completed = subprocess.run(["launchctl", "getenv", "usd"], stdout=subprocess.PIPE)
    usd_local_env = completed.stdout.decode('utf-8')
    
    if usd_local_env:
        return int(usd_local_env)
    else:
        set_usd_env()
        return live_usd

def set_usd_env():
    subprocess.run(["launchctl", "setenv", "usd", str(live_usd)])

def price_move():
    req_bitcoin_val()
    last_usd = get_usd_env()
    print("price_move(): last_usd $"+ str(last_usd))
    
    if live_usd >= last_usd + usd_move:
        return {"move": True,"variation": live_usd - last_usd, "trend": "alsa"}
    elif live_usd <= last_usd - usd_move:
        return {"move": True, "variation": last_usd - live_usd, "trend": "baja"}
    else:
        return {"move": False, "variation": last_usd - live_usd, "trend": "nada"}


def speech(price_moved):
    _usd = str(live_usd)[0:3]+"00"
    _mxn = str(live_mxn)[0:3]+"000"

    txt = "'El, bitcoin esta! en %s dolares. y en %s pesos, con variación de: %s dolares' a la %s" % (
        _usd, _mxn, price_moved["variation"], price_moved["trend"])
    subprocess.run(["say","-r 185",txt])
    
    print("variacion de: $" + str(price_moved["variation"]) + " a la " + price_moved["trend"])


price_moved = price_move()
speech(price_moved) if price_moved["move"] else print(
    "no cambio esta en: $" + str(live_usd))
