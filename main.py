from lib import User, DB
"""
Pendiente de optimizar:
    1. En un lapso de un minuto usar live_usd last_usd contenidos en el objeto User (sin usar request)
    2. preguntar si hacer request al inicializar un Usuario, si ha pasado un lapso(minuto) 
    desde la ultima vez que se llamo a request

- la proxima ves que se llame a User se puede omitir la db
"""

db = DB()
user = User(name="cris",db=db)
