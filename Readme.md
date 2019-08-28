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

### Metodos para correr servicios
#### Crontab
    Agregar tarea a cronjob
    * * * * * significa cada minuto
    https://crontab.guru/#01_*_*_*_*

        crontab -e

    # correr .py en cron job
    -& "ampersand" para correr en segundo plano
    -Nesecita la ruta desde la raiz


    * * * * * /Users/panic/.local/share/virtualenvs/py-OPFHogRf/bin/python /Users/panic/dev/py/alarm.py >/Users/panic/dev/py/log/stdout.log 2>/Users/panic/dev/py/log/stderr.log &

    # correr freeze app echa con py2app 
    https://py2app.readthedocs.io/en/latest/tutorial.html#create-a-setup-py-file

        * * * * * /Users/panic/dev/py/dist/btc_swing.app/Contents/MacOS/btc_swing >/Users/panic/dev/py/log/stdout.log 2>/Users/panic/dev/py/log/stderr.log &

### Configurar servicio cron con un archivo Plist

    Guardar archivo en /Users/panic/Library/LaunchAgents
    >`launchctl load/unload` foo.plist
    >`plutil` Este comando "plutil ayuda a checar la sintaxis del archivo"

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
        <string>/Users/panic/dev/py/dist/btc_swing.app/Contents/MacOS/btc_swing</string>
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
        <string>/Users/panic/dev/py/log/stderr.log</string>

        <key>StandardOutPath</key>
        <string>/Users/panic/dev/py/log/stdout.log</string>
        
        <!-- low priority -->
        <key>Nice</key>
        <integer>20</integer>
        <key>LowPriorityIO</key>
        <true/>
    </dict>
    </plist>

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