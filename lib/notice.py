class Btc_currency:
    from pync import Notifier
    import subprocess
    import requests
    import json
    import time

    bounce_bounds = 99
    last_usd = 0
    live_usd = 0
    live_mxn = 0
    price_action = {}
    rise_alert = [10500, 10800, 10965, 11100, 11265,
                11300, 11500, 11765, 11900, 12100, 12300, 12500, 12800]
    drop_alert = [9500, 9200, 9090, 9000, 8900, 8700, 8500, 8300, 8100, 8000, ]

    @staticmethod
    def stdout_flow(course):
        t_now = Btc_currency.time.strftime("%I:%M:%S")

        if course == "req_bitcoin_val()":
            msg = "req_bitcoin_val(): live_usd $%s "
            values = (live_usd)

        elif course == "get_price_shift()":
            msg = "get_price_shift(): last_usd $%s"
            values = (last_usd)

        elif course == "crossing_bounds()":
            msg = "crossing_bounds() variación de: $%s %s\n%s"
            values = (price_action["amount"],
                    price_action["trend"], t_now)

        elif course == "not_cross":
            msg = "price_action in bounds: no cruso los limites, variacion de: $%s, %s límites de rebote de: $%s\n%s\n"
            values = (price_action["amount"], price_action["trend"],
                      Btc_currency.bounce_bounds, t_now)
        
        elif course == "Err_requests":
            msg = "Sin internet ... %s\n"
            values = (t_now)
        
        elif course == "check_alert()":
            msg = "Alerta de precio! %s"
            values = (t_now)
        
        elif course == "announcement()":
            msg = "announcement() %s"
            values = (t_now)
        else:
            msg = "unknown stdout_flow call %s"
            values = ("")

        print(msg % values)

    @staticmethod
    def req_bitcoin_val():
        try:
            rq = Btc_currency.requests.get(
            'https://api.coindesk.com/v1/bpi/currentprice/mxn.json').json()
        except Btc_currency.requests.exceptions.ConnectionError:
            Btc_currency.stdout_flow("Err_requests")
            raise SystemExit
        
        global live_usd, live_mxn
        live_usd = int(rq["bpi"]["USD"]["rate_float"])
        live_mxn = int(rq["bpi"]["MXN"]["rate_float"])

        Btc_currency.stdout_flow("req_bitcoin_val()")

    @staticmethod
    def get_usd_env():
        completed = Btc_currency.subprocess.run(
            ["launchctl", "getenv", "usd"], stdout=Btc_currency.subprocess.PIPE)
        usd_local_env = completed.stdout.decode('utf-8')

        Btc_currency.set_usd_env()
        if usd_local_env == "":
            return live_usd
        else:
            return int(usd_local_env)

    @staticmethod
    def set_usd_env():
        Btc_currency.subprocess.run(
            ["launchctl", "setenv", "usd", str(live_usd)])

    @staticmethod
    def send_notification():
        if price_action["trend"] == "a la alza":
            icon = "img/blue_bull_128.png"
        elif price_action["trend"] == "a la baja":
            icon = "img/red_bear_128.png"
        else:
            icon = "img/btc_move.png"

        Btc_currency.Notifier.notify("$ " + str(price_action["amount"]) + " Dolares",
                                     title=price_action["trend"], appIcon=icon, open='https://www.tradingview.com/chart/Cz3BHy7j/')

    @staticmethod
    def rounding(value,currency):
        if live_usd >= 10000 and currency=="usd":
            return str(value)[0:3]+"00"
        elif live_usd < 10000 and currency == "usd":
            return str(value)[0:2]+"00"

        if live_mxn >= 100000 and currency == "mxn":
            return str(value)[0:3]+"000"
        elif live_mxn < 100000 and currency == "mxn":
            return str(value)[0:2]+"000"

    @staticmethod
    def announcement():
        _usd = Btc_currency.rounding(live_usd, "usd")
        _mxn = Btc_currency.rounding(live_mxn, "mxn")
        #system("osascript -e 'set Volume 1'")
        to_speech = "'El, bitcoin esta! en %s dolares. y en %s pesos, con variación de: %s dolares' %s" % (_usd, _mxn, price_action["amount"], price_action["trend"])    
        Btc_currency.subprocess.run(["say", "-r 185", to_speech])
        Btc_currency.send_notification()
        Btc_currency.stdout_flow("announcement()")

    @staticmethod
    def crossing_bounds():    
        Btc_currency.announcement()

    @staticmethod
    def get_price_shift():
        Btc_currency.req_bitcoin_val()
        global last_usd
        last_usd = Btc_currency.get_usd_env()
        
        #If price swing out selected range
        global price_action
        if live_usd >= last_usd + Btc_currency.bounce_bounds:
            price_action = {"in_bounds": False, "amount": live_usd - last_usd, "trend": "a la alza"}
        elif live_usd <= last_usd - Btc_currency.bounce_bounds:
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
        
        Btc_currency.stdout_flow("get_price_shift()")
        Btc_currency.check_alert()

    @staticmethod
    def check_alert():
        Btc_currency.rise_alert.sort(reverse=True)
        Btc_currency.drop_alert.sort(reverse=True)

        for price in Btc_currency.rise_alert:
            if live_usd >= price:
                Btc_currency.announcement()
                return
        for price in Btc_currency.drop_alert:
            if live_usd <= price:
                Btc_currency.announcement()
                return

Btc_currency.get_price_shift()
Btc_currency.stdout_flow(
    "not_cross") if price_action["in_bounds"] else Btc_currency.crossing_bounds()
