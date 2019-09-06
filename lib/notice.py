class Notifications:
    from pync import Notifier
    @staticmethod
    def send_notification():
        if price_action["trend"] == "a la alza":
            icon = "img/blue_bull_128.png"
        elif price_action["trend"] == "a la baja":
            icon = "img/red_bear_128.png"
        else:
            icon = "img/btc_move.png"

        Btc.Notifier.notify("$ " + str(price_action["amount"]) + " Dolares",
                            title=price_action["trend"], appIcon=icon, open='https://www.tradingview.com/chart/Cz3BHy7j/')

    @staticmethod
    def rounding(value, currency):
        if live_usd >= 10000 and currency == "usd":
            return str(value)[0:3]+"00"
        elif live_usd < 10000 and currency == "usd":
            return str(value)[0:2]+"00"

        if btc_pair >= 100000 and currency == "mxn":
            return str(value)[0:3]+"000"
        elif btc_pair < 100000 and currency == "mxn":
            return str(value)[0:2]+"000"

    @staticmethod
    def announcement(pair_name):
        _usd = Btc.rounding(live_usd, "usd")
        _pair = Btc.rounding(btc_pair, pair_name)
        Btc.subprocess.run(["osascript", "-e", "set Volume 1.6"])
        
        to_speech = "'El, bitcoin esta! en %s dolares. y en %s pesos, con variación de: %s dolares' %s" % (
            _usd, _pair, price_action["amount"], price_action["trend"])
        Btc.subprocess.run(["say", "-r 185", to_speech])
        Btc.send_notification()

class Btc(Notifications):
    import subprocess
    import requests
    import json
    import time

    bounce_bounds = 99

    @staticmethod
    def req_bitcoin(pair_name):
        try:
            rq = Btc.requests.get(
            'https://api.coindesk.com/v1/bpi/currentprice/'+pair_name+'.json').json()
        except Btc.requests.exceptions.ConnectionError:
            print("re_bitcoin: Sin internet")
            raise SystemExit
        
        global live_usd, btc_pair
        live_usd = int(rq["bpi"]["USD"]["rate_float"])
        btc_pair = int(rq["bpi"]["MXN"]["rate_float"])

    @staticmethod
    def get_usd_env():
        completed = Btc.subprocess.run(
            ["launchctl", "getenv", "usd"], stdout=Btc.subprocess.PIPE)
        usd_local_env = completed.stdout.decode('utf-8')

        Btc.set_usd_env()
        if usd_local_env == "":
            return live_usd
        else:
            return int(usd_local_env)

    @staticmethod
    def set_usd_env():
        Btc.subprocess.run(
            ["launchctl", "setenv", "usd", str(live_usd)])

    @staticmethod
    def crossing_bounds(pair_name):    
        Btc.announcement(pair_name)

    @staticmethod
    def get_price_shift(user):
        Btc.req_bitcoin(user.pair_name)
        global last_usd
        last_usd = Btc.get_usd_env()
        
        #If price swing out selected range
        global price_action
        if live_usd >= last_usd + Btc.bounce_bounds:
            price_action = {"in_bounds": False, "amount": live_usd - last_usd, "trend": "a la alza"}
        elif live_usd <= last_usd - Btc.bounce_bounds:
            price_action = {"in_bounds": False, "amount": (last_usd - live_usd) * -1, "trend": "a la baja"}
        else:
            #If price swing inside selected range
            price_action = {"in_bounds": True}
            if live_usd > last_usd:
                price_action["trend"] = "a la alza"
                price_action["amount"] = live_usd - last_usd
            elif live_usd < last_usd:
                price_action["trend"] = "a la baja"
                price_action["amount"] = (last_usd - live_usd) * -1
            else:
                price_action["trend"] = "sin tendencia"
                price_action["amount"] = 0
        
        Btc.check_alert(user)
        return price_action

    @staticmethod
    def check_alert(user):
        rise_alert = [alert["price"] for alert in user.alarms["rise"]]
        dump_alert = [alert["price"] for alert in user.alarms["dump"]]
        rise_alert.sort(reverse=True)
        dump_alert.sort(reverse=True)
        

        for price in rise_alert:
            if live_usd >= price:
                Btc.announcement(user.pair_name)
                return
        for price in dump_alert:
            if live_usd <= price:
                Btc.announcement(user.pair_name)
                return

class User:
    from .db.db_file import DB
    
    def __init__(self,user):
        db = User.DB()
        row = db.get_alerts(user)
        self.user = user
        self.pair_name = row[0]
        self.alarms = row[1]
