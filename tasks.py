from invoke import task

@task
def log(c):
    c.run("rm -rf log/*")

@task
def deploy(c):
    c.run("rm -rf build dist setup.py")
    c.run("py2applet --make-setup btc_note.py")
    c.run("python setup.py py2app")
