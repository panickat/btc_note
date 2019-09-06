class DB:
    from json import dumps
    import psycopg2

    def __init__(self):
        self.cnn = DB.psycopg2.connect(
            database="btc_note",
            user="panic",
            host="localhost",
            password="Jajaja123",
            port="5432")
        self.cursor = self.cnn.cursor()

    def send_query(self,sql, fetch=False):
        if self.cnn:
            f = None
            self.cursor.execute(sql+";")
            if fetch: f = self.cursor.fetchone()

            self.cnn.commit()
            self.cursor.close()
            self.cnn.close()
            return f

    def create_tbl(self):
        sql = "CREATE TABLE IF NOT EXISTS usrs (id serial PRIMARY KEY, name char(11), pair char(3), alarms json)"
        self.send_query(sql)

    def insert_alerts(self,pair, alerts):
        sql = "insert into users (pair,alarms) values ('%s','%s')" % (pair, DB.dumps(alerts))
        self.send_query(sql)

    def get_alerts(self, name):
        sql = "select pair,alarms from users where name = '%s'" % (name)
        return self.send_query(sql, fetch=True)

    def update_alerts(self,pair,alerts,name):
        sql = "update users set pair = '%s', alarms = '%s' where name = '%s'" % (pair,DB.dumps(alerts),name)
        self.send_query(sql)

"""
consultas en tabla json
    insert into usrs (alarms) values ('{"rise":{"currency":"mxn","price":100}}'),('{"dump":{"currency":"mxn","price":10}}')

    insert into users (alarms) values 
        ('{"rise":[
            {"currency":"cny","price":100},
            {"currency":"cny","price":99}
            ],
        "dump":[
            {"currency":"cny","price":2},
            {"currency":"cny","price":1}
            ]
        }')

    select json_array_elements(alarms->'dump')->'price' from users

Crea multiples usuarios(filas) por cada alarma guardada
    alerts = (
        {"currency":"usd","price":10800},
        {"currency":"usd","price":10900}
    )        
    s = ['(\'%s\')' % (DB.dumps(r)) for r in alerts]
    sql = "insert into users (alarms) values %s;" % (", ".join(s))
"""
