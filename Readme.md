###### Establecer una variable local en sistema
https://www.schrodinger.com/kb/1842

OS X 10.10
To set an environment variable, enter the following command:
launchctl setenv variable "value"
To find out if an environment variable is set, use the following command:
launchctl getenv variable
To clear an environment variable, use the following command:
launchctl unsetenv variable

#### Como usar el script
###### correr el script
    pipenv shell
    >Launching subshell in virtual environment…
    >. /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/activate

###### Instalacion de un cronjob
    https://stackoverflow.com/questions/48990067/how-to-run-a-cron-job-with-pipenv

###### Obtener un shell con el workflow virtual con 
    pipenv --py
    >/Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/python

#### Crontab
Agregar tarea a cronjob
* * * * * significa cada minuto
https://crontab.guru/#01_*_*_*_*

    crontab -e

# correr .py en cron job
* * * * * /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/python /Users/panic/dev/py/alarm.py >/Users/panic/dev/py/log/stdout.log 2>/Users/panic/dev/py/log/stderr.log

# correr freeze app echa con py2app
https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file

    * * * * * /Users/panic/dev/py/dist/btc_swing.app/Contents/MacOS/btc_swing >/Users/panic/dev/py/log/stdout.log 2>/Users/panic/dev/py/log/stderr.log

#Notificaciones
    pipenv install git+https://github.com/SeTeM/pync.git#egg=pync
    brew install terminal-notifier #dependencia de ruby 

"""
opciones para notificaciones:
https://weareopensource.me/python-osx/
https://g3rv4.com/2015/08/macos-notifications-python-pycharm
https://stackoverflow.com/questions/17651017/python-post-osx-notification


https://pypi.org/project/pync/
- https://github.com/julienXX/terminal-notifier
- https://github.com/vjeantet/alerter

to be able to communicate with you over other devices.
https://github.com/dschep/ntfy    
"""