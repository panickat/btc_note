from pync import Notifier
import subprocess
import requests
import json
import time

bounce_bounds = 1
last_usd = 0
live_usd = 0
live_mxn = 0
rise_alarm = [10500,10800,10965,11100,11265,11300,11500,1765,11900,12100,12300,12500,12800]
drop_alarm = [9500,9200,9090,9000,8900,8700,8500,8300,8100,8000]
price_action = {}

def stdout_flow(course):
    t_now = time.strftime("%I:%M:%S")
    if course == "req_bitcoin_val()":
        msg = "req_bitcoin_val(): live_usd $%s "
        values = (live_usd)

    elif course == "get_price_shift()":
        msg = "get_price_shift(): last_usd $%s"
        values = (last_usd)

    elif course == "speech()":
        msg = "speech() variación de: $%s %s\n%s"
        values = (price_action["variation"],
                  price_action["trend"], t_now)

    elif course == "not_cross":
        msg = "price_action else: no cambio, variacion de: $%s, %s límites de rebote de: $%s\n%s\n"
        values = (price_action["variation"],
                  price_action["trend"], bounce_bounds, t_now)
    
    elif course == "Err_requests":
        msg = "Sin internet ... %s\n"
        values = (t_now)

    print(msg % values)

def req_bitcoin_val():
    try:
        rq = requests.get(
        'https://api.coindesk.com/v1/bpi/currentprice/mxn.json').json()
    except requests.exceptions.ConnectionError:
        stdout_flow("Err_requests")
        raise SystemExit
    
    global live_usd, live_mxn
    live_usd = int(rq["bpi"]["USD"]["rate_float"])
    live_mxn = int(rq["bpi"]["MXN"]["rate_float"])

    stdout_flow("req_bitcoin_val()")

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

def send_notification():
    if price_action["trend"] == "a la alza":
        icon = "img/blue_bull_128.png"
    elif price_action["trend"] == "a la baja":
        icon = "img/red_bear_128.png"

    Notifier.notify("$ " + str(price_action["variation"]) + " Dolares",title=price_action["trend"],appIcon=icon,open='https://www.tradingview.com/chart/Cz3BHy7j/')

def speech():
    _usd = str(live_usd)[0:3]+"00"
    _mxn = str(live_mxn)[0:3]+"000"

    to_speech = "'El, bitcoin esta! en %s dolares. y en %s pesos, con variación de: %s dolares' %s" % (
        _usd, _mxn, price_action["variation"], price_action["trend"])
    subprocess.run(["say", "-r 185", to_speech])

    send_notification()
    stdout_flow("speech()")

def get_price_shift():
    req_bitcoin_val()
    global last_usd
    last_usd = get_usd_env()
    stdout_flow("get_price_shift()")

    #If price swing out selected range
    global price_action
    if live_usd >= last_usd + bounce_bounds:
        price_action = {"in_bounds": True, "variation": live_usd - last_usd, "trend": "a la alza"}
    elif live_usd <= last_usd - bounce_bounds:
        price_action = {"in_bounds": True, "variation": (last_usd - live_usd) * -1, "trend": "a la baja"}
    else:
        #If price swing inside selected range
        price_action = {"in_bounds": False, "variation": last_usd - live_usd}
        if live_usd > last_usd:
            price_action["trend"] = "a la alza"
        elif live_usd < last_usd:
            price_action["trend"] = "a la baja"
            price_action["variation"] = price_action["variation"] * -1

def send_alert():
    if price_action["trend"] == "a la alza":
        pass
    elif price_action["trend"] == "a la baja":
        pass
    
get_price_shift()
speech() if price_action["in_bounds"] else stdout_flow("not_cross")
