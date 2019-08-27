from pync import Notifier
import subprocess
import requests
import json
import time

usd_swing = 1
last_usd = 0
live_usd = 0
live_mxn = 0

def outflow(course):
    if course == "req_bitcoin_val()":
        msg = "req_bitcoin_val(): live_usd $%s "
        values = (live_usd)

    elif course == "price_move()":
        msg = "price_move(): last_usd $%s"
        values = (last_usd)

    elif course == "speech()":
        msg = "speech() variación de: $%s %s"
        values = (price_moved["variation"], price_moved["trend"])

    if course == "not_moved":
        msg = "price_moved else: no cambio, variacion de: $%s, %s de: $%s\n%s"
        values = (price_moved["variation"],
                  price_moved["trend"], usd_swing, time.strftime("%I:%M:%S"))

    print(msg % values)

def req_bitcoin_val():
    rq = requests.get(
        'https://api.coindesk.com/v1/bpi/currentprice/mxn.json').json()

    global live_usd, live_mxn
    live_usd = int(rq["bpi"]["USD"]["rate_float"])
    live_mxn = int(rq["bpi"]["MXN"]["rate_float"])

    outflow("req_bitcoin_val()")

def get_usd_env():
    completed = subprocess.run(
        ["launchctl", "getenv", "usd"], stdout=subprocess.PIPE)
    usd_local_env = completed.stdout.decode('utf-8')

    if usd_local_env:
        return int(usd_local_env)
    else:
        set_usd_env()
        return live_usd

def set_usd_env():
    subprocess.run(["launchctl", "setenv", "usd", str(live_usd)])

def send_notification(price_moved):
    if price_moved["trend"] == "a la alsa":
        icon = "img/blue_bull_128.png"
    elif price_moved["trend"] == "a la baja":
        icon = "img/red_bear_128.png"

    Notifier.notify(
        "$ " + str(price_moved["variation"]) + " Dolares", title=price_moved["trend"],
        appIcon=icon,
        open='https://www.tradingview.com/chart/Cz3BHy7j/')

def speech(price_moved):
    _usd = str(live_usd)[0:3]+"00"
    _mxn = str(live_mxn)[0:3]+"000"

    to_speech = "'El, bitcoin esta! en %s dolares. y en %s pesos, con variación de: %s dolares' %s" % (
        _usd, _mxn, price_moved["variation"], price_moved["trend"])
    subprocess.run(["say", "-r 185", to_speech])

    send_notification(price_moved)
    outflow("speech()")

def price_move():
    req_bitcoin_val()
    global last_usd
    last_usd = get_usd_env()
    outflow("price_move()")

    #If price swing out selected range
    if live_usd >= last_usd + usd_swing:
        return {"move": True, "variation": live_usd - last_usd, "trend": "a la alsa"}
    elif live_usd <= last_usd - usd_swing:
        return {"move": True, "variation": last_usd - live_usd, "trend": "a la baja"}
    else:
        #If price swing inside selected range
        return {"move": False, "variation": last_usd - live_usd, "trend": "dentro del rango"}

price_moved = price_move()
speech(price_moved) if price_moved["move"] else outflow("not_moved")
