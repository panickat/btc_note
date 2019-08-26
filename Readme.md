Establecer una variable local en sistema
https://www.schrodinger.com/kb/1842

OS X 10.10
To set an environment variable, enter the following command:
launchctl setenv variable "value"
To find out if an environment variable is set, use the following command:
launchctl getenv variable
To clear an environment variable, use the following command:
launchctl unsetenv variable


correr el script
pipenv shell
    Launching subshell in virtual environment…
 . /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/activate

Instalacion de un cronjob
    https://stackoverflow.com/questions/48990067/how-to-run-a-cron-job-with-pipenv

Obtener un shell con el workflow virtual con 
pipenv --py
    /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/python

Agregar atrea a cronjob
    * * * * * cada minuto
    https://crontab.guru/#01_*_*_*_*

crontab -e
# correr .py
* * * * * /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/python /Users/panic/dev/py/alarm.py >/Users/panic/dev/py/log/stdout.log 2>/Users/panic/dev/py/log/stderr.log

# correr freeze app echa con py2app
* * * * * /Users/panic/dev/py/dist/btc_swing.app/Contents/MacOS/btc_swing >/Users/panic/dev/py/log/stdout.log 2>/Users/panic/dev/py/log/stderr.log