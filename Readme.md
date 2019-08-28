#### Como usar el script
correr el script en un entorno virtual
`pipenv shell`
>Launching subshell in virtual environment…
. /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/activate

Se crea automatica mente una variable de entorno llamada `usd`
para revisar o modificar la variable `launchctl getenv/setenv`

###### Para obtener un shell con el workflow virtual para el crontab
`pipenv --py`
>/Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/python

### Metodos para correr servicios

##### Crontab

- [How to run a crontab with pipenv](https://stackoverflow.com/questions/48990067/how-to-run-a-cron-job-with-pipenv) 
- [como hacer argumentos de tiempo en crontab](https://crontab.guru/#01_*_*_*_*)

###### correr .py en crontab
- & "ampersand" al final para correr en segundo plano
- Nesecita la ruta desde la raiz

`crontab -e`

    * * * * * /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/python /Users/panic/dev/btc_note/alarm.py >/Users/panic/dev/btc_note/log/stdout.log 2>/Users/panic/dev/btc_note/log/stderr.log &

###### correr freeze app echa con py2app en crontab
[como usar py2app](https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file)

    * * * * * /Users/panic/dev/btc_note/dist/btc_swing.app/Contents/MacOS/btc_swing >/Users/panic/dev/btc_note/log/stdout.log 2>/Users/panic/dev/btc_note/log/stderr.log &

##### Configurar servicio cron con un archivo Plist

`launchctl load/unload` /Users/panic/Library/LaunchAgents/com.panic.btc_swing.plist
`launchctl list | grep btc_swing` para revisar el estado del servicio

`plutil` ayuda a checar la sintaxis del archivo

    <?xml version="1.0" encoding="UTF-8"?>
    <!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" \
    "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
    <plist version="1.0">
    <dict>

        <!-- Contains a unique string that identifies your daemon to launchd.
        This key is required. -->
        <key>Label</key>
        <string>com.panic.btc_swing</string>

        <!-- Contains the arguments [to exec()] used to launch your daemon.
        This key is required.  -->
        <key>ProgramArguments</key>
        <array>
        <string>/Users/panic/dev/btc_note/dist/btc_swing.app/Contents/MacOS/btc_swing</string>
        </array>
        
        <!-- This optional key specifies the user to run the job as. This key
        is only applicable when launchd is running as root. -->
        <key>UserName</key>
        <string>panic</string>
        
        <!-- Run every 12 hours -->
        <key>StartInterval</key>
        <integer>60</integer>

        <key>RunAtLoad</key>
        <true/>

        <key>StandardErrorPath</key>
        <string>/Users/panic/dev/btc_note/log/stderr.log</string>

        <key>StandardOutPath</key>
        <string>/Users/panic/dev/btc_note/log/stdout.log</string>
        
        <!-- low priority -->
        <key>Nice</key>
        <integer>20</integer>
        <key>LowPriorityIO</key>
        <true/>
    </dict>
    </plist>

###### Notificaciones

`pipenv install git+https://github.com/SeTeM/pync.git#egg=pync`
`brew install terminal-notifier` nesecita esta dependencia de ruby 


###### opciones para notificaciones:

- [1](https://weareopensource.me/python-osx/)
- [2](https://g3rv4.com/2015/08/macos-notifications-python-pycharm)
- [3](https://stackoverflow.com/questions/17651017/python-post-osx-notification)
- [pync](https://pypi.org/project/pync/)
    - [notificaciones por comandos](https://github.com/julienXX/terminal-notifier)
    - [notificaciones con acciones](https://github.com/vjeantet/alerter)
- [to be able to communicate with you over other devices.](https://github.com/dschep/ntfy)