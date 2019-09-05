from invoke import task
import os
@task
def log(c):
    c.run("rm -rf log/*")

@task
def deploy(c):
    actual_directory = os.getcwd()

    plist_data = {
        "user_name": "panic",
        "app_name": "btc_note",
        "main_dir": actual_directory,
        "run_time_interval": 60
    }

    sed_cmd = ""
    for k,v in plist_data.items():
        if not sed_cmd: 
            sed_cmd = "s#%s#%s#g" % (k, v) 
        else: 
            sed_cmd += "; s#%s#%s#g" % (k, v)
    
    plist_file = "/Users/%s/Library/LaunchAgents/com.%s.%s.plist" % (plist_data["user_name"], plist_data["user_name"], plist_data["app_name"])
    sed_cmd = "sed -e '%s' db/plist_template | > %s" % (sed_cmd, plist_file)
    #sed_cmd = "sed -e '%s' db/plist_template" % (sed_cmd)

    #c.run("launchctl unload %s" % (plist_file) )
    #c.run("rm -rf build dist setup.py %s log/*" % (plist_file))

    #plist_file = c.run(sed_cmd).stdout  # crear plist
    #c.run("echo")
    print(sed_cmd)
    c.run(sed_cmd)
    
    #c.run("py2applet --make-setup inspect/notice.py")
    #c.run("python setup.py py2app")
    #c.run("launchctl load %s" % (plist_file) )


