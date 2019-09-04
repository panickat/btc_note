class DB:
    from json import dumps
    def __init__(self):
        import psycopg2
        self.cnn = psycopg2.connect(database="btc_note",
                                user="panic",
                                host="localhost",
                                password="Jajaja123",
                                port="5432")                     
        self.cursor = self.cnn.cursor()

    def close(self):
        self.cnn.commit()
        self.cursor.close()
        self.cnn.close()
    def create_usrs(self):
        self.cursor.execute("CREATE TABLE IF NOT EXISTS usrs (id serial PRIMARY KEY,name char(11), alarms json);")
    def set_alerts(self,alerts):
        s = ['(\'%s\')' % (DB.dumps(r)) for r in rise_alert]
        sql = "insert into usrs (alarms) values %s;" % (", ".join(s))
        
        self.cursor.execute(sql)
        self.close()
    def get_alerts(self,usr_id):
        sql = "Select * from alarms where usr_id="+str(usr_id)
        self.cursor.execute(sql)
        return self.cursor.fetchall()

rise_alert = (
    {"currency": "usd", "price": 10800},
    {"currency": "usd", "price": 10900},
    {"currency": "usd", "price": 11000},
    {"currency": "usd", "price": 11100},
    {"currency": "usd", "price": 11200},
    {"currency": "usd", "price": 11300},
    {"currency": "usd", "price": 11450},
    {"currency": "usd", "price": 11650}
)
dump_alert = [
    {"currency": "usd", "price": 9500},
    {"currency": "usd", "price": 9400},
    {"currency": "usd", "price": 9300},
    {"currency": "usd", "price": 9200},
    {"currency": "usd", "price": 9100},
    {"currency": "usd", "price": 9000},
    {"currency": "usd", "price": 8900},
    {"currency": "usd", "price": 8800}
    ]

db = DB()
db.set_alerts(rise_alert)
