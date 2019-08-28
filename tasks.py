from invoke import task

@task
def log(c):
    c.run("rm -rf log/*")

@task
def deploy(c):
    c.run("launchctl unload /Users/panic/Library/LaunchAgents/com.panic.btc_note.plist")
    c.run("rm -rf build dist setup.py log/*")
    c.run("py2applet --make-setup btc_note.py")
    c.run("python setup.py py2app")
    c.run("launchctl load /Users/panic/Library/LaunchAgents/com.panic.btc_note.plist")
